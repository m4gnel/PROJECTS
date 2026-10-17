from .state import AgriState
from datetime import datetime, timedelta

# Crop GDD (Growing Degree Days) to maturity
CROP_DAYS = {
    "rice": 120, "wheat": 110, "maize": 100, "soybean": 105,
    "coconut": 365, "banana": 300, "pepper": 180, "default": 120,
}


async def harvest_node(state: AgriState) -> dict:
    """
    Predicts harvest date from sowing_date + crop GDD model.
    Returns: {"agent_findings": ["harvest: Estimated harvest on <date>"], "agents_completed": ["harvest"]}
    """
    try:
        crop_name = ""
        sowing_date = None
        if state.get("crop_info"):
            ci = state["crop_info"] or {}
            crop_name = ci.get("crop_name", "").lower()
            sowing_date = ci.get("sowing_date")

        if not sowing_date:
            return {"agent_findings": ["harvest: Sowing date unknown — cannot predict harvest."], "agents_completed": ["harvest"]}

        days_to_harvest = CROP_DAYS.get(crop_name, CROP_DAYS["default"])
        sowing = datetime.fromisoformat(sowing_date)
        harvest_date = sowing + timedelta(days=days_to_harvest)
        today = datetime.now()
        days_remaining = (harvest_date - today).days

        msg = f"Estimated harvest on {harvest_date.strftime('%Y-%m-%d')} ({days_remaining} days remaining)."
        return {"agent_findings": [f"harvest: {msg}"], "agents_completed": ["harvest"]}
    except Exception as e:
        return {"error_messages": [f"harvest: {str(e)}"], "agents_completed": ["harvest"]}
