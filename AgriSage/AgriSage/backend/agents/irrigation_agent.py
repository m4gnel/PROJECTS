import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState

logger = logging.getLogger(__name__)


async def irrigation_node(state: AgriSageState) -> Dict[str, Any]:
    weather = state.get("weather_context", {})
    crop = state.get("crop", "coconut")
    stage = state.get("crop_stage", "vegetative")

    temp_c = weather.get("temp_c", 28.0)
    rain_24h = weather.get("rain_mm_24h", 0.0)

    # Calculate basic water requirement (ET0 approximation)
    base_et0 = 4.0 if temp_c < 30 else 5.5
    if rain_24h > 10.0:
        recommendation = "No irrigation needed due to recent rainfall."
        water_mm = 0.0
    elif rain_24h < 1.0 and temp_c > 32.0:
        recommendation = f"High evaporation ({temp_c}°C). Drip irrigate 40-50 Liters per palm/plant."
        water_mm = base_et0 * 1.2
    else:
        recommendation = f"Standard irrigation schedule for {crop} ({stage} stage)."
        water_mm = base_et0

    res_dict = {
        "irrigation_mm": water_mm,
        "recommendation": recommendation,
        "crop": crop,
        "stage": stage
    }

    return {
        "agent_outputs": {"irrigation": res_dict}
    }
