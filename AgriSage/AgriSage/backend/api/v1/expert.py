from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from backend.database import AsyncSessionLocal
from backend.dependencies import get_current_user

router = APIRouter(prefix="/expert", tags=["expert"])


class ReviewSubmission(BaseModel):
    verdict: str  # correct / partially_correct / incorrect / insufficient_data
    corrected_diagnosis: Optional[str] = None
    notes: Optional[str] = None


@router.get("/queue")
async def get_expert_queue(user: Dict[str, Any] = Depends(get_current_user)):
    if user.get("subscription_tier") != "expert" and user.get("tier") != "expert":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to tier='expert' users only."
        )

    async with AsyncSessionLocal() as session:
        sql = text("""
        SELECT a.id as advisory_id, a.created_at, a.confidence_state,
               o.crop, f.district
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
        res = await session.execute(sql)
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
    return {"queue": queue, "total_pending": len(queue)}


@router.post("/reviews/{advisory_id}")
async def submit_expert_review(
    advisory_id: str,
    body: ReviewSubmission,
    user: Dict[str, Any] = Depends(get_current_user)
):
    if user.get("subscription_tier") != "expert" and user.get("tier") != "expert":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access restricted to tier='expert' users only."
        )

    async with AsyncSessionLocal() as session:
        sql = text("""
        INSERT INTO expert_reviews (
            id, advisory_id, expert_user_id, verdict, corrected_diagnosis, notes
        ) VALUES (
            gen_random_uuid(), :advisory_id, :expert_id, :verdict, :corrected_diagnosis, :notes
        ) RETURNING id
        """)
        res = await session.execute(sql, {
            "advisory_id": advisory_id,
            "expert_id": user["sub"],
            "verdict": body.verdict,
            "corrected_diagnosis": body.corrected_diagnosis,
            "notes": body.notes
        })
        review_id = res.scalar()
        await session.commit()

    return {"review_id": str(review_id), "message": "Review submitted successfully"}
