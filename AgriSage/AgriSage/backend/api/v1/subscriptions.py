import hmac
import hashlib
import json
import uuid
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
from fastapi import APIRouter, Body, Depends, Header, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from backend.config import settings
from backend.database import AsyncSessionLocal
from backend.dependencies import get_current_user

try:
    import razorpay
except ImportError:
    razorpay = None

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


def _razorpay_client():
    if razorpay is None or not settings.RAZORPAY_KEY_ID or not settings.RAZORPAY_KEY_SECRET:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment provider is not configured",
        )
    return razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))


@router.post("/create-order")
async def create_order(
    body: CreateOrderRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    if body.plan not in PLAN_PRICES:
        raise HTTPException(status_code=400, detail="Invalid plan selected.")

    amount = PLAN_PRICES[body.plan]
    client = _razorpay_client()
    try:
        order = client.order.create(
            {
                "amount": amount,
                "currency": "INR",
                "receipt": f"agrisage_{uuid.uuid4().hex}",
                "notes": {"plan": body.plan, "user_id": str(user["sub"])},
            }
        )
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Payment provider order creation failed",
        ) from exc

    return {
        "order_id": order["id"],
        "amount": amount,
        "currency": "INR",
        "key_id": settings.RAZORPAY_KEY_ID,
    }


@router.post("/verify-payment")
async def verify_payment(
    body: VerifyPaymentRequest,
    user: Dict[str, Any] = Depends(get_current_user)
):
    if body.plan not in PLAN_PRICES:
        raise HTTPException(status_code=400, detail="Invalid plan selected.")

    # The Razorpay secret is separate from the JWT signing secret.
    secret = settings.RAZORPAY_KEY_SECRET
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment provider is not configured",
        )
    msg = f"{body.razorpay_order_id}|{body.razorpay_payment_id}".encode("utf-8")
    expected_sig = hmac.new(secret.encode("utf-8"), msg, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_sig, body.razorpay_signature):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid payment signature")

    client = _razorpay_client()
    try:
        order = client.order.fetch(body.razorpay_order_id)
        payment = client.payment.fetch(body.razorpay_payment_id)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Payment provider verification failed",
        ) from exc

    notes = order.get("notes") or {}
    if (
        order.get("amount") != PLAN_PRICES[body.plan]
        or order.get("currency") != "INR"
        or notes.get("plan") != body.plan
        or str(notes.get("user_id")) != str(user["sub"])
        or payment.get("order_id") != body.razorpay_order_id
        or payment.get("status") not in {"authorized", "captured"}
    ):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Payment details do not match order")

    expires_at = datetime.now(timezone.utc) + timedelta(days=30)

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
        "expires_at": expires_at.isoformat()
    }


@router.post("/webhook")
async def razorpay_webhook(
    body: bytes = Body(...),
    x_razorpay_signature: str = Header(default="")
):
    secret = settings.RAZORPAY_WEBHOOK_SECRET
    if not secret:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Payment webhook is not configured",
        )

    expected_sig = hmac.new(secret.encode("utf-8"), body, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected_sig, x_razorpay_signature):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook signature")

    try:
        json.loads(body)
    except (TypeError, json.JSONDecodeError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid webhook payload") from exc

    # Signature verification is complete; event-specific fulfillment remains idempotent work.
    return {"status": "accepted"}
