import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState
from backend.services.pest_service import pest_service

logger = logging.getLogger(__name__)


async def pest_node(state: AgriSageState) -> Dict[str, Any]:
    location = state.get("location", {})
    district = location.get("district", "Ernakulam") if isinstance(location, dict) else "Ernakulam"
    crop = state.get("crop", None)

    ctx = await pest_service.get_alerts_for_district_and_crop(district=district, crop=crop)
    res_dict = {
        "highest_severity": ctx.highest_severity,
        "alerts_count": len(ctx.alerts),
        "alerts": ctx.alerts
    }

    return {
        "pest_alerts": ctx.alerts,
        "agent_outputs": {"pest": res_dict}
    }
