from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_db
from ..models.farmer import Farmer
from ..schemas.farmer import FarmerRead, FarmerUpdate
from ..utils.auth import verify_token

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_current_farmer(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)) -> Farmer:
    payload = verify_token(token)
    farmer_id = payload.get("sub")
    result = await db.execute(select(Farmer).where(Farmer.id == farmer_id))
    farmer = result.scalar_one_or_none()
    if not farmer:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    return farmer


@router.get("/me", response_model=FarmerRead)
async def get_my_profile(current_farmer: Farmer = Depends(get_current_farmer)):
    return current_farmer


@router.put("/me", response_model=FarmerRead)
async def update_my_profile(
    update: FarmerUpdate,
    current_farmer: Farmer = Depends(get_current_farmer),
    db: AsyncSession = Depends(get_db)
):
    for field, value in update.model_dump(exclude_none=True).items():
        setattr(current_farmer, field, value)
    await db.commit()
    await db.refresh(current_farmer)
    return current_farmer
