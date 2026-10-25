from typing import Dict, Any, Optional
from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from backend.database import get_db
from backend.dependencies import require_expert_access
from backend.services.audit import AuditLogUnavailable, record_audit_event

router = APIRouter(prefix="/expert", tags=["expert"])


class ReviewSubmission(BaseModel):
    verdict: str  # correct / partially_correct / incorrect / insufficient_data
    corrected_diagnosis: Optional[str] = None
    notes: Optional[str] = None


@router.get("/queue")
async def get_expert_queue(
    request: Request,
    user: Dict[str, Any] = Depends(require_expert_access),
    db: AsyncSession = Depends(get_db),
):
    sql = text("""
    SELECT a.id as advisory_id, a.created_at, a.confidence_state,
           cc.crop, f.district
    FROM advisories a
    JOIN observations o ON a.observation_id = o.id
    JOIN crop_cycles cc ON o.crop_cycle_id = cc.id
    JOIN fields fld ON cc.field_id = fld.id
    JOIN farms f ON fld.farm_id = f.id
    LEFT JOIN expert_reviews er ON a.id = er.advisory_id
    WHERE er.id IS NULL
    ORDER BY a.created_at DESC
    LIMIT 50
    """)
    res = await db.execute(sql)
    rows = res.fetchall()

    queue = []
    for r in rows:
        queue.append({
            "advisory_id": str(r.advisory_id),
            "created_at": str(r.created_at),
            "confidence_state": r.confidence_state,
            "crop": r.crop,
            "district": r.district
        })
    try:
        await record_audit_event(
            db,
            user_id=user["sub"],
            event_type="expert.queue.read",
            event_data={"result_count": len(queue), "read_only": True},
            ip_address=request.client.host if request.client else None,
        )
    except AuditLogUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Audit storage is unavailable",
        ) from exc

    return {"queue": queue, "total_pending": len(queue)}


@router.post("/reviews/{advisory_id}")
async def submit_expert_review(
    advisory_id: str,
    body: ReviewSubmission,
    request: Request,
    user: Dict[str, Any] = Depends(require_expert_access),
    db: AsyncSession = Depends(get_db),
):
    sql = text("""
    INSERT INTO expert_reviews (
        id, advisory_id, expert_id, verdict, corrected_diagnosis, notes
    ) VALUES (
        gen_random_uuid(), :advisory_id, :expert_id, :verdict, :corrected_diagnosis, :notes
    ) RETURNING id
    """)
    res = await db.execute(sql, {
        "advisory_id": advisory_id,
        "expert_id": user["sub"],
        "verdict": body.verdict,
        "corrected_diagnosis": body.corrected_diagnosis,
        "notes": body.notes
    })
    review_id = res.scalar()
    try:
        await record_audit_event(
            db,
            user_id=user["sub"],
            event_type="expert.review.create",
            event_data={"advisory_id": advisory_id, "verdict": body.verdict},
            ip_address=request.client.host if request.client else None,
        )
    except AuditLogUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Audit storage is unavailable",
        ) from exc

    return {"review_id": str(review_id), "message": "Review submitted successfully"}
