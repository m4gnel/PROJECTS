from typing import Dict, Any, Optional
from backend.agents.state import AgriSAGEState


class EconomicsAgent:
    """Agent evaluating intervention economic viability, ROI, treatment cost, and net return."""

    def __init__(self, msp_price_per_kg: float = 23.0):
        # Baseline Minimum Support Price (MSP) per kg for standard crops (e.g. Paddy ~Rs 23/kg)
        self.default_msp = msp_price_per_kg

    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        vision_result = state.get("vision_result") or {}
        crop = state.get("crop") or "paddy"
        
        # Estimate disease severity impact (0.0 to 1.0)
        disease_severity = vision_result.get("severity", 0.25)
        
        # Treatment cost estimate (INR per acre) based on severity and intervention type
        chemical_cost_inr = round(500.0 + (disease_severity * 1000.0), 2)
        labor_cost_inr = 400.0
        total_intervention_cost = round(chemical_cost_inr + labor_cost_inr, 2)

        # Baseline expected yield (kg/acre)
        baseline_yield_kg = 2000.0
        potential_loss_percentage = min(0.60, disease_severity * 0.80)
        
        yield_loss_without_treatment_kg = baseline_yield_kg * potential_loss_percentage
        protected_yield_kg = yield_loss_without_treatment_kg * 0.85  # 85% efficacy of treatment
        
        protected_value_inr = round(protected_yield_kg * self.default_msp, 2)
        net_financial_benefit_inr = round(protected_value_inr - total_intervention_cost, 2)
        
        roi_ratio = round(protected_value_inr / max(1.0, total_intervention_cost), 2)

        economics_result = {
            "crop": crop,
            "disease_severity": disease_severity,
            "chemical_cost_inr": chemical_cost_inr,
            "labor_cost_inr": labor_cost_inr,
            "total_intervention_cost_inr": total_intervention_cost,
            "protected_yield_kg": round(protected_yield_kg, 1),
            "protected_value_inr": protected_value_inr,
            "net_financial_benefit_inr": net_financial_benefit_inr,
            "roi_ratio": roi_ratio,
            "is_economically_viable": net_financial_benefit_inr > 0,
            "currency": "INR",
            "unit": "per acre"
        }

        state["economics_result"] = economics_result
        return state
