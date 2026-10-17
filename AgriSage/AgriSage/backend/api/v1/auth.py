import re
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config import settings
from backend.database import get_db
from backend.models.db import User, OTPSession, RefreshToken
from backend.services.jwt_service import (
    hash_otp, verify_otp, hash_token, create_access_token, create_refresh_token
)

try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

router = APIRouter(tags=["Authentication"])


E164_REGEX = re.compile(r"^\+[1-9]\d{1,14}$")


class SendOTPRequest(BaseModel):
    phone: str = Field(..., example="+919876543210")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip()
        if not E164_REGEX.match(v):
            raise ValueError("Invalid phone number format. Must be E.164 format (e.g. +919876543210)")
        return v


class VerifyOTPRequest(BaseModel):
    phone: str = Field(..., example="+919876543210")
    otp: str = Field(..., min_length=6, max_length=6, example="123456")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip()
        if not E164_REGEX.match(v):
            raise ValueError("Invalid phone number format. Must be E.164 format (e.g. +919876543210)")
        return v


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class LogoutRequest(BaseModel):
    refresh_token: str


@router.post("/auth/send-otp", status_code=status.HTTP_200_OK)
async def send_otp(payload: SendOTPRequest, db: AsyncSession = Depends(get_db)):
    """Generate a 6-digit OTP, bcrypt hash it, store session, print in dev mode."""
    phone = payload.phone
    now = datetime.now(timezone.utc)
    ten_mins_ago = now - timedelta(minutes=10)

    # 1. Check rate limit: max 5 OTP requests per phone per 10 minutes
    rate_stmt = select(OTPSession).where(
        OTPSession.phone == phone,
        OTPSession.created_at >= ten_mins_ago
    )
    res = await db.execute(rate_stmt)
    recent_sessions = res.scalars().all()
    if len(recent_sessions) >= 5:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Too many OTP requests"
        )

    # 2. Generate OTP: str(secrets.randbelow(1000000)).zfill(6)
    otp_code = str(secrets.randbelow(1000000)).zfill(6)

    # 3. Hash OTP with passlib bcrypt
    otp_hashed = hash_otp(otp_code)

    # 4. Delete any existing unexpired OTP for this phone
    await db.execute(
        delete(OTPSession).where(
            OTPSession.phone == phone,
            OTPSession.expires_at > now
        )
    )

    # 5. Insert into otp_sessions
    expires_at = now + timedelta(seconds=300)
    session = OTPSession(
        phone=phone,
        otp_hash=otp_hashed,
        expires_at=expires_at,
        attempts=0,
        used=False
    )
    db.add(session)
    await db.commit()

    # 6. In DEVELOPMENT environment: print OTP to console
    if settings.ENVIRONMENT == "development":
        print(f"\n[DEV OTP] Phone: {phone} | OTP: {otp_code}\n")
        logger.info("dev_otp_generated", phone=phone, otp=otp_code)

    return {"message": "OTP sent", "expires_in": 300}


@router.post("/auth/verify-otp", status_code=status.HTTP_200_OK)
async def verify_otp_endpoint(payload: VerifyOTPRequest, db: AsyncSession = Depends(get_db)):
    """Verify OTP hash, track attempts, upsert user, issue JWT pair."""
    phone = payload.phone
    otp = payload.otp
    now = datetime.now(timezone.utc)

    # 1. Find most recent unused unexpired otp_session for phone
    stmt = (
        select(OTPSession)
        .where(
            OTPSession.phone == phone,
            OTPSession.used == False,
            OTPSession.expires_at > now
        )
        .order_by(OTPSession.created_at.desc())
    )
    res = await db.execute(stmt)
    session = res.scalars().first()

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP"
        )

    # 2. Check failed attempts
    if session.attempts >= 5:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Too many failed attempts"
        )

    # 3. Increment attempts
    session.attempts += 1

    # 4. Verify bcrypt hash
    if not verify_otp(otp, session.otp_hash):
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid OTP"
        )

    # 5. Mark session used=True
    session.used = True

    # 6. Get or create user by phone
    user_stmt = select(User).where(User.phone == phone)
    user_res = await db.execute(user_stmt)
    user = user_res.scalars().first()

    if not user:
        user = User(
            phone=phone,
            language="ml",
            subscription_tier="free",
            is_active=True,
            last_active_at=now,
        )
        db.add(user)
        await db.flush()
    else:
        user.last_active_at = now

    # 7. Generate access token + refresh token pair
    access_token = create_access_token(str(user.id), subscription_tier=user.subscription_tier)
    raw_refresh, hashed_refresh = create_refresh_token(str(user.id))

    # 8. Store refresh token hash in refresh_tokens table
    ref_record = RefreshToken(
        user_id=user.id,
        token_hash=hashed_refresh,
        expires_at=now + timedelta(days=7),
        revoked=False,
    )
    db.add(ref_record)
    await db.commit()

    return {
        "access_token": access_token,
        "refresh_token": raw_refresh,
        "user": {
            "id": str(user.id),
            "phone": user.phone,
            "name": user.name,
            "language": user.language,
            "subscription_tier": user.subscription_tier,
        }
    }


@router.post("/auth/refresh", status_code=status.HTTP_200_OK)
async def refresh_tokens_endpoint(payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    """Rotate refresh token pair."""
    token = payload.refresh_token.strip()
    now = datetime.now(timezone.utc)

    # 1. Hash incoming token with SHA-256
    incoming_hash = hash_token(token)

    # 2. Find in refresh_tokens: must exist, NOT revoked, expires_at > NOW()
    stmt = select(RefreshToken).where(
        RefreshToken.token_hash == incoming_hash,
        RefreshToken.revoked == False,
        RefreshToken.expires_at > now
    )
    res = await db.execute(stmt)
    record = res.scalars().first()

    if not record:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # 3. Mark old token revoked=True BEFORE issuing new one
    record.revoked = True

    # 4. Fetch user
    user_res = await db.execute(select(User).where(User.id == record.user_id))
    user = user_res.scalars().first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # 5. Generate new access + refresh token pair
    new_access = create_access_token(str(user.id), subscription_tier=user.subscription_tier)
    new_raw_refresh, new_hashed_refresh = create_refresh_token(str(user.id))

    # 6. Store new refresh token hash
    new_record = RefreshToken(
        user_id=user.id,
        token_hash=new_hashed_refresh,
        expires_at=now + timedelta(days=7),
        revoked=False,
    )
    db.add(new_record)
    await db.commit()

    return {
        "access_token": new_access,
        "refresh_token": new_raw_refresh,
    }


@router.post("/auth/logout", status_code=status.HTTP_200_OK)
async def logout_endpoint(payload: LogoutRequest, db: AsyncSession = Depends(get_db)):
    """Revoke refresh token on logout."""
    token = payload.refresh_token.strip()
    incoming_hash = hash_token(token)

    await db.execute(
        update(RefreshToken)
        .where(RefreshToken.token_hash == incoming_hash)
        .values(revoked=True)
    )
    await db.commit()

    return {"message": "Logged out"}
