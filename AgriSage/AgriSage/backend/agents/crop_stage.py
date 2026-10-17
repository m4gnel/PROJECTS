import os
import json
from typing import Dict, Any, List
from pydantic import BaseModel
from backend.agents.state import AgriSAGEState

GDD_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "gdd_thresholds.json")
if os.path.exists(GDD_PATH):
    with open(GDD_PATH, "r", encoding="utf-8") as f:
        GDD_DATA = json.load(f)
else:
    GDD_DATA = {"base_temperatures": {}, "thresholds": {}}


class CropStageResult(BaseModel):
    stage_code: str
    stage_name: str
    vulnerability: str
    days_after_sowing: int
    cumulative_gdd: float
    diseases_expected: List[str]
    upcoming_vulnerable_stage: str = "flowering"


class CropStageAgent:
    def estimate_stage(self, crop: str, cumulative_gdd: float) -> CropStageResult:
        thresholds = GDD_DATA.get("thresholds", {}).get(crop, {})
        matched_stage_code = "tillering"
        vulnerability = "medium"
        diseases_expected = []

        for stage_code, info in thresholds.items():
            gdd_from = info.get("gdd_from", 0)
            gdd_to = info.get("gdd_to", 9999)
            if gdd_from <= cumulative_gdd <= gdd_to:
                matched_stage_code = stage_code
                vulnerability = info.get("vulnerability", "medium")
                diseases_expected = info.get("diseases_expected", [])
                break

        return CropStageResult(
            stage_code=matched_stage_code,
            stage_name=matched_stage_code.replace("_", " ").title(),
            vulnerability=vulnerability,
            days_after_sowing=int(cumulative_gdd / 12.5),
            cumulative_gdd=cumulative_gdd,
            diseases_expected=diseases_expected,
            upcoming_vulnerable_stage="flowering"
        )

    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        crop = state.get("crop") or "rice"
        farm_state = state.get("farm_state") or {}
        das = farm_state.get("days_after_sowing") or 45

        base_temp = GDD_DATA.get("base_temperatures", {}).get(crop, 10)
        cumulative_gdd = float(das * 12.5)

        est = self.estimate_stage(crop=crop, cumulative_gdd=cumulative_gdd)

        crop_stage_result = {
            "stage_code": est.stage_code,
            "stage_name": est.stage_name,
            "vulnerability": est.vulnerability,
            "days_after_sowing": das,
            "cumulative_gdd": cumulative_gdd,
            "diseases_expected": est.diseases_expected,
            "upcoming_vulnerable_stage": est.upcoming_vulnerable_stage
        }

        state["crop_stage_result"] = crop_stage_result
        return state

