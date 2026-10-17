from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from ..database import get_db
from ..models.alert import Alert
from ..schemas.alert import AlertRead, MarkReadRequest
from .farmers import get_current_farmer
from ..models.farmer import Farmer

router = APIRouter()


@router.get("/", response_model=List[AlertRead])
async def get_alerts(
    unread_only: bool = Query(False),
    current_farmer: Farmer = Depends(get_current_farmer),
    db: AsyncSession = Depends(get_db)
):
    query = select(Alert).where(Alert.farmer_id == current_farmer.id)
    if unread_only:
        query = query.where(Alert.is_read == False)
    result = await db.execute(query.order_by(Alert.created_at.desc()))
    return result.scalars().all()


@router.post("/mark-read")
async def mark_alerts_read(
    request: MarkReadRequest,
    current_farmer: Farmer = Depends(get_current_farmer),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(Alert).where(Alert.id.in_(request.alert_ids), Alert.farmer_id == current_farmer.id)
    )
    alerts = result.scalars().all()
    count = 0
    for a in alerts:
        a.is_read = True
        count += 1
    await db.commit()
    return {"marked_count": count}
