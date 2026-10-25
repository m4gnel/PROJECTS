"""Canonical roles and permissions for the production API.

The JWT contains these values for client ergonomics, but authorization must use
the values resolved from the persisted :class:`User` row.  Keeping the role
catalogue in one module prevents individual routers from inventing slightly
different role or permission spellings.
"""

from enum import Enum
from typing import Any, Iterable


class UserRole(str, Enum):
    FARMER = "farmer"
    EMPLOYEE = "employee"
    OFFICER = "officer"
    EXPERT = "expert"


FARMER_PERMISSIONS = frozenset(
    {
        "advisory:read",
        "farms:read",
        "farms:write",
    }
)

OPERATIONS_READ_PERMISSIONS = frozenset(
    {
        "operations:summary:read",
        "operations:queue:read",
        "operations:service-boundary:read",
    }
)

EXPERT_PERMISSIONS = frozenset(
    {
        "expert:queue:read",
        "expert:review:write",
    }
)


# These are the only permissions that can be resolved for a persisted role.
# A malformed or over-privileged database value is rejected rather than
# silently widened.
ROLE_PERMISSIONS = {
    UserRole.FARMER.value: FARMER_PERMISSIONS,
    UserRole.EMPLOYEE.value: OPERATIONS_READ_PERMISSIONS,
    UserRole.OFFICER.value: OPERATIONS_READ_PERMISSIONS,
    UserRole.EXPERT.value: FARMER_PERMISSIONS | EXPERT_PERMISSIONS,
}
KNOWN_PERMISSIONS = frozenset().union(*ROLE_PERMISSIONS.values())


def normalize_role(value: Any) -> UserRole | None:
    """Return a known role or ``None`` for invalid persisted input."""

    if isinstance(value, UserRole):
        return value
    if not isinstance(value, str):
        return None
    try:
        return UserRole(value.strip().lower())
    except ValueError:
        return None


def normalize_permissions(value: Any) -> frozenset[str] | None:
    """Validate a JSONB permission list without accepting arbitrary claims."""

    if value is None:
        return None
    if not isinstance(value, (list, tuple, set)):
        return None
    if any(not isinstance(permission, str) for permission in value):
        return None
    permissions = frozenset(value)
    if not permissions.issubset(KNOWN_PERMISSIONS):
        return None
    return permissions


def resolve_permissions(role: Any, stored_permissions: Any = None) -> frozenset[str] | None:
    """Resolve safe permissions for a role and optional persisted grants.

    An empty or missing JSONB value uses the role defaults for migration
    compatibility.  A non-empty value becomes the explicit least-privilege
    grant, but it may only contain permissions already allowed for that role.
    Malformed values fail closed.
    """

    normalized_role = normalize_role(role)
    if normalized_role is None:
        return None

    role_permissions = ROLE_PERMISSIONS[normalized_role.value]
    if stored_permissions is None:
        return role_permissions
    normalized_stored = normalize_permissions(stored_permissions)
    if normalized_stored is None:
        return None
    if not normalized_stored.issubset(role_permissions):
        return None
    return normalized_stored or role_permissions


def user_rbac_claims(user: Any) -> tuple[str, list[str]]:
    """Return canonical role and permission claims from a persisted user."""

    role = normalize_role(getattr(user, "role", None))
    permissions = resolve_permissions(role, getattr(user, "permissions", None))
    if role is None or permissions is None:
        raise ValueError("User has an invalid role or permission set")
    return role.value, sorted(permissions)


def claims_for_role(role: Any, permissions: Iterable[str] | None = None) -> tuple[str, list[str]]:
    """Validate server-issued token claims against the role catalogue."""

    normalized_role = normalize_role(role)
    resolved = resolve_permissions(normalized_role, permissions)
    if normalized_role is None or resolved is None:
        raise ValueError("Unknown role or permission set")
    return normalized_role.value, sorted(resolved)
