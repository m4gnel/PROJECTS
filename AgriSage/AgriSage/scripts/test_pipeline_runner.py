import sys
import asyncio

sys.path.insert(0, ".")

from backend.agents.orchestrator import run_advisory_pipeline
from backend.agents.state import AgriSAGEState

async def main():
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

    result = await run_advisory_pipeline(initial_state, thread_id="test-thread-1")
    print("Pipeline result confidence state:", result.get("confidence_state"))
    print("Safe to act:", result.get("critic_result", {}).get("safe_to_act"))
    print("Decision scenarios:", result.get("decision_result", {}).get("recommended_scenario"))
    print("Advisory summary:", result.get("advisory", {}).get("diagnosis_summary"))
    print("PASS: 14-Agent pipeline executed successfully.")

if __name__ == "__main__":
    asyncio.run(main())
