from typing import List, Dict, Any
import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field as PydanticField
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models.db import Farm, Field, CropCycle
from backend.models.schemas.farms import (
    FarmCreate, FarmResponse,
    FieldCreate, FieldResponse,
    CropCycleCreate, CropCycleResponse
)

router = APIRouter(tags=["Farms & Fields"])


class MobileFieldCreateRequest(BaseModel):
    """Request shape emitted by the Android client.

    The authenticated user's farm is selected server-side; no farmer/user id is
    accepted from the client.
    """

    name: str = PydanticField(..., min_length=1, max_length=100)
    area_sq_m: float = PydanticField(..., gt=0, lt=50_000_000)
    latitude: float = PydanticField(..., ge=6.0, le=38.0)
    longitude: float = PydanticField(..., ge=68.0, le=97.5)
    soil_type: str | None = PydanticField(default=None, max_length=50)
    irrigation_type: str | None = PydanticField(default=None, max_length=30)
    crop_name: str | None = PydanticField(default=None, max_length=50)
    crop_variety: str | None = PydanticField(default=None, max_length=100)
    sowing_date: str | None = None


def _mobile_field_response(field: Field, farmer_id: str) -> dict[str, Any]:
    area_ha = float(field.area_ha) if field.area_ha is not None else 0.0
    return {
        "id": str(field.id),
        "farmer_id": farmer_id,
        "name": field.name or "",
        "area_sq_m": area_ha * 10_000,
        "latitude": float(field.latitude) if field.latitude is not None else 0.0,
        "longitude": float(field.longitude) if field.longitude is not None else 0.0,
        "soil_type": field.soil_type,
        "irrigation_type": field.irrigation,
        "last_ndvi": None,
        "active_crop": None,
        "created_at": field.created_at,
        "updated_at": field.created_at,
    }


# ==============================================================================
# FARMS ENDPOINTS
# ==============================================================================

