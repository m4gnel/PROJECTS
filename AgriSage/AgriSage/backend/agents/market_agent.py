import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState
from backend.services.market_service import market_service

logger = logging.getLogger(__name__)


async def market_node(state: AgriSageState) -> Dict[str, Any]:
    location = state.get("location", {})
    district = location.get("district", "Ernakulam") if isinstance(location, dict) else "Ernakulam"
    crop = state.get("crop", "coconut") or "coconut"

    ctx = await market_service.get_market_data(crop=crop, district=district)
    res_dict = {
        "crop": ctx.crop_name,
        "variety": ctx.variety,
        "district": ctx.district,
        "min_price": ctx.min_price,
        "max_price": ctx.max_price,
        "modal_price": ctx.modal_price,
        "date": ctx.date,
        "trend": ctx.trend,
        "sell_recommendation": ctx.sell_recommendation
    }

    return {
        "market_data": res_dict,
        "agent_outputs": {"market": res_dict}
    }
