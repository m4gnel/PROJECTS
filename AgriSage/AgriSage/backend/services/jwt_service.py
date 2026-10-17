import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, Tuple
from uuid import uuid4
from jose import jwt, JWTError
from passlib.context import CryptContext

from backend.config import settings

pwd_context = CryptContext(schemes=["pbkdf2_sha256", "bcrypt"], deprecated="auto")


def hash_otp(otp: str) -> str:
    """Hash OTP using passlib bcrypt with 10 rounds."""
    return pwd_context.hash(otp)


def verify_otp(plain_otp: str, hashed_otp: str) -> bool:
    """Verify plaintext OTP against bcrypt hash."""
    return pwd_context.verify(plain_otp, hashed_otp)


def hash_token(token: str) -> str:
    """Hash refresh token with SHA-256."""
    return hashlib.sha256(token.encode('utf-8')).hexdigest()


def create_access_token(user_id: str, subscription_tier: str = "free") -> str:
    """Create a signed HS256 JWT access token with 15-minute expiry."""
    now = datetime.now(timezone.utc)
    expire = now + timedelta(minutes=15)
    
    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "tier": subscription_tier,
        "exp": int(expire.timestamp()),
        "iat": int(now.timestamp()),
        "jti": str(uuid4()),
    }
    return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")


def create_refresh_token(user_id: str) -> Tuple[str, str]:
    """
    Generate a random raw refresh token and its SHA-256 hash.
    Returns (raw_token, hashed_token).
    """
    raw_token = secrets.token_urlsafe(64)
    hashed_token = hash_token(raw_token)
    return raw_token, hashed_token


def verify_access_token(token: str) -> Dict[str, Any]:
    """Decode and return JWT access token payload."""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError as e:
        raise ValueError(f"Invalid or expired token: {str(e)}")
