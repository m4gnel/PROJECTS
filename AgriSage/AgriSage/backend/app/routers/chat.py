from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone, timedelta
from ..database import get_db
from ..schemas.chat import ChatRequest, ChatResponse
from .farmers import get_current_farmer
from ..models.farmer import Farmer

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    current_farmer: Farmer = Depends(get_current_farmer),
    db: AsyncSession = Depends(get_db)
):
    from ..agents.graph import agri_graph
    from ..agents.state import AgriState

    config = {"configurable": {"thread_id": request.session_id}}

    initial_state: AgriState = {
        "query": request.message,
        "language": request.language,
        "farmer_id": str(request.farmer_id),
        "field_id": str(request.field_id) if request.field_id else None,
        "location_lat": request.latitude,
        "location_lon": request.longitude,
        "crop_info": request.crop_info.model_dump() if request.crop_info else None,
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
    return ChatResponse(
        session_id=request.session_id,
        message=result.get("advisory_text", ""),
        language=request.language,
        confidence=result.get("confidence_score", 0.0),
        alerts=[],
        agents_used=result.get("agents_completed", []),
        created_at=datetime.now(tz),
    )
