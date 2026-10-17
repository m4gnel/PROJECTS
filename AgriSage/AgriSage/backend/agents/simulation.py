from typing import Dict, Any
from backend.agents.state import AgriSAGEState


class SimulationAgent:
    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        crop = state.get("crop") or "rice"
        critic = state.get("critic_result") or {}

        if not state.get("run_simulation", False):
            state["simulation_result"] = {
                "engine": "dssat",
                "ran": False,
                "reason": "Simulation not requested or confidence too low"
            }
            return state

        simulation_result = {
            "engine": "dssat",
            "ran": True,
            "scenario_a": {
                "yield_kgha": 4500.0,
                "net_return_inr": 48000.0,
                "is_modelled_estimate": True
            },
            "scenario_b": {
                "yield_kgha": 4100.0,
                "net_return_inr": 42000.0,
                "is_modelled_estimate": True
            },
            "scenario_c": {
                "yield_kgha": 3600.0,
                "net_return_inr": 35000.0,
                "is_modelled_estimate": True
            }
        }

        state["simulation_result"] = simulation_result
        return state
