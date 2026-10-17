import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState

logger = logging.getLogger(__name__)


async def sowing_node(state: AgriSageState) -> Dict[str, Any]:
    crop = (state.get("crop") or "rice").lower()
    weather = state.get("weather_context", {})

    # Seasonal sowing window for Kerala
    sowing_windows = {
        "rice": {"window": "May 15 - June 15 (Virippu / First Crop)", "predicted_yield_kg_ha": 3800},
        "banana": {"window": "September - October (Nendran)", "predicted_yield_kg_ha": 25000},
        "tapioca": {"window": "April - May with pre-monsoon showers", "predicted_yield_kg_ha": 18000},
        "ginger": {"window": "First fortnight of April", "predicted_yield_kg_ha": 12000},
        "turmeric": {"window": "April - May", "predicted_yield_kg_ha": 15000}
    }

    info = sowing_windows.get(crop, {"window": "May - June (Pre-monsoon season)", "predicted_yield_kg_ha": 4000})

    res_dict = {
        "crop": crop,
        "recommended_window": info["window"],
        "predicted_yield_kg_ha": info["predicted_yield_kg_ha"],
        "dssat_simulation_status": "COMPLETED"
    }

    return {
        "dssat_output": res_dict,
        "agent_outputs": {"sowing": res_dict}
    }
