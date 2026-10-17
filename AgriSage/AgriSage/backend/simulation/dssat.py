from typing import Dict, Any
from backend.simulation.interface import SimulationEngineInterface, SimulationParams
from backend.simulation.scenarios import ScenarioBuilder
from backend.simulation.rules import PhenologyRules, WaterStressRules, DiseaseFavorabilityRules


class DSSATSimulator(SimulationEngineInterface):
    """DSSAT (Decision Support System for Agrotechnology Transfer) Crop Simulation Engine."""

    async def run_simulation(self, params: SimulationParams) -> Dict[str, Any]:
        scenarios = ScenarioBuilder.generate_scenarios(params)
        
        gdd = PhenologyRules.calculate_daily_gdd(
            crop=params.crop,
            temp_max=params.daily_temp_c + 4.0,
            temp_min=params.daily_temp_c - 4.0
        )
        
        wsi = WaterStressRules.calculate_water_stress_index(
            rainfall_mm=params.daily_rainfall_mm,
            humidity_pct=params.relative_humidity_pct,
            temp_c=params.daily_temp_c
        )

        dfi = DiseaseFavorabilityRules.calculate_dfi(
            relative_humidity_pct=params.relative_humidity_pct,
            temp_c=params.daily_temp_c,
            consecutive_wet_days=2
        )

        return {
            "crop": params.crop,
            "stage_code": params.stage_code,
            "accumulated_gdd": params.gdd_accumulated + gdd,
            "water_stress_index": wsi,
            "disease_favorability_index": dfi,
            "scenarios": scenarios,
            "modelled_estimate_disclaimer": "* Modelled estimate based on ICAR calibrated DSSAT parameters."
        }
