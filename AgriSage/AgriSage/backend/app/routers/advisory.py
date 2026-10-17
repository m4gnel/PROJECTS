from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta
from ..database import get_db
from ..schemas.advisory import AdvisoryRequest, AdvisoryResponse
from .farmers import get_current_farmer
from ..models.farmer import Farmer

router = APIRouter()


@router.post("/ask", response_model=AdvisoryResponse)
async def ask_advisory(
    request: AdvisoryRequest,
    current_farmer: Farmer = Depends(get_current_farmer),
    db: AsyncSession = Depends(get_db)
):
    from ..agents.graph import agri_graph
    from ..agents.state import AgriState

    config = {"configurable": {"thread_id": f"advisory-{request.farmer_id}"}}

    initial_state: AgriState = {
        "query": request.question,
        "language": request.language,
        "farmer_id": request.farmer_id,
        "field_id": request.field_id,
        "location_lat": current_farmer.latitude or 10.1632,
        "location_lon": current_farmer.longitude or 76.3986,
        "crop_info": None,
        "weather_data": None,
        "soil_data": None,
        "ndvi_value": None,
        "pest_alerts": [],
        "market_prices": [],
        "dssat_result": None,
        "agent_findings": [],
        "advisory_text": "",
        "alerts_generated": [],
        "confidence_score": 0.0,
        "agents_needed": [],
        "agents_completed": [],
        "error_messages": [],
    }

    result = await agri_graph.ainvoke(initial_state, config=config)

    tz = timezone(timedelta(hours=5, minutes=30))
    return AdvisoryResponse(
        question=request.question,
        answer=result.get("advisory_text", "Unable to generate advisory."),
        language=request.language,
        confidence=result.get("confidence_score", 0.0),
        sources=["KAU Package of Practices", "Real-time weather data"],
        agents_used=result.get("agents_completed", []),
        created_at=datetime.now(tz),
    )
