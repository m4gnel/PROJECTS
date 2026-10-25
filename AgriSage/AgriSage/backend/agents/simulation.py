from backend.agents.state import AgriSAGEState
from backend.simulation.dssat import DSSATSimulator
from backend.simulation.interface import SimulationParams


simulator = DSSATSimulator()


class SimulationAgent:
    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        crop = state.get("crop") or "rice"

        if not state.get("run_simulation", False):
            state["simulation_result"] = {
                "engine": "dssat",
                "ran": False,
                "reason": "Simulation not requested or confidence too low"
            }
            return state

        weather = state.get("weather_result") or {}
        stage = state.get("crop_stage_result") or {}
        vision = state.get("vision_result") or {}
        if weather.get("available") is False or not weather:
            state["simulation_result"] = {
                "engine": "dssat",
                "ran": False,
                "reason": "Current weather data is unavailable",
            }
            return state

        affected_area = float(vision.get("affected_area_pct", 0.0) or 0.0)
        params = SimulationParams(
            crop=crop,
            stage_code=stage.get("stage_code", "tillering"),
            gdd_accumulated=float(stage.get("cumulative_gdd", 0.0) or 0.0),
            daily_temp_c=float(weather.get("temp_c", 0.0) or 0.0),
            daily_rainfall_mm=float(weather.get("rain_mm_24h", 0.0) or 0.0),
            relative_humidity_pct=float(weather.get("humidity_pct", 0.0) or 0.0),
            disease_severity=max(0.0, min(1.0, affected_area / 100.0)),
        )
        simulation_result = await simulator.run_simulation(params)
        simulation_result = {
            "engine": "dssat",
            "ran": True,
            **simulation_result,
        }

        state["simulation_result"] = simulation_result
        return state
