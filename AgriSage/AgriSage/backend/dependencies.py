from typing import Dict, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError, jwt

from backend.config import settings
from backend.database import get_db

security_scheme = HTTPBearer(auto_error=True)


async def require_auth(
    credentials: HTTPAuthorizationCredentials = Depends(security_scheme),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """
    FastAPI dependency enforcing JWT authentication.
    Decodes the Bearer token, checks expiration, sets the PostgreSQL RLS
    session variable app.current_user_id, and returns the payload dict.
    """
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired token",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Set PostgreSQL session variable for Row-Level Security (RLS)
        try:
            await db.execute(text(f"SET LOCAL app.current_user_id = '{user_id}'"))
        except Exception:
            pass

        return payload


    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )


# Alias for backward compatibility across routers
get_current_user = require_auth

