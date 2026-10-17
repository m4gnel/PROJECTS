import pytest
import asyncio
from backend.agents.orchestrator import run_advisory_pipeline
from backend.agents.state import AgriSAGEState

VALID_STATES = {'CONFIRMED', 'LIKELY', 'POSSIBLE', 'UNCERTAIN', 'INSUFFICIENT_DATA', 'CONFLICTING_EVIDENCE', 'OUT_OF_SCOPE'}

@pytest.mark.asyncio
async def test_full_advisory_pipeline_e2e():
    """Integration test verifying full 14-agent pipeline execution and response schema."""
    initial_state: AgriSAGEState = {
        "observation_id": "test-obs-12345",
        "user_id": "test-user-67890",
        "images": [{"key": "test_image.jpg"}],
        "farm_state": {
            "crop": "rice",
            "planting_date": "2026-06-15",
            "district": "Palakkad",
            "state": "Kerala",
            "location_lat": 10.8505,
            "location_lon": 76.2711,
            "days_after_sowing": 45
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
        "pipeline_start_ms": 1000,
        "generation_ms": None,
        "language": "ml",
        "crop": "rice",
    }

    result_state = await run_advisory_pipeline(initial_state, thread_id="test-thread-1")
    print(f"[DEBUG test] result_state keys={list(result_state.keys()) if isinstance(result_state, dict) else type(result_state)}")
    print(f"[DEBUG test] result_state['confidence_state']={result_state.get('confidence_state')}")
    print(f"[DEBUG test] result_state['critic_result']={result_state.get('critic_result')}")

    conf_state = result_state.get("confidence_state")
    assert conf_state in VALID_STATES, f"Invalid confidence_state: {conf_state}"

    # Assert 2: Critic result safe_to_act is boolean
    critic = result_state.get("critic_result") or {}
    assert isinstance(critic.get("safe_to_act"), bool)

    # Assert 3: Decision scenarios all have modelled_estimate == True
    decision = result_state.get("decision_result") or {}
    scenarios = decision.get("scored_scenarios", [])
    for sc in scenarios:
        assert sc.get("modelled_estimate") is True

    # Assert 4: Advisory response exists
    advisory = result_state.get("advisory")
    assert advisory is not None
