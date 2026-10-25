import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState

logger = logging.getLogger(__name__)

async def fertilizer_node(state: AgriSageState) -> Dict[str, Any]:
    crop = (state.get("crop") or "coconut").lower()
    res_dict = {
        "available": False,
        "crop": crop,
        "nitrogen_g": None,
        "phosphorus_g": None,
        "potassium_g": None,
        "organic_amendment_kg": None,
        "warning": "Fertilizer dosage requires a current soil test and verified crop-specific guidance.",
    }

    return {
        "agent_outputs": {"fertilizer": res_dict}
    }
