from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4

import httpx
import pytest
from fastapi import HTTPException
from fastapi.security import HTTPAuthorizationCredentials
from jose import jwt

from backend.config import settings
from backend.database import get_db
from backend.dependencies import (
    require_auth,
    require_expert_access,
    require_permissions,
    require_principal,
    require_roles,
)
from backend.main import app
from backend.models.db import User
from backend.services.jwt_service import create_access_token, verify_access_token


class _Result:
    def __init__(self, user=None):
        self.user = user

    def scalar_one_or_none(self):
        return self.user


class _AuditSession:
    def __init__(self, user=None):
        self.user = user
        self.executed = []
        self.commits = 0

    async def execute(self, statement, params=None):
        sql = str(statement)
        self.executed.append((sql, params))
        if "FROM users" in sql:
            return _Result(self.user)
        return _Result()

    async def commit(self):
        self.commits += 1


class _MappingResult:
    def __init__(self, rows):
        self.rows = rows

    def mappings(self):
        return self

    def one(self):
        return self.rows[0]

    def all(self):
        return self.rows


class _OperationsSession(_AuditSession):
    async def execute(self, statement, params=None):
        sql = str(statement)
        self.executed.append((sql, params))
        if "COUNT(*)" in sql:
            return _MappingResult(
                [
                    {
                        "active_advisories": 2,
                        "needs_review": 1,
                        "high_confidence": 1,
                        "average_confidence": 0.82,
                    }
                ]
            )
        if "FROM advisories AS a" in sql:
            return _MappingResult(
                [
                    {
                        "id": uuid4(),
                        "created_at": datetime.now(timezone.utc),
                        "confidence_state": "UNCERTAIN",
                        "confidence_score": 0.42,
                        "safe_to_act": False,
                        "triage_status": "ESCALATED",
                        "farmer_name": "Rajan K.",
                        "farmer_phone": "+919876543210",
                        "farm_name": "North field",
                        "district": "Wayanad",
                        "crop": "Rice",
                    }
                ]
            )
        return _Result()


def _user(*, role: str = "farmer", subscription_tier: str = "free") -> User:
    return User(
        id=uuid4(),
        phone="+919876543210",
        role=role,
        permissions=[],
        subscription_tier=subscription_tier,
        is_active=True,
    )


def test_access_token_has_explicit_rbac_claims():
    user_id = str(uuid4())
    token = create_access_token(user_id, role="officer")
    payload = verify_access_token(token)

    assert payload["sub"] == user_id
    assert payload["role"] == "officer"
    assert "operations:queue:read" in payload["permissions"]
    assert payload["subscription_tier"] == "free"


