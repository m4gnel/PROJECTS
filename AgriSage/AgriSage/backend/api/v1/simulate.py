from typing import Dict, Any, Optional
from fastapi import APIRouter, Body
from backend.simulation.dssat import DSSATSimulator
from backend.simulation.interface import SimulationParams

router = APIRouter(tags=["Simulation"])

simulator = DSSATSimulator()


@router.post("/simulate/scenario")
async def run_crop_simulation_scenario(
    payload: Dict[str, Any] = Body(...)
) -> Dict[str, Any]:
    """Run DSSAT simulation returning 3-way comparative yield, cost, and income scenarios."""
    crop = payload.get("crop", "paddy")
    stage_code = payload.get("stage_code", "tillering")
    gdd = payload.get("gdd_accumulated", 450.0)
    temp_c = payload.get("temp_c", 28.5)
    rainfall_mm = payload.get("rainfall_mm", 5.0)
    humidity_pct = payload.get("humidity_pct", 78.0)
    severity = payload.get("disease_severity", 0.25)

    params = SimulationParams(
        crop=crop,
        stage_code=stage_code,
        gdd_accumulated=gdd,
        daily_temp_c=temp_c,
        daily_rainfall_mm=rainfall_mm,
        relative_humidity_pct=humidity_pct,
        disease_severity=severity
    )

    return await simulator.run_simulation(params)
