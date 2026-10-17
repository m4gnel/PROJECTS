import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState
from backend.services.soil_service import get_soil_by_district

logger = logging.getLogger(__name__)


async def soil_node(state: AgriSageState) -> Dict[str, Any]:
    location = state.get("location", {})
    district = location.get("district", "Ernakulam") if isinstance(location, dict) else "Ernakulam"
    crop = state.get("crop", "unknown")

    soil_ctx = get_soil_by_district(district)
    if not soil_ctx:
        res_dict = {"status": "unavailable", "district": district}
    else:
        res_dict = {
            "district": soil_ctx.district,
            "ph_range": f"{soil_ctx.ph_min} - {soil_ctx.ph_max}",
            "texture": soil_ctx.texture,
            "organic_carbon": soil_ctx.organic_carbon,
            "npk_status": {
                "n": soil_ctx.n_status,
                "p": soil_ctx.p_status,
                "k": soil_ctx.k_status
            },
            "suitable_crops": soil_ctx.suitable_crops
        }

    return {
        "soil_context": res_dict,
        "agent_outputs": {"soil": res_dict}
    }
