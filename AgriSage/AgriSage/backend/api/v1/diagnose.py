import uuid
import time
import json
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
from backend.config import settings
from backend.database import get_db
from backend.dependencies import get_current_user
from backend.models.db.farms import Observation, CropCycle, Field, Farm, Image
from backend.agents.orchestrator import run_advisory_pipeline
from backend.agents.state import AgriSAGEState

try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

router = APIRouter(tags=["Diagnosis"])


class DiagnoseRequest(BaseModel):
    observation_id: str


@router.post("/diagnose", status_code=status.HTTP_200_OK)
async def run_diagnose(
    payload: DiagnoseRequest,
    auth: Dict[str, Any] = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Run full 14-agent diagnostic pipeline for observation."""
    user_id = auth.get("sub")
    await db.execute(
        text("SELECT set_config('app.current_user_id', :user_id, true)"),
        {"user_id": str(user_id)},
    )

    try:
        obs_uuid = uuid.UUID(payload.observation_id)
    except ValueError:
        raise HTTPException(status_code=404, detail="Observation not found")

    # Verify observation ownership via RLS
    stmt = (
        select(Observation, CropCycle, Farm)
        .join(CropCycle, Observation.crop_cycle_id == CropCycle.id)
        .join(Field, CropCycle.field_id == Field.id)
        .join(Farm, Field.farm_id == Farm.id)
        .where(Observation.id == obs_uuid, Farm.user_id == uuid.UUID(user_id))
    )
    res = await db.execute(stmt)
    row = res.first()
    if not row:
        raise HTTPException(status_code=404, detail="Observation not found")

    obs, crop_cycle, farm = row[0], row[1], row[2]
    image_result = await db.execute(select(Image).where(Image.observation_id == obs.id))
    image_records = image_result.scalars().all()

    # Build initial AgriSAGEState
    start_ms = int(time.time() * 1000)
    initial_state: AgriSAGEState = {
        "observation_id": str(obs.id),
        "user_id": str(user_id),
        "images": [{"key": image.r2_key} for image in image_records],
        "farm_state": {
            "crop": crop_cycle.crop,
            "planting_date": str(crop_cycle.planting_date),
            "district": farm.district or "",
            "state": farm.state or "India",
            "location_lat": float(farm.location_lat) if farm.location_lat else 22.5937,
            "location_lon": float(farm.location_lon) if farm.location_lon else 78.9629,
        },
        "vision_result": None,
        "weather_result": None,
        "crop_stage_result": None,
        "knowledge_result": None,
        "critic_result": None,
        "scheme_result": None,
        "simulation_result": None,
        "decision_result": None,
        "advisory": None,
        "run_simulation": True,
        "confidence_state": None,
        "warnings": [],
        "errors": [],
        "pipeline_start_ms": start_ms,
        "generation_ms": None,
        "language": "ml",
        "crop": crop_cycle.crop,
    }

    final_state = await run_advisory_pipeline(initial_state, thread_id=str(obs.id))
    gen_ms = final_state.get("generation_ms") or (int(time.time() * 1000) - start_ms)

    adv = final_state.get("advisory") or {}
    critic = final_state.get("critic_result") or {}
    vision = final_state.get("vision_result") or {}
    dec = final_state.get("decision_result") or {}
    has_image_evidence = bool(image_records)

    advisory_id = str(uuid.uuid4())

    # Only return modelled scenarios produced by the pipeline.  A missing
    # image/evidence set must not become a fabricated yield or treatment plan.
    scenarios = dec.get("scored_scenarios", [])
    for s in scenarios:
        s["modelled_estimate"] = bool(s.get("modelled_estimate", False))

    response_data = {
        "advisory_id": advisory_id,
        "observation_id": str(obs.id),
        "confidence_state": (
            final_state.get("confidence_state", "INSUFFICIENT_DATA")
            if has_image_evidence
            else "INSUFFICIENT_DATA"
        ),
        "confidence_score": critic.get("confidence_score", 0.0) if has_image_evidence else 0.0,
        "diagnosis": {
            "label": vision.get("label", "out_of_distribution"),
            "common_name": {"ml": vision.get("ml_name", "Diagnosis unavailable"), "en": vision.get("common_name", "Diagnosis unavailable")},
            "confidence_score": vision.get("confidence_score", 0.0),
            "severity": vision.get("severity", "unknown"),
            "affected_area_pct": vision.get("affected_area_pct", 0.0),
        },
        "risk": {
            "level": "UNKNOWN",
            "horizon_days": 0,
            "factors": []
        },
        "scenarios": scenarios,
        "recommended_scenario": dec.get("recommended_scenario"),
        "recommended_action": adv.get("recommended_action", {
            "what": "Inspect plants",
            "when": "Today",
            "how": "Visual check",
            "spray_window": None,
            "cost_estimate_inr": None,
        }),
        "evidence": {
            "items": adv.get("evidence_summary", []),
            "contradictions": critic.get("conflicts", []),
            "missing_data": final_state.get("warnings", [])
        },
        "what_would_change_this": adv.get(
            "what_would_change_this",
            ["A valid field image and current provider-backed observations"],
        ),
        "safe_to_act": bool(critic.get("safe_to_act", False)) and has_image_evidence,
        "scheme_matches": [],
        "sources": [],
        "model_version": settings.MODEL_VERSION,
        "generation_ms": gen_ms,
        "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }

    # Persist the advisory so the canonical operations/expert queues and audit
    # workflows can observe the result that was returned to the farmer.
    try:
        await db.execute(
            text(
                """
                INSERT INTO advisories (
                    id, observation_id, confidence_state, confidence_score,
                    recommended_scenario, scenarios_json, evidence_bundle_json,
                    recommended_action_json, what_would_change_json,
                    safe_to_act, sources_json, scheme_matches_json,
                    model_version, knowledge_version, generation_ms
                ) VALUES (
                    CAST(:id AS UUID), CAST(:observation_id AS UUID),
                    :confidence_state, :confidence_score, :recommended_scenario,
                    CAST(:scenarios_json AS JSONB), CAST(:evidence_bundle_json AS JSONB),
                    CAST(:recommended_action_json AS JSONB),
                    CAST(:what_would_change_json AS JSONB), :safe_to_act,
                    CAST(:sources_json AS JSONB), CAST(:scheme_matches_json AS JSONB),
                    :model_version, :knowledge_version, :generation_ms
                )
                """
            ),
            {
                "id": advisory_id,
                "observation_id": str(obs.id),
                "confidence_state": response_data["confidence_state"],
                "confidence_score": response_data["confidence_score"],
                "recommended_scenario": response_data["recommended_scenario"],
                "scenarios_json": json.dumps(response_data["scenarios"]),
                "evidence_bundle_json": json.dumps(response_data["evidence"]),
                "recommended_action_json": json.dumps(response_data["recommended_action"]),
                "what_would_change_json": json.dumps(response_data["what_would_change_this"]),
                "safe_to_act": response_data["safe_to_act"],
                "sources_json": json.dumps(response_data["sources"]),
                "scheme_matches_json": json.dumps(response_data["scheme_matches"]),
                "model_version": response_data["model_version"],
                "knowledge_version": settings.KNOWLEDGE_VERSION,
                "generation_ms": response_data["generation_ms"],
            },
        )
        await db.commit()
    except Exception as exc:
        await db.rollback()
        logger.error("advisory_persistence_failed", error_type=type(exc).__name__)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Advisory storage is unavailable",
        ) from exc

    return response_data
