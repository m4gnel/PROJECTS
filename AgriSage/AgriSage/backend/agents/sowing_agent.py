import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState

logger = logging.getLogger(__name__)


async def sowing_node(state: AgriSageState) -> Dict[str, Any]:
    crop = (state.get("crop") or "rice").lower()

    res_dict = {
        "crop": crop,
        "recommended_window": None,
        "predicted_yield_kg_ha": None,
        "dssat_simulation_status": "UNAVAILABLE",
        "warning": "Sowing timing and yield estimates require current location, season, and verified crop guidance.",
    }

    return {
        "dssat_output": res_dict,
        "agent_outputs": {"sowing": res_dict}
    }