@pytest.mark.asyncio
async def test_invalid_and_expired_jwt_fail_closed():
    db = _AuditSession()
    credentials = HTTPAuthorizationCredentials(scheme="Bearer", credentials="not-a-jwt")
    with pytest.raises(HTTPException) as invalid:
        await require_auth(credentials, db)
    assert invalid.value.status_code == 401

    expired = jwt.encode(
        {
            "sub": str(uuid4()),
            "exp": datetime.now(timezone.utc) - timedelta(minutes=1),
        },
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    with pytest.raises(HTTPException) as expired_error:
        await require_auth(
            HTTPAuthorizationCredentials(scheme="Bearer", credentials=expired),
            db,
        )
    assert expired_error.value.status_code == 401


@pytest.mark.asyncio
async def test_role_is_resolved_from_persisted_user_not_jwt_claim():
    persisted_user = _user(role="farmer")
    db = _AuditSession(persisted_user)
    auth = {
        "sub": str(persisted_user.id),
        "role": "officer",
        "permissions": ["operations:queue:read"],
    }

    principal = await require_principal(auth, db)
    assert principal["role"] == "farmer"
    assert "operations:queue:read" not in principal["permissions"]

    officer_only = require_roles("officer")
    with pytest.raises(HTTPException) as denied:
        await officer_only(principal)
    assert denied.value.status_code == 403


@pytest.mark.asyncio
async def test_permission_dependency_is_least_privilege():
    principal = {
        "sub": str(uuid4()),
        "role": "officer",
        "permissions": ["operations:summary:read"],
    }

    assert (await require_permissions("operations:summary:read")(principal)) == principal
    with pytest.raises(HTTPException) as denied:
        await require_permissions("operations:queue:read")(principal)
    assert denied.value.status_code == 403


@pytest.mark.asyncio
async def test_expert_subscription_compatibility_is_preserved():
    persisted_user = _user(role="farmer", subscription_tier="expert")
    principal = await require_principal(
        {"sub": str(persisted_user.id), "role": "farmer"},
        _AuditSession(persisted_user),
    )

    assert (await require_expert_access(principal))["subscription_tier"] == "expert"


@pytest.mark.asyncio
async def test_operations_endpoint_allows_staff_and_denies_farmer():
    async def staff_principal():
        return {
            "sub": str(uuid4()),
            "role": "officer",
            "permissions": [
                "operations:summary:read",
                "operations:queue:read",
                "operations:service-boundary:read",
            ],
        }

    app.dependency_overrides.clear()
    from backend.dependencies import require_principal as principal_dependency

    app.dependency_overrides[principal_dependency] = staff_principal
    app.dependency_overrides[get_db] = lambda: _AuditSession()
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            allowed = await client.get("/api/v1/operations/service-boundary")
        assert allowed.status_code == 200
        assert allowed.json()["read_only"] is True
    finally:
        app.dependency_overrides.clear()


@pytest.mark.asyncio
async def test_operations_read_contracts_are_audited():
    async def staff_principal():
        return {
            "sub": str(uuid4()),
            "role": "employee",
            "permissions": [
                "operations:summary:read",
                "operations:queue:read",
                "operations:service-boundary:read",
            ],
        }

    from backend.dependencies import require_principal as principal_dependency

    session = _OperationsSession()
    app.dependency_overrides[principal_dependency] = staff_principal
    app.dependency_overrides[get_db] = lambda: session
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            summary = await client.get("/api/v1/operations/summary")
            queue = await client.get("/api/v1/operations/queue?limit=1")
            boundary = await client.get("/api/v1/operations/service-boundary")
        assert summary.status_code == 200
        assert summary.json()["read_only"] is True
        assert queue.status_code == 200
        assert queue.json()["total_pending"] == 1
        assert queue.json()["items"][0]["farmer_name"] == "Rajan K."
        assert queue.json()["items"][0]["triage_status"] == "ESCALATED"
        assert boundary.status_code == 200
        assert len([sql for sql, _ in session.executed if "audit_logs" in sql]) == 3
    finally:
        app.dependency_overrides.clear()

    async def farmer_principal():
        return {"sub": str(uuid4()), "role": "farmer", "permissions": ["advisory:read"]}

    app.dependency_overrides[principal_dependency] = farmer_principal
    app.dependency_overrides[get_db] = lambda: _AuditSession()
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            denied = await client.get("/api/v1/operations/service-boundary")
        assert denied.status_code == 403
    finally:
        app.dependency_overrides.clear()


def test_user_model_has_additive_rbac_state():
    assert User.__table__.c.role.nullable is False
    assert User.__table__.c.permissions.nullable is False
    assert User.__table__.c.subscription_tier is not None
    assert "chk_users_role" in {constraint.name for constraint in User.__table__.constraints}

    migration = Path(__file__).parents[2] / "alembic" / "versions" / "019_user_rbac.py"
    migration_source = migration.read_text(encoding="utf-8")
    assert 'down_revision: Union[str, None] = "018_master_database_schema"' in migration_source
    assert 'sa.Column("role"' in migration_source
    assert 'sa.Column("permissions"' in migration_source
    assert "farms_operations_staff" in migration_source
    assert "advisories_operations_staff" in migration_source

    repair_migration = Path(__file__).parents[2] / "alembic" / "versions" / "022_rls_policy_repair.py"
    repair_source = repair_migration.read_text(encoding="utf-8")
    assert "adv_operations_staff" in repair_source
    assert "Revises: 021_mobile_field_contract" in repair_source
