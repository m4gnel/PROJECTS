import re
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel, Field, field_validator
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config import settings
from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models.db import User, OTPSession, RefreshToken
from backend.services.jwt_service import (
    hash_otp, verify_otp, hash_token, create_access_token, create_refresh_token
)
from backend.services.otp_provider import OTPProviderError, configured_otp_provider
from backend.services.rate_limit import enforce_rate_limit, hashed_rate_key
from backend.rbac import user_rbac_claims

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
    name: str | None = Field(default=None, max_length=100)

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str) -> str:
        v = v.strip()
        if not E164_REGEX.match(v):
            raise ValueError("Invalid phone number format. Must be E.164 format (e.g. +919876543210)")
        return v


class RefreshTokenRequest(BaseModel):
    refresh_token: str = Field(..., min_length=32, max_length=512)


class LogoutRequest(BaseModel):
    refresh_token: str = Field(..., min_length=32, max_length=512)


class ProfileUpdateRequest(BaseModel):
    """Writable fields shared by the Android profile screen."""

    name: str | None = Field(default=None, max_length=100)
    district: str | None = Field(default=None, max_length=100)
    state: str | None = Field(default=None, max_length=100)
    preferred_language: str | None = Field(default=None, max_length=10)
    latitude: float | None = Field(default=None, ge=6.0, le=38.0)
    longitude: float | None = Field(default=None, ge=68.0, le=97.5)


@router.get("/auth/me", status_code=status.HTTP_200_OK)
async def current_user_profile(auth: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Return the persisted user profile in the mobile/web client contract."""

    user = auth["user"]
    return {
        "id": str(user.id),
        "phone": user.phone,
        "name": user.name or "",
        "village": None,
        "district": user.district,
        "state": user.state or "India",
        "preferred_language": user.language,
        "latitude": float(user.location_lat) if user.location_lat is not None else None,
        "longitude": float(user.location_lon) if user.location_lon is not None else None,
        "is_active": user.is_active,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }


@router.put("/farmers/me", status_code=status.HTTP_200_OK)
async def update_current_user_profile(
    payload: ProfileUpdateRequest,
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Update only the authenticated user's profile fields."""

    user = auth["user"]
    updates = payload.model_dump(exclude_none=True)
    if "preferred_language" in updates:
        updates["language"] = updates.pop("preferred_language")
    if "latitude" in updates:
        updates["location_lat"] = updates.pop("latitude")
    if "longitude" in updates:
        updates["location_lon"] = updates.pop("longitude")
    for field_name, value in updates.items():
        setattr(user, field_name, value.strip() if isinstance(value, str) else value)
    await db.commit()
    await db.refresh(user)
    return await current_user_profile({**auth, "user": user})


@router.post("/auth/send-otp", status_code=status.HTTP_200_OK)
async def send_otp(
    payload: SendOTPRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Generate, deliver, and persist a six-digit OTP.

    Production requires the explicitly configured generic HTTP provider.  The
    console path is available only when ``OTP_DEV_MODE=true`` outside
    production, so a missing provider cannot silently disable sign-in.
    """
    phone = payload.phone
    client_ip = request.client.host if request.client else "unknown"
    await enforce_rate_limit(
        db,
        key=hashed_rate_key("otp-send-phone", phone),
        limit=5,
        window_seconds=600,
    )
    await enforce_rate_limit(
        db,
        key=hashed_rate_key("otp-send-ip", client_ip),
        limit=20,
        window_seconds=600,
    )

    now = datetime.now(timezone.utc)
    otp_code = str(secrets.randbelow(1000000)).zfill(6)

    provider = configured_otp_provider()
    if provider is not None:
        try:
            await provider.deliver(phone=phone, otp=otp_code)
        except OTPProviderError as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="OTP delivery provider is unavailable",
            ) from exc
    elif settings.OTP_DEV_MODE and settings.ENVIRONMENT.lower() != "production":
        # Deliberately print only in the explicit local development mode.  Do
        # not send the OTP to structured logs or include it in the response.
        print(f"\n[DEV OTP] Phone: {phone} | OTP: {otp_code}\n")
    else:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="OTP delivery provider is not configured",
        )

    otp_hashed = hash_otp(otp_code)
    await db.execute(
        delete(OTPSession).where(
            OTPSession.phone == phone,
            OTPSession.expires_at > now,
        )
    )
    expires_at = now + timedelta(seconds=300)
    db.add(
        OTPSession(
            phone=phone,
            otp_hash=otp_hashed,
            expires_at=expires_at,
            attempts=0,
            used=False,
        )
    )
    await db.commit()

    return {"message": "OTP sent", "expires_in": 300}


@router.post("/auth/verify-otp", status_code=status.HTTP_200_OK)
async def verify_otp_endpoint(
    payload: VerifyOTPRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Verify OTP hash, track attempts, upsert user, issue JWT pair."""
    phone = payload.phone
    otp = payload.otp
    display_name = payload.name.strip() if payload.name else None
    client_ip = request.client.host if request.client else "unknown"
    await enforce_rate_limit(
        db,
        key=hashed_rate_key("otp-verify-phone", phone),
        limit=10,
        window_seconds=600,
    )
    await enforce_rate_limit(
        db,
        key=hashed_rate_key("otp-verify-ip", client_ip),
        limit=30,
        window_seconds=600,
    )
    now = datetime.now(timezone.utc)

    # 1. Find most recent unused unexpired otp_session for phone
    stmt = (
        select(OTPSession)
        .where(
            OTPSession.phone == phone,
            OTPSession.used.is_(False),
            OTPSession.expires_at > now
        )
        .order_by(OTPSession.created_at.desc())
        .with_for_update()
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

    # 4. Verify bcrypt hash.  A corrupt stored hash is treated as an invalid
    # attempt rather than becoming an internal-error oracle.
    try:
        valid_otp = verify_otp(otp, session.otp_hash)
    except Exception:
        valid_otp = False
    if not valid_otp:
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
            name=display_name,
            language="ml",
            subscription_tier="free",
            is_active=True,
            last_active_at=now,
        )
        db.add(user)
        await db.flush()
    else:
        user.last_active_at = now
        if display_name and not user.name:
            user.name = display_name

    # 7. Resolve persisted RBAC state before issuing token claims.
    try:
        role, permissions = user_rbac_claims(user)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User authorization state is unavailable",
        ) from exc

    # 8. Generate access token + refresh token pair
    access_token = create_access_token(
        str(user.id),
        subscription_tier=user.subscription_tier,
        role=role,
        permissions=permissions,
    )
    raw_refresh, hashed_refresh = create_refresh_token(str(user.id))

    # 9. Store refresh token hash in refresh_tokens table
    ref_record = RefreshToken(
        user_id=user.id,
        token_hash=hashed_refresh,
        expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
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
            "role": role,
            "permissions": permissions,
        }
    }


