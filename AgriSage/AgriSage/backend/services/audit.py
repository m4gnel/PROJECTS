"""Audit helpers for privileged API activity."""

import ipaddress
import json
from typing import Any, Mapping, Optional

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


class AuditLogUnavailable(RuntimeError):
    """Raised when a privileged event cannot be durably recorded."""


def _safe_ip_address(value: Optional[str]) -> Optional[str]:
    if not value:
        return None
    try:
        return str(ipaddress.ip_address(value))
    except ValueError:
        return None


async def record_audit_event(
    db: AsyncSession,
    *,
    user_id: str,
    event_type: str,
    event_data: Optional[Mapping[str, Any]] = None,
    ip_address: Optional[str] = None,
) -> None:
    """Write an event to the existing ``audit_logs`` contract.

    Migration ``016_audit`` intentionally provides an event-oriented table
    for this kind of access record.  The operation is committed together with
    the caller's privileged work; callers fail closed if the audit write
    cannot be completed.
    """

    try:
        await db.execute(
            text(
                """
                INSERT INTO audit_logs (user_id, event_type, event_data, ip_address)
                VALUES (CAST(:user_id AS UUID), :event_type,
                        CAST(:event_data AS JSONB), CAST(:ip_address AS INET))
                """
            ),
            {
                "user_id": str(user_id),
                "event_type": event_type,
                "event_data": json.dumps(dict(event_data or {})),
                "ip_address": _safe_ip_address(ip_address),
            },
        )
        await db.commit()
    except Exception as exc:
        raise AuditLogUnavailable("Privileged activity could not be audited") from exc
