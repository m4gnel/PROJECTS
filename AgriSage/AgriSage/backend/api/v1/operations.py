"""Read-only operations data for authenticated staff roles."""

from datetime import datetime, timezone
from typing import Any, Dict, List

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from backend.config import settings
from backend.database import get_db
from backend.dependencies import require_access
from backend.rbac import UserRole
from backend.services.audit import AuditLogUnavailable, record_audit_event


router = APIRouter(prefix="/operations", tags=["operations"])

STAFF_ACCESS = {
    "roles": (UserRole.EMPLOYEE, UserRole.OFFICER),
}


def _isoformat(value: Any) -> str | None:
    if value is None:
        return None
    if hasattr(value, "isoformat"):
        return value.isoformat()
    return str(value)


async def _audit(
    db: AsyncSession,
    principal: Dict[str, Any],
    request: Request,
    event_type: str,
    event_data: Dict[str, Any],
) -> None:
    try:
        await record_audit_event(
            db,
            user_id=principal["sub"],
            event_type=event_type,
            event_data=event_data,
            ip_address=request.client.host if request.client else None,
        )
    except AuditLogUnavailable as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Audit storage is unavailable",
        ) from exc


@router.get("/summary")
async def get_operations_summary(
    request: Request,
    principal: Dict[str, Any] = Depends(
        require_access(
            roles=STAFF_ACCESS["roles"],
            permissions=("operations:summary:read",),
        )
    ),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Return aggregate advisory triage data for employees and officers."""

    try:
        result = await db.execute(
            text(
                """
                SELECT
                    COUNT(*)::INTEGER AS active_advisories,
                    COUNT(*) FILTER (
                        WHERE confidence_state IN (
                            'UNCERTAIN', 'INSUFFICIENT_DATA', 'CONFLICTING_EVIDENCE'
                        )
                    )::INTEGER AS needs_review,
                    COUNT(*) FILTER (
                        WHERE confidence_score >= 0.70
                    )::INTEGER AS high_confidence,
                    COALESCE(AVG(confidence_score), 0)::NUMERIC(5, 4) AS average_confidence
                FROM advisories
                """
            )
        )
        row = result.mappings().one()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Operations data is unavailable",
        ) from exc

    response = {
        "active_advisories": int(row["active_advisories"] or 0),
        "needs_review": int(row["needs_review"] or 0),
        "high_confidence": int(row["high_confidence"] or 0),
        "average_confidence": float(row["average_confidence"] or 0),
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "read_only": True,
    }
    await _audit(db, principal, request, "operations.summary.read", {"read_only": True})
    return response


@router.get("/queue")
async def get_operations_queue(
    request: Request,
    limit: int = Query(50, ge=1, le=100),
    principal: Dict[str, Any] = Depends(
        require_access(
            roles=STAFF_ACCESS["roles"],
            permissions=("operations:queue:read",),
        )
    ),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Return the pending advisory review queue without mutation controls."""

    try:
        result = await db.execute(
            text(
                """
                SELECT a.id, a.created_at, a.confidence_state,
                       a.confidence_score, a.safe_to_act,
                       COALESCE(u.name, 'Unassigned farmer') AS farmer_name,
                       u.phone AS farmer_phone,
                       f.name AS farm_name,
                       f.district AS district,
                       cc.crop AS crop,
                       CASE
                           WHEN a.confidence_state IN (
                               'UNCERTAIN', 'INSUFFICIENT_DATA', 'CONFLICTING_EVIDENCE'
                           ) OR a.safe_to_act = false THEN 'ESCALATED'
                           ELSE 'PENDING_REVIEW'
                       END AS triage_status
                FROM advisories AS a
                JOIN observations AS o ON o.id = a.observation_id
                JOIN crop_cycles AS cc ON cc.id = o.crop_cycle_id
                JOIN fields AS fld ON fld.id = cc.field_id
                JOIN farms AS f ON f.id = fld.farm_id
                JOIN users AS u ON u.id = f.user_id
                LEFT JOIN expert_reviews AS er ON er.advisory_id = a.id
                WHERE er.id IS NULL
                ORDER BY a.created_at DESC
                LIMIT :limit
                """
            ),
            {"limit": limit},
        )
        rows = result.mappings().all()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Operations queue is unavailable",
        ) from exc

    items: List[Dict[str, Any]] = [
        {
            "advisory_id": str(row["id"]),
            "created_at": _isoformat(row["created_at"]),
            "confidence_state": row["confidence_state"],
            "confidence_score": float(row["confidence_score"])
            if row["confidence_score"] is not None
            else None,
            "safe_to_act": bool(row["safe_to_act"]),
            "triage_status": row["triage_status"],
            "farmer_name": row["farmer_name"],
            "farmer_phone": row["farmer_phone"],
            "farm_name": row["farm_name"],
            "district": row["district"],
            "crop": row["crop"],
        }
        for row in rows
    ]
    await _audit(
        db,
        principal,
        request,
        "operations.queue.read",
        {"limit": limit, "result_count": len(items), "read_only": True},
    )
    return {"items": items, "total_pending": len(items), "read_only": True}


@router.get("/service-boundary")
async def get_service_boundary(
    request: Request,
    principal: Dict[str, Any] = Depends(
        require_access(
            roles=STAFF_ACCESS["roles"],
            permissions=("operations:service-boundary:read",),
        )
    ),
    db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
    """Describe the staff API's explicit read-only service boundaries."""

    boundaries = [
        {
            "name": "advisory_snapshot",
            "access": "read-only",
            "source": "database",
            "writes_enabled": False,
        },
        {
            "name": "expert_review_workflow",
            "access": "separate expert authorization",
            "source": "database",
            "writes_enabled": False,
        },
        {
            "name": "service_health",
            "access": "read-only",
            "source": "backend configuration",
            "writes_enabled": False,
        },
    ]
    await _audit(db, principal, request, "operations.service_boundary.read", {"read_only": True})
    return {
        "service": "agrisage-backend",
        "environment": settings.ENVIRONMENT,
        "read_only": True,
        "boundaries": boundaries,
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
