from datetime import date, datetime
from typing import Dict, Any
from backend.agents.state import AgriSAGEState

ALLOWED_CROPS = {"rice", "banana", "coconut", "tomato", "maize"}


class IntakeAgent:
    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        warnings = []
        errors = []

        farm_state = state.get("farm_state") or {}

        # 1. Normalize crop name
        raw_crop = farm_state.get("crop") or state.get("crop") or ""
        normalized_crop = raw_crop.lower().strip()

        if normalized_crop not in ALLOWED_CROPS:
            warnings.append("crop not normalized")
            state["crop"] = None
        else:
            state["crop"] = normalized_crop

        # 2. Compute days_after_sowing
        planting_date_str = farm_state.get("planting_date")
        days_after_sowing = None
        if planting_date_str:
            try:
                if isinstance(planting_date_str, date):
                    p_date = planting_date_str
                else:
                    p_date = datetime.strptime(str(planting_date_str), "%Y-%m-%d").date()
                days_after_sowing = (date.today() - p_date).days
            except Exception:
                warnings.append("invalid planting_date format")

        farm_state["days_after_sowing"] = days_after_sowing

        # 3. Flag null required fields
        if not farm_state.get("location_lat") or not farm_state.get("location_lon"):
            warnings.append("missing location coordinates")
        if not farm_state.get("district"):
            warnings.append("missing district")

        state["farm_state"] = farm_state
        state["warnings"] = warnings
        state["errors"] = errors
        return state
