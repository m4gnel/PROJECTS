import logging
import uuid
from datetime import datetime, timezone
from typing import Any, Dict, Iterable

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import select, text
from sqlalchemy.exc import OperationalError
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt

from backend.config import settings
from backend.database import get_db
from backend.models.db import User
from backend.rbac import KNOWN_PERMISSIONS, UserRole, normalize_role, resolve_permissions

logger = logging.getLogger(__name__)

security_scheme = HTTPBearer(auto_error=True)


def require_subject_identity(requested_id: str | None, principal: Dict[str, Any]) -> str:
    """Return the JWT subject and reject a conflicting request identity.

    Farmer/user identifiers in request bodies are retained for mobile-client
    compatibility, but they are never an authorization input.  A mismatch is
    rejected rather than silently routing work to another tenant, which also
    makes stale or corrupted client state visible to the caller.
    """

    subject = str(principal.get("sub") or "")
    matches = False
    if subject and requested_id is not None:
        try:
            matches = uuid.UUID(str(requested_id)) == uuid.UUID(subject)
        except (AttributeError, TypeError, ValueError):
            matches = str(requested_id) == subject
    if not matches:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="farmer_id must match the authenticated user",
        )
    return subject


async def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    FastAPI dependency enforcing JWT authentication.
    Decodes the Bearer token, checks expiration, sets the PostgreSQL RLS
    session variable app.current_user_id, and returns the payload dict.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            uuid.UUID(str(user_id))
        except (AttributeError, TypeError, ValueError) as exc:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            ) from exc

        # Set PostgreSQL session variable for Row-Level Security (RLS).
        # set_config is parameterized; interpolating a JWT subject into SET
        # would allow malformed subjects to alter the SQL statement.
        try:
            await db.execute(
                text("SELECT set_config('app.current_user_id', :user_id, true)"),
                {"user_id": str(user_id)},
            )
        except (OperationalError, ConnectionRefusedError, TimeoutError, OSError):
            # Some authenticated endpoints (weather and other external-data
            # reads) do not require the database. They can remain available
            # during a database outage; database-backed handlers still fail
            # at their first query. Never suppress SQL/programming errors.
            logger.warning("database unavailable while setting RLS context")
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Authentication storage is unavailable",
            ) from exc

        return payload

    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


async def require_principal(
    auth: Dict[str, Any] = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Resolve an authenticated token subject to the persisted user record.

    JWT role and permission claims are informational only.  Every RBAC route
    uses this dependency, which reloads the active user and derives canonical
    claims from the database.  Missing storage, an unknown user, and malformed
    role data all fail closed.
    """

    subject = auth.get("sub")
    try:
        user_id = uuid.UUID(str(subject))
    except (AttributeError, TypeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        result = await db.execute(select(User).where(User.id == user_id))
        user = result.scalar_one_or_none()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Authentication storage is unavailable",
        ) from exc

    if user is None or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active",
            headers={"WWW-Authenticate": "Bearer"},
        )

    role = normalize_role(getattr(user, "role", None))
    permissions = resolve_permissions(role, getattr(user, "permissions", None))
    if role is None or permissions is None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User role is not authorized",
        )

    subscription_tier = getattr(user, "subscription_tier", "free") or "free"
    principal = dict(auth)
    principal.update(
        {
            "sub": str(user.id),
            "tier": subscription_tier,
            "subscription_tier": subscription_tier,
            "role": role.value,
            "permissions": sorted(permissions),
            "user": user,
        }
    )
    return principal


def require_roles(*allowed_roles: UserRole | str):
    """Build a dependency that allows any one of the supplied roles."""

    normalized_roles = {normalize_role(role) for role in allowed_roles}
    if not allowed_roles or None in normalized_roles:
        normalized_roles = set()

    async def dependency(principal: Dict[str, Any] = Depends(require_principal)) -> Dict[str, Any]:
        if principal.get("role") not in {role.value for role in normalized_roles}:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role for this operation",
            )
        return principal

    return dependency


def require_permissions(*allowed_permissions: str):
    """Build a dependency requiring all supplied canonical permissions."""

    requested = frozenset(allowed_permissions)

    async def dependency(principal: Dict[str, Any] = Depends(require_principal)) -> Dict[str, Any]:
        granted = frozenset(principal.get("permissions", []))
        if not requested or not requested.issubset(KNOWN_PERMISSIONS) or not requested.issubset(granted):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions for this operation",
            )
        return principal

    return dependency


def require_access(
    *,
    roles: Iterable[UserRole | str] = (),
    permissions: Iterable[str] = (),
):
    """Build a dependency requiring both an allowed role and permissions."""

    normalized_roles = {normalize_role(role) for role in roles}
    requested_permissions = frozenset(permissions)
    role_values = (
        set()
        if None in normalized_roles
        else {role.value for role in normalized_roles}
    )

    async def dependency(principal: Dict[str, Any] = Depends(require_principal)) -> Dict[str, Any]:
        role_allowed = bool(role_values) and principal.get("role") in role_values
        permissions_allowed = (
            bool(requested_permissions)
            and requested_permissions.issubset(KNOWN_PERMISSIONS)
            and requested_permissions.issubset(frozenset(principal.get("permissions", [])))
        )
        if not (role_allowed and permissions_allowed):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient role or permissions for this operation",
            )
        return principal

    return dependency


async def require_expert_access(
    principal: Dict[str, Any] = Depends(require_principal),
) -> Dict[str, Any]:
    """Preserve expert subscription access while preferring persisted RBAC."""

    user = principal.get("user")
    subscription_expires = getattr(user, "subscription_expires", None)
    subscription_active = principal.get("subscription_tier") == "expert" and (
        subscription_expires is None
        or subscription_expires > datetime.now(timezone.utc)
    )
    if (
        principal.get("role") == UserRole.EXPERT.value
        or subscription_active
        or "expert:queue:read" in principal.get("permissions", [])
    ):
        return principal
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Expert access is required for this operation",
    )


# Backward-compatible name used by the canonical v1 routers.  It now resolves
# the active persisted user rather than exposing untrusted role claims.
get_current_user = require_principal

