import pytest
from backend.services.jwt_service import (
    hash_otp, verify_otp, hash_token,
    create_access_token, create_refresh_token, verify_access_token
)

def test_otp_hashing():
    otp = "123456"
    hashed = hash_otp(otp)
    assert verify_otp("123456", hashed) is True
    assert verify_otp("654321", hashed) is False

def test_jwt_tokens():
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    access_token = create_access_token(user_id, subscription_tier="free")
    payload = verify_access_token(access_token)
    assert payload["sub"] == user_id
    assert payload["tier"] == "free"

def test_refresh_tokens():
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    raw, hashed = create_refresh_token(user_id)
    assert raw != hashed
    assert hash_token(raw) == hashed
