from backend.agents.state import AgriSAGEState


class DecisionAgent:
    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        critic = state.get("critic_result") or {}
        sim = state.get("simulation_result") or {}
        confidence_score = float(critic.get("confidence_score", 0.0) or 0.0)
        scenarios = list(sim.get("scenarios") or []) if sim.get("ran") else []

        if not scenarios:
            state["decision_result"] = {
                "recommended_scenario": None,
                "scored_scenarios": [],
                "reasoning": "No verified simulation result is available.",
            }
            return state

        # Score scenarios
        risk_penalties = {"critical": 3.0, "high": 2.0, "medium": 1.0, "low": 0.0}
        uncertainty_penalty = (1.0 - confidence_score) * 2.0

        for sc in scenarios:
            rp = risk_penalties.get(sc["risk_level"], 1.0)
            # Normalization scale
            norm_yield = float(sc.get("expected_yield_kgha", 0.0) or 0.0) / 5000.0
            norm_return = float(sc.get("expected_net_return_inr", 0.0) or 0.0) / 50000.0
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
