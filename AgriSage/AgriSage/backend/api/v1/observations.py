import uuid
from typing import List, Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.dependencies import require_auth

try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

router = APIRouter(tags=["Observations"])



@router.post("/observations", status_code=status.HTTP_201_CREATED)
async def create_observation(
    crop_cycle_id: str = Form(...),
    description: Optional[str] = Form(None),
    images: List[UploadFile] = File(...),
    auth: Dict[str, Any] = Depends(require_auth),
    db: AsyncSession = Depends(get_db),
):
    """
    Create a new observation with images for a crop cycle.
    Enforces image quality checks, EXIF stripping, R2 upload, and RLS ownership.
    """
    user_id = auth.get("sub")
    await db.execute(text(f"SET LOCAL app.current_user_id = '{user_id}'"))

    # Validate image count
    if len(images) > 5:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 5 images allowed per observation"
        )

    # Validate crop_cycle ownership
    try:
        cc_uuid = uuid.UUID(crop_cycle_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Crop cycle not found")

    stmt = (
        select(CropCycle)
        .join(Field, CropCycle.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(CropCycle.id == cc_uuid, Farm.user_id == uuid.UUID(user_id))
    )
    res = await db.execute(stmt)
    crop_cycle = res.scalars().first()
    if not crop_cycle:
        raise HTTPException(status_code=404, detail="Crop cycle not found")

    # Truncate description if needed
    clean_desc = description.strip()[:2000] if description else None

    # Create Observation Record
    obs_id = uuid.uuid4()
    obs_record = Observation(
        id=obs_id,
        crop_cycle_id=cc_uuid,
        problem_description=clean_desc,
    )
    db.add(obs_record)

    image_ids = []
    for file in images:
        file_bytes = await file.read()
        try:
            processed_bytes = process_uploaded_image(file_bytes)
        except ValueError as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image validation failed for {file.filename}: {str(e)}"
            )

        img_uuid = uuid.uuid4()
        r2_key = f"observations/{user_id}/{obs_id}/{img_uuid}.jpg"

        # Upload to R2
        r2_url = await r2_storage.upload_image(processed_bytes, r2_key)

        img_record = Image(
            id=img_uuid,
            observation_id=obs_id,
            r2_key=r2_key,
            mime_type="image/jpeg",
            file_size_bytes=len(processed_bytes),
            quality_score=1.0,
        )
        db.add(img_record)
        image_ids.append(str(img_uuid))

    await db.commit()

    return {
        "observation_id": str(obs_id),
        "image_ids": image_ids,
    }