@router.post("/farms", response_model=FarmResponse, status_code=status.HTTP_201_CREATED)
async def create_farm(
    payload: FarmCreate,
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new farm for the authenticated user."""
    user_id = auth.get("sub")
    await db.execute(
        text("SELECT set_config('app.current_user_id', :user_id, true)"),
        {"user_id": str(user_id)},
    )

    farm = Farm(
        user_id=uuid.UUID(user_id),
        name=payload.name,
        district=payload.district,
        state=payload.state,
        area_ha=payload.area_ha,
    )
    db.add(farm)
    await db.commit()
    await db.refresh(farm)
    return FarmResponse.model_validate(farm)


@router.get("/farms", response_model=List[FarmResponse])
async def list_farms(
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all farms owned by the authenticated user."""
    user_id = auth.get("sub")
    await db.execute(
        text("SELECT set_config('app.current_user_id', :user_id, true)"),
        {"user_id": str(user_id)},
    )

    stmt = select(Farm).where(Farm.user_id == uuid.UUID(user_id)).order_by(Farm.created_at.desc())
    result = await db.execute(stmt)
    farms = result.scalars().all()
    return [FarmResponse.model_validate(f) for f in farms]


@router.get("/farms/{farm_id}", response_model=FarmResponse)
async def get_farm(
    farm_id: str,
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get farm details by ID. Returns 404 if not found or unauthorized."""
    user_id = auth.get("sub")
    try:
        f_uuid = uuid.UUID(farm_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Farm not found") from exc

    await db.execute(
        text("SELECT set_config('app.current_user_id', :user_id, true)"),
        {"user_id": str(user_id)},
    )
    stmt = select(Farm).where(Farm.id == f_uuid, Farm.user_id == uuid.UUID(user_id))
    result = await db.execute(stmt)
    farm = result.scalars().first()

    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    return FarmResponse.model_validate(farm)



@router.put("/farms/{farm_id}", response_model=FarmResponse)
async def update_farm(
    farm_id: str,
    payload: FarmCreate,
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Update farm details by ID. Returns 404 if not found or unauthorized."""
    user_id = auth.get("sub")
    await db.execute(
        text("SELECT set_config('app.current_user_id', :user_id, true)"),
        {"user_id": str(user_id)},
    )

    try:
        f_uuid = uuid.UUID(farm_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Farm not found")

    stmt = select(Farm).where(Farm.id == f_uuid, Farm.user_id == uuid.UUID(user_id))
    result = await db.execute(stmt)
    farm = result.scalars().first()

    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    farm.name = payload.name
    farm.district = payload.district
    farm.state = payload.state
    farm.area_ha = payload.area_ha

    await db.commit()
    await db.refresh(farm)
    return FarmResponse.model_validate(farm)


@router.delete("/farms/{farm_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_farm(
    farm_id: str,
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete farm by ID. Returns 404 if not found or unauthorized."""
    user_id = auth.get("sub")
    await db.execute(
        text("SELECT set_config('app.current_user_id', :user_id, true)"),
        {"user_id": str(user_id)},
    )

    try:
        f_uuid = uuid.UUID(farm_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Farm not found")

    stmt = select(Farm).where(Farm.id == f_uuid, Farm.user_id == uuid.UUID(user_id))
    result = await db.execute(stmt)
    farm = result.scalars().first()

    if not farm:
        raise HTTPException(status_code=404, detail="Farm not found")

    farm.is_active = False
    await db.commit()
    return None


# ==============================================================================
# FIELDS ENDPOINTS
# ==============================================================================

@router.post("/farms/{farm_id}/fields", response_model=FieldResponse, status_code=status.HTTP_201_CREATED)
async def create_field(
    farm_id: str,
    payload: FieldCreate,
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a field inside a specific farm."""
    user_id = auth.get("sub")
    await db.execute(
        text("SELECT set_config('app.current_user_id', :user_id, true)"),
        {"user_id": str(user_id)},
    )

    try:
        f_uuid = uuid.UUID(farm_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Farm not found")

    # Verify farm ownership
    farm_stmt = select(Farm).where(Farm.id == f_uuid, Farm.user_id == uuid.UUID(user_id))
    farm_res = await db.execute(farm_stmt)
    if not farm_res.scalars().first():
        raise HTTPException(status_code=404, detail="Farm not found")

    field = Field(
        farm_id=f_uuid,
        name=payload.name,
        area_ha=payload.area_ha,
        slope=payload.slope,
        irrigation=payload.irrigation,
        soil_type=payload.soil_type,
    )
    db.add(field)
    await db.commit()
    await db.refresh(field)
    return FieldResponse.model_validate(field)


@router.get("/farms/{farm_id}/fields", response_model=List[FieldResponse])
async def list_fields(
    farm_id: str,
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all fields inside a specific farm."""
    user_id = auth.get("sub")
    await db.execute(
        text("SELECT set_config('app.current_user_id', :user_id, true)"),
        {"user_id": str(user_id)},
    )

    try:
        f_uuid = uuid.UUID(farm_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Farm not found")

    farm_stmt = select(Farm).where(Farm.id == f_uuid, Farm.user_id == uuid.UUID(user_id))
    if not (await db.execute(farm_stmt)).scalars().first():
        raise HTTPException(status_code=404, detail="Farm not found")

    stmt = select(Field).where(Field.farm_id == f_uuid).order_by(Field.created_at.desc())
    fields = (await db.execute(stmt)).scalars().all()
    return [FieldResponse.model_validate(f) for f in fields]


# ==============================================================================
# CROP CYCLES ENDPOINTS
# ==============================================================================

@router.post("/crop-cycles", response_model=CropCycleResponse, status_code=status.HTTP_201_CREATED)
async def create_crop_cycle(
    payload: CropCycleCreate,
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a new crop cycle for a field owned by the authenticated user."""
    user_id = auth.get("sub")
    await db.execute(
        text("SELECT set_config('app.current_user_id', :user_id, true)"),
        {"user_id": str(user_id)},
    )

    try:
        fld_uuid = uuid.UUID(payload.field_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Field not found")

    # Verify field ownership via farm join
    field_stmt = (
        select(Field)
        .join(Farm, Field.farm_id == Farm.id)
        .where(Field.id == fld_uuid, Farm.user_id == uuid.UUID(user_id))
    )
    if not (await db.execute(field_stmt)).scalars().first():
        raise HTTPException(status_code=404, detail="Field not found")

    cycle = CropCycle(
        field_id=fld_uuid,
        crop=payload.crop,
        cultivar=payload.cultivar,
        season=payload.season,
        planting_date=payload.planting_date,
        expected_harvest=payload.expected_harvest,
        actual_harvest=payload.actual_harvest,
        status=payload.status,
        notes=payload.notes,
    )
    db.add(cycle)
    await db.commit()
    await db.refresh(cycle)
    return CropCycleResponse.model_validate(cycle)


@router.get("/crop-cycles", response_model=List[CropCycleResponse])
async def list_crop_cycles(
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """List all crop cycles owned by the authenticated user across all fields."""
    user_id = auth.get("sub")
    await db.execute(
        text("SELECT set_config('app.current_user_id', :user_id, true)"),
        {"user_id": str(user_id)},
    )

    stmt = (
        select(CropCycle)
        .join(Field, CropCycle.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(Farm.user_id == uuid.UUID(user_id))
        .order_by(CropCycle.created_at.desc())
    )
    cycles = (await db.execute(stmt)).scalars().all()
    return [CropCycleResponse.model_validate(c) for c in cycles]


# ---------------------------------------------------------------------------
# Android-compatible flat field endpoints
# ---------------------------------------------------------------------------

@router.get("/fields/")
async def list_mobile_fields(
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> List[Dict[str, Any]]:
    """Return fields in the Android response shape, scoped by JWT subject."""

    user_id = uuid.UUID(str(auth["sub"]))
    result = await db.execute(
        select(Field, Farm)
        .join(Farm, Field.farm_id == Farm.id)
        .where(Farm.user_id == user_id)
        .order_by(Field.created_at.desc())
    )
    return [_mobile_field_response(field, str(user_id)) for field, _farm in result.all()]


@router.post("/fields/", status_code=status.HTTP_201_CREATED)
async def create_mobile_field(
    payload: MobileFieldCreateRequest,
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Create a field for the authenticated user without trusting a farmer id."""

    user_id = uuid.UUID(str(auth["sub"]))
    user = auth["user"]
    farm_result = await db.execute(
        select(Farm).where(Farm.user_id == user_id).order_by(Farm.created_at.asc())
    )
    farm = farm_result.scalars().first()
    if farm is None:
        farm = Farm(
            user_id=user_id,
            name="My Farm",
            district=user.district,
            state=user.state or "India",
            area_ha=payload.area_sq_m / 10_000,
        )
        db.add(farm)
        await db.flush()

    field = Field(
        farm_id=farm.id,
        name=payload.name.strip(),
        area_ha=payload.area_sq_m / 10_000,
        irrigation=payload.irrigation_type,
        soil_type=payload.soil_type,
        latitude=payload.latitude,
        longitude=payload.longitude,
    )
    db.add(field)
    await db.commit()
    await db.refresh(field)
    return _mobile_field_response(field, str(user_id))


@router.delete("/fields/{field_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_mobile_field(
    field_id: str,
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> None:
    """Delete only a field belonging to the authenticated user's farm."""

    try:
        field_uuid = uuid.UUID(field_id)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail="Field not found") from exc
    user_id = uuid.UUID(str(auth["sub"]))
    result = await db.execute(
        select(Field)
        .join(Farm, Field.farm_id == Farm.id)
        .where(Field.id == field_uuid, Farm.user_id == user_id)
    )
    field = result.scalars().first()
    if field is None:
        raise HTTPException(status_code=404, detail="Field not found")
    await db.delete(field)
    await db.commit()
