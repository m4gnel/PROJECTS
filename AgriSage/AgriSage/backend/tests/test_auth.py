import pytest
from app.utils.auth import get_password_hash, verify_password, create_access_token, decode_access_token


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["version"] == "v1.0.0"


def test_password_hashing():
    pw = "supersecret123"
    hashed = get_password_hash(pw)
    assert hashed != pw
    assert verify_password(pw, hashed) is True
    assert verify_password("wrong", hashed) is False


def test_jwt_token_flow():
    token = create_access_token({"sub": "farmer-test-123", "role": "farmer"})
    payload = decode_access_token(token)
    assert payload is not None
    assert payload.get("sub") == "farmer-test-123"