@router.post("/auth/refresh", status_code=status.HTTP_200_OK)
async def refresh_tokens_endpoint(
    payload: RefreshTokenRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Rotate refresh token pair."""
    token = payload.refresh_token.strip()
    client_ip = request.client.host if request.client else "unknown"
    await enforce_rate_limit(
        db,
        key=hashed_rate_key("refresh-ip", client_ip),
        limit=30,
        window_seconds=60,
    )
    now = datetime.now(timezone.utc)

    # 1. Hash incoming token with SHA-256
    incoming_hash = hash_token(token)

    # 2. Find in refresh_tokens: must exist, NOT revoked, expires_at > NOW()
    # Lock the token row before checking and revoking it.  Without this lock,
    # two concurrent refresh requests can both observe the same live token and
    # each mint a valid successor.
    stmt = (
        select(RefreshToken)
        .where(
            RefreshToken.token_hash == incoming_hash,
            RefreshToken.revoked.is_(False),
            RefreshToken.expires_at > now,
        )
        .with_for_update()
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
        # The presented token is consumed even when its subject was disabled
        # between issuance and refresh.  Otherwise a revoked account could
        # repeatedly replay the same refresh token.
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # 5. Resolve persisted RBAC state and generate new access + refresh pair.
    try:
        role, permissions = user_rbac_claims(user)
    except ValueError as exc:
        await db.commit()
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="User authorization state is unavailable",
        ) from exc
    new_access = create_access_token(
        str(user.id),
        subscription_tier=user.subscription_tier,
        role=role,
        permissions=permissions,
    )
    new_raw_refresh, new_hashed_refresh = create_refresh_token(str(user.id))

    # 6. Store new refresh token hash
    new_record = RefreshToken(
        user_id=user.id,
        token_hash=new_hashed_refresh,
        expires_at=now + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS),
        revoked=False,
    )
    db.add(new_record)
    await db.commit()

    return {
        "access_token": new_access,
        "refresh_token": new_raw_refresh,
    }


@router.post("/auth/logout", status_code=status.HTTP_200_OK)
async def logout_endpoint(
    payload: LogoutRequest,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    """Revoke refresh token on logout."""
    token = payload.refresh_token.strip()
    client_ip = request.client.host if request.client else "unknown"
    await enforce_rate_limit(
        db,
        key=hashed_rate_key("logout-ip", client_ip),
        limit=30,
        window_seconds=60,
    )
    incoming_hash = hash_token(token)

    await db.execute(
        update(RefreshToken)
        .where(RefreshToken.token_hash == incoming_hash)
        .values(revoked=True)
    )
    await db.commit()

    return {"message": "Logged out"}
