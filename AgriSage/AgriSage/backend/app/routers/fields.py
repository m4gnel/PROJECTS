from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
import uuid
from ..database import get_db
from ..models.field import Field
from ..models.crop import CropRecord
from ..schemas.field import FieldCreate, FieldRead, ActiveCrop
from .farmers import get_current_farmer
from ..models.farmer import Farmer
from datetime import datetime, timezone, timedelta

router = APIRouter()


def make_tz():
    return timezone(timedelta(hours=5, minutes=30))


async def field_to_read(field: Field, db: AsyncSession) -> FieldRead:
    active_crop = None
    result = await db.execute(
        select(CropRecord).where(CropRecord.field_id == field.id, CropRecord.is_active == True)
    )
    crop = result.scalar_one_or_none()
    if crop:
        active_crop = ActiveCrop(
            id=crop.id,
            crop_name=crop.crop_name,
            variety=crop.variety,
            sowing_date=str(crop.sowing_date),
            growth_stage=crop.growth_stage,
            expected_harvest_date=str(crop.expected_harvest_date) if crop.expected_harvest_date else None,
        )
    return FieldRead(
        id=field.id,
        farmer_id=field.farmer_id,
        name=field.name,
        area_sq_m=field.area_sq_m,
        latitude=field.latitude,
        longitude=field.longitude,
        soil_type=field.soil_type,
        irrigation_type=field.irrigation_type,
        last_ndvi=field.last_ndvi,
        active_crop=active_crop,
        created_at=field.created_at,
        updated_at=field.updated_at,
    )


@router.get("/", response_model=List[FieldRead])
async def get_fields(current_farmer: Farmer = Depends(get_current_farmer), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Field).where(Field.farmer_id == current_farmer.id))
    fields = result.scalars().all()
    return [await field_to_read(f, db) for f in fields]


@router.post("/", response_model=FieldRead, status_code=status.HTTP_201_CREATED)
async def create_field(
    req: FieldCreate,
    current_farmer: Farmer = Depends(get_current_farmer),
    db: AsyncSession = Depends(get_db)
):
    field = Field(
        id=str(uuid.uuid4()),
        farmer_id=current_farmer.id,
        name=req.name,
        area_sq_m=req.area_sq_m,
        latitude=req.latitude,
        longitude=req.longitude,
        soil_type=req.soil_type,
        irrigation_type=req.irrigation_type,
    )
    db.add(field)
    await db.flush()

    if req.crop_name and req.sowing_date:
        from datetime import date
        crop = CropRecord(
            id=str(uuid.uuid4()),
            field_id=field.id,
            crop_name=req.crop_name,
            variety=req.crop_variety,
            sowing_date=date.fromisoformat(req.sowing_date),
            is_active=True,
        )
        db.add(crop)

    await db.commit()
    await db.refresh(field)
    return await field_to_read(field, db)


@router.delete("/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_field(
    field_id: str,
    current_farmer: Farmer = Depends(get_current_farmer),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(Field).where(Field.id == field_id, Field.farmer_id == current_farmer.id))
    field = result.scalar_one_or_none()
    if not field:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Field not found")
    await db.delete(field)
    await db.commit()
