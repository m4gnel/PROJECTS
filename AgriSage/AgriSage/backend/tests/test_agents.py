import pytest
from app.agents.state import AgriState
from app.agents.soil_agent import soil_node
from app.agents.weather_agent import weather_node
from app.agents.orchestrator import orchestrator_node, should_continue


@pytest.mark.asyncio
async def test_soil_agent():
    state: AgriState = {
        "query": "soil test",
        "language": "en",
        "farmer_id": "f1",
        "field_id": "field1",
        "location_lat": 10.165,
        "location_lon": 76.401,
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
    res = await soil_node(state)
    assert "soil_data" in res
    assert "soil" in res.get("agents_completed", [])
    assert res["soil_data"]["soil_type"] == "laterite"


@pytest.mark.asyncio
async def test_orchestrator():
    state: AgriState = {
        "query": "What is the weather and fertilizer?",
        "language": "en",
        "farmer_id": "f1",
        "field_id": None,
        "location_lat": 10.165,
        "location_lon": 76.401,
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
    res = orchestrator_node(state)
    assert "agents_needed" in res
    assert len(res["agents_needed"]) > 0
