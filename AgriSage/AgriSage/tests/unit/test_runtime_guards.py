import pytest
from fastapi import HTTPException

from backend.api.v1.subscriptions import (
    CreateOrderRequest,
    VerifyPaymentRequest,
    create_order,
    verify_payment,
)
from backend.config import Settings, settings


def test_production_defaults_are_rejected():
    production = Settings(
        _env_file=None,
        ENVIRONMENT="production",
        CORS_ORIGINS=["https://console.example.com"],
        PUBLIC_BASE_URL="https://api.example.com",
    )

    with pytest.raises(RuntimeError, match="Unsafe production configuration"):
        production.validate_runtime()


def test_valid_production_configuration_is_accepted():
    production = Settings(
        _env_file=None,
        ENVIRONMENT="production",
        DATABASE_URL="postgresql+asyncpg://runtime:strong-password@db:5432/agrisage",
        DB_PASSWORD="a-real-production-password",
        SECRET_KEY="a" * 48,
        CORS_ORIGINS=["https://console.example.com"],
        PUBLIC_BASE_URL="https://api.example.com",
        OTP_PROVIDER="generic_http",
        OTP_PROVIDER_URL="https://sms.example.com/otp",
        OTP_PROVIDER_KEY="provider-secret",
        GEMINI_API_KEY="gemini-production-key",
        R2_BUCKET="agrisage-images",
        R2_ACCOUNT_ID="account-id",
        R2_ACCESS_KEY="r2-access",
        R2_SECRET_KEY="r2-secret",
    )

    production.validate_runtime()


@pytest.mark.asyncio
async def test_create_order_fails_closed_without_payment_provider(monkeypatch):
    monkeypatch.setattr(settings, "RAZORPAY_KEY_ID", "")
    monkeypatch.setattr(settings, "RAZORPAY_KEY_SECRET", "")

    with pytest.raises(HTTPException) as exc_info:
        await create_order(CreateOrderRequest(plan="kisan_pro"), {"sub": "user-1"})

    assert exc_info.value.status_code == 503


@pytest.mark.asyncio
async def test_invalid_payment_signature_is_rejected(monkeypatch):
    monkeypatch.setattr(settings, "RAZORPAY_KEY_SECRET", "test-payment-secret")

    with pytest.raises(HTTPException) as exc_info:
        await verify_payment(
            VerifyPaymentRequest(
                razorpay_payment_id="pay_1",
                razorpay_order_id="order_1",
                razorpay_signature="not-valid",
                plan="kisan_pro",
            ),
            {"sub": "user-1"},
        )

    assert exc_info.value.status_code == 400
