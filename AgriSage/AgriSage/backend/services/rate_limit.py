"""Database-backed rate limits for security-sensitive endpoints.

The limiter uses a hashed key so phone numbers, IP addresses, and opaque
refresh tokens are not stored in the rate-limit table.  The upsert is atomic in
PostgreSQL and therefore works across multiple Uvicorn workers.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


def hashed_rate_key(scope: str, identifier: str) -> str:
    """Return a stable, non-reversible key for a rate-limit subject."""

    value = f"{scope}:{identifier}".encode("utf-8")
    return hashlib.sha256(value).hexdigest()


async def enforce_rate_limit(
    db: AsyncSession,
    *,
    key: str,
    limit: int,
    window_seconds: int,
) -> None:
    """Atomically count a request and reject it once the limit is exceeded."""

    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(seconds=window_seconds)
    try:
        result = await db.execute(
            text(
                """
                INSERT INTO auth_rate_limits (
                    rate_key, window_start, request_count, max_allowed, updated_at
                )
                VALUES (:rate_key, :now, 1, :limit, :now)
                ON CONFLICT (rate_key) DO UPDATE
                SET window_start = CASE
                        WHEN auth_rate_limits.window_start <= :cutoff
                        THEN EXCLUDED.window_start
                        ELSE auth_rate_limits.window_start
                    END,
                    request_count = CASE
                        WHEN auth_rate_limits.window_start <= :cutoff
                        THEN 1
                        ELSE auth_rate_limits.request_count + 1
                    END,
                    max_allowed = EXCLUDED.max_allowed,
                    updated_at = EXCLUDED.updated_at
                RETURNING request_count
                """
            ),
            {
                "rate_key": key,
                "now": now,
                "cutoff": cutoff,
                "limit": limit,
            },
        )
        row = result.mappings().one()
        # Commit the counter independently from the business transaction.  A
        # failed OTP/provider request must not roll back the abuse-prevention
        # accounting and allow an attacker to retry indefinitely.
        await db.commit()
    except HTTPException:
        raise
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication rate-limit storage is unavailable",
        ) from exc

    if int(row["request_count"]) > limit:
        retry_after = max(window_seconds, 1)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many requests",
            headers={"Retry-After": str(retry_after)},
        )
