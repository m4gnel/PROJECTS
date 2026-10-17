import pytest
import httpx
from backend.services.jwt_service import create_access_token


@pytest.mark.asyncio
async def test_user_cannot_read_other_users_farm(async_client: httpx.AsyncClient):
    # RLS security check: accessing another user's farm must return 404
    jwt_b = create_access_token("00000000-0000-0000-0000-000000000002")
    token_b = f"Bearer {jwt_b}"

    resp = await async_client.get(
        "/api/v1/farms/00000000-0000-0000-0000-000000000000",
        headers={"Authorization": token_b}
    )
    assert resp.status_code == 404, f"Expected 404 for unowned farm, got {resp.status_code}"


@pytest.mark.asyncio
async def test_user_cannot_access_other_users_advisory(async_client: httpx.AsyncClient):
    jwt_b = create_access_token("00000000-0000-0000-0000-000000000002")
    token_b = f"Bearer {jwt_b}"
    resp = await async_client.get(
        "/api/v1/advisories/00000000-0000-0000-0000-000000000000",
        headers={"Authorization": token_b}
    )
    assert resp.status_code == 404, f"Expected 404 for unowned advisory, got {resp.status_code}"

