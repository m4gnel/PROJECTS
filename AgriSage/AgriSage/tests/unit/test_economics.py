import pytest
from backend.agents.economics import EconomicsAgent
from backend.agents.state import AgriSAGEState


@pytest.mark.asyncio
async def test_economics_agent_calculation():
    agent = EconomicsAgent()
    state: AgriSAGEState = {
        "crop": "paddy",
        "vision_result": {"label": "rice_blast", "severity": 0.30},
    }
    
    res_state = await agent.run(state)
    econ = res_state.get("economics_result")
    
    assert econ is not None
    assert econ["crop"] == "paddy"
    assert econ["chemical_cost_inr"] > 0
    assert econ["total_intervention_cost_inr"] > 0
    assert econ["protected_yield_kg"] > 0
    assert econ["roi_ratio"] > 1.0
    assert econ["is_economically_viable"] is True
