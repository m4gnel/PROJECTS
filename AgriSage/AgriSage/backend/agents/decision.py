from typing import Dict, Any, List
from backend.agents.state import AgriSAGEState


class DecisionAgent:
    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        critic = state.get("critic_result") or {}
        sim = state.get("simulation_result") or {}
        confidence_score = critic.get("confidence_score", 0.8)

        # Scenarios A, B, C
        scenarios = [
            {
                "id": "A",
                "label": "Integrated Chemical Control",
                "action": "Spray Tricyclazole 75% WP @ 0.6g/L during early spray window",
                "expected_yield_kgha": 4500.0,
                "modelled_estimate": True,
                "expected_cost_inr": 1200.0,
                "expected_net_return_inr": 48000.0,
                "risk_level": "low"
            },
            {
                "id": "B",
                "label": "Biological / Organic Control",
                "action": "Apply Pseudomonas fluorescens @ 10g/L spray",
                "expected_yield_kgha": 4100.0,
                "modelled_estimate": True,
                "expected_cost_inr": 600.0,
                "expected_net_return_inr": 42000.0,
                "risk_level": "medium"
            },
            {
                "id": "C",
                "label": "Monitoring & Cultural Only",
                "action": "Drain excess water, delay nitrogen fertilizer",
                "expected_yield_kgha": 3600.0,
                "modelled_estimate": True,
                "expected_cost_inr": 0.0,
                "expected_net_return_inr": 35000.0,
                "risk_level": "high"
            }
        ]

        # Score scenarios
        risk_penalties = {"critical": 3.0, "high": 2.0, "medium": 1.0, "low": 0.0}
        uncertainty_penalty = (1.0 - confidence_score) * 2.0

        for sc in scenarios:
            rp = risk_penalties.get(sc["risk_level"], 1.0)
            # Normalization scale
            norm_yield = sc["expected_yield_kgha"] / 5000.0
            norm_return = sc["expected_net_return_inr"] / 50000.0
            sc["score"] = round(norm_yield + norm_return - rp - uncertainty_penalty, 2)

        # Recommended scenario is highest scored
        best_sc = max(scenarios, key=lambda s: s["score"])

        decision_result = {
            "recommended_scenario": best_sc["id"],
            "scored_scenarios": scenarios,
            "reasoning": f"Scenario {best_sc['id']} ({best_sc['label']}) offers highest net return with acceptable risk level."
        }

        state["decision_result"] = decision_result
        return state
