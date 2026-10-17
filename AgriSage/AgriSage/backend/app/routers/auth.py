from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from passlib.context import CryptContext
from datetime import timedelta
from ..database import get_db
from ..models.farmer import Farmer
from ..schemas.auth import RegisterRequest, TokenResponse
from ..utils.auth import create_access_token
from ..config import settings
import uuid

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check if phone already registered
    result = await db.execute(select(Farmer).where(Farmer.phone == request.phone))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Phone number already registered")

    hashed_password = pwd_context.hash(request.password)
    farmer = Farmer(
        id=str(uuid.uuid4()),
        phone=request.phone,
        name=request.name,
        hashed_password=hashed_password,
        village=request.village,
        district=request.district,
        preferred_language=request.preferred_language,
        latitude=request.latitude,
        longitude=request.longitude,
    )
    db.add(farmer)
    await db.commit()
    await db.refresh(farmer)

    token = create_access_token(
        {"sub": farmer.id, "phone": farmer.phone},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return TokenResponse(access_token=token, farmer_id=farmer.id)


@router.post("/token", response_model=TokenResponse)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Farmer).where(Farmer.phone == form_data.username))
    farmer = result.scalar_one_or_none()
    if not farmer or not pwd_context.verify(form_data.password, farmer.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect phone or password")

    token = create_access_token(
        {"sub": farmer.id, "phone": farmer.phone},
        timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    return TokenResponse(access_token=token, farmer_id=farmer.id)
