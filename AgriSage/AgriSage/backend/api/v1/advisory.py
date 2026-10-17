"""
POST /api/v1/advisory — Agri-SAGE Advisory Router
Wraps the LangGraph multi-agent graph (graph.py) for the Android advisory chat flow.
"""
import time
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from backend.agents.graph import graph
from backend.agents.state import AgriSageState
from backend.dependencies import require_auth

try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

router = APIRouter(tags=["Advisory"])


# ─────────────────────────────────────────────
# Request / Response Schemas
# ─────────────────────────────────────────────

class AdvisoryRequest(BaseModel):
    """Schema for POST /api/v1/advisory — matches Android AdvisoryRequest DTO."""
    farmer_id: str = Field(..., description="Unique farmer identifier")
    query: str = Field(..., min_length=1, max_length=2000, description="Farmer's question (any language)")
    language: str = Field(default="en", description="Preferred response language: hi/en/ta/ml/te/pa")
    state: str = Field(default="Kerala", description="Indian state name")
    district: str = Field(default="Ernakulam", description="District name")
    crops: List[str] = Field(default_factory=list, description="Farmer's crops")
    lat: Optional[float] = Field(default=None, description="GPS latitude")
    lon: Optional[float] = Field(default=None, description="GPS longitude")
    farm_size_acres: Optional[float] = Field(default=None, description="Total farm size in acres")


class AdvisoryResponse(BaseModel):
    """Schema for advisory response — matches Android AdvisoryResponse DTO."""
    answer_native: str = Field(..., description="Answer in farmer's selected language")
    answer_en: str = Field(..., description="Answer in English (for logging/debug)")
    agents_used: List[str] = Field(default_factory=list, description="Which agents contributed")
    language: str = Field(default="en", description="Detected/used language")
    farmer_id: str
    generation_ms: int = Field(default=0, description="Pipeline latency in ms")
    fcm_triggered: bool = Field(default=False)
    warnings: List[str] = Field(default_factory=list)


# ─────────────────────────────────────────────
# Advisory Endpoint
# ─────────────────────────────────────────────

@router.post(
    "/advisory",
    response_model=AdvisoryResponse,
    status_code=status.HTTP_200_OK,
    summary="Run multi-agent farming advisory pipeline",
    description=(
        "Accepts a farmer's query in any of 6 supported languages "
        "(hi/en/ta/ml/te/pa) and runs it through the 14-agent LangGraph "
        "pipeline to produce a localised, source-cited advisory response."
    ),
)
async def get_advisory(
    request: AdvisoryRequest,
    auth: Dict[str, Any] = Depends(require_auth),
) -> AdvisoryResponse:
    """
    POST /api/v1/advisory

    Runs: TranslatorPre → Router → [Parallel: Weather|Soil|Pest|Crop|Irrigation|Market] →
          Synthesizer → TranslatorPost → Alert → Analytics → END

    Returns the synthesised advisory in the farmer's preferred language.
    """
    start_ms = int(time.time() * 1000)

    # Build initial LangGraph state
    initial_state: AgriSageState = {
        "farmer_id": request.farmer_id,
        "user_id": auth.get("sub", request.farmer_id),
        "farmer_query": request.query,
        "language": request.language,
        "location": {
            "state": request.state,
            "district": request.district,
            "lat": request.lat,
            "lon": request.lon,
        },
        "crop": request.crops[0] if request.crops else None,
        "crops": request.crops,
        "query_intent": [],
        "images": [],
        "farm_state": {
            "district": request.district,
            "state": request.state,
            "farm_size_acres": request.farm_size_acres,
        },
        "weather_context": {},
        "soil_context": {},
        "pest_alerts": [],
        "market_data": {},
        "kau_rag_results": [],
        "dssat_output": {},
        "agent_outputs": {},
        "final_answer_en": "",
        "final_answer_ml": "",
        "fcm_triggered": False,
        "error": None,
        "warnings": [],
        "errors": [],
        "pipeline_start_ms": start_ms,
        "generation_ms": None,
        "run_simulation": False,
        "confidence_state": None,
    }

    try:
        import asyncio
        config = {
            "configurable": {"thread_id": f"{request.farmer_id}_{int(time.time())}"}
        }
        result = await asyncio.wait_for(
            graph.ainvoke(initial_state, config=config),
            timeout=20.0,
        )
    except asyncio.TimeoutError:
        logger.error("advisory_pipeline_timeout", farmer_id=request.farmer_id)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Advisory pipeline timed out. Please try again.",
        )
    except Exception as exc:
        logger.error("advisory_pipeline_error", farmer_id=request.farmer_id, error=str(exc))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )

    gen_ms = int(time.time() * 1000) - start_ms

    # Pull outputs from result dict safely
    answer_en: str = result.get("final_answer_en") or ""
    answer_native: str = result.get("final_answer_ml") or answer_en
    agents_used: List[str] = list(result.get("agent_outputs", {}).keys())
    detected_lang: str = result.get("language", request.language)
    fcm_triggered: bool = result.get("fcm_triggered", False)
    warnings: List[str] = result.get("warnings", [])

    # Graceful fallback if pipeline produced no answer
    if not answer_en:
        answer_en = (
            "I was unable to generate an advisory at this time. "
            "Please consult your nearest Krishi Vigyan Kendra or call "
            "the Kisan Call Centre: 1800-180-1551 (free, 24×7)."
        )
        answer_native = answer_en

    logger.info(
        "advisory_complete",
        farmer_id=request.farmer_id,
        language=detected_lang,
        agents_used=agents_used,
        gen_ms=gen_ms,
        fcm_triggered=fcm_triggered,
    )

    return AdvisoryResponse(
        answer_native=answer_native,
        answer_en=answer_en,
        agents_used=agents_used,
        language=detected_lang,
        farmer_id=request.farmer_id,
        generation_ms=gen_ms,
        fcm_triggered=fcm_triggered,
        warnings=warnings,
    )
