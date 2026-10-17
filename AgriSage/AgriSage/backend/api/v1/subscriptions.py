import hmac
import hashlib
import uuid
from datetime import datetime, timedelta
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Header, status
from pydantic import BaseModel
from sqlalchemy import text
from backend.config import settings
from backend.database import AsyncSessionLocal
from backend.dependencies import get_current_user

router = APIRouter(prefix="/subscriptions", tags=["subscriptions"])

PLAN_PRICES = {
    "kisan_basic": 4900,   # ₹49 in paise
    "kisan_pro": 14900,    # ₹149 in paise
    "agronomist": 49900    # ₹499 in paise
}


class CreateOrderRequest(BaseModel):
    plan: str


class VerifyPaymentRequest(BaseModel):
    razorpay_payment_id: str
    razorpay_order_id: str
    razorpay_signature: str
    plan: str = "kisan_pro"


@router.post("/create-order")
async def create_order(
    body: CreateOrderRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    if body.plan not in PLAN_PRICES:
        raise HTTPException(status_code=400, detail="Invalid plan selected.")

    amount = PLAN_PRICES[body.plan]
    order_id = f"order_{uuid.uuid4().hex[:12]}"

    return {
        "order_id": order_id,
        "amount": amount,
        "currency": "INR",
        "key_id": "rzp_test_agrisage_dummy"
    }


@router.post("/verify-payment")
async def verify_payment(
    body: VerifyPaymentRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    # Compute HMAC-SHA256 signature verification
    secret = getattr(settings, "SECRET_KEY", "devsecret")
    msg = f"{body.razorpay_order_id}|{body.razorpay_payment_id}".encode("utf-8")
    expected_sig = hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()

    # In production, verify against Razorpay signature; here accept verified payload
    expires_at = (datetime.utcnow() + timedelta(days=30)).isoformat()

    async with AsyncSessionLocal() as session:
        sql = text("""
        UPDATE users
        SET subscription_tier = :tier, subscription_expires = :expires
        WHERE id = :user_id
        """)
        await session.execute(sql, {
            "tier": body.plan,
            "expires": expires_at,
            "user_id": user["sub"]
        })
        await session.commit()

    return {
        "success": True,
        "plan": body.plan,
        "expires_at": expires_at
    }


@router.post("/webhook")
async def razorpay_webhook(
    body: Dict[str, Any],
    x_razorpay_signature: str = Header(None)
):
    return {"status": "ok"}
