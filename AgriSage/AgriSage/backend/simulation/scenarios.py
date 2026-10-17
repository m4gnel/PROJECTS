from typing import List, Dict, Any
from backend.simulation.interface import SimulationParams, ScenarioResult
from backend.simulation.rules import WaterStressRules, DiseaseFavorabilityRules


class ScenarioBuilder:
    """Builder generating 3-way comparative DSSAT crop yield scenarios."""

    @classmethod
    def generate_scenarios(cls, params: SimulationParams) -> List[Dict[str, Any]]:
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

        base_yield = 4500.0 if params.crop in ["rice", "paddy"] else 3800.0
        msp = 23.0  # INR per kg baseline

        # Scenario A: Recommended Treatment
        yield_a = base_yield * (1.0 - (params.disease_severity * 0.05))
        cost_a = 1200.0
        net_a = (yield_a * msp) - cost_a

        # Scenario B: Biological / Organic Control
        yield_b = base_yield * (1.0 - (params.disease_severity * 0.15))
        cost_b = 600.0
        net_b = (yield_b * msp) - cost_b

        # Scenario C: Do Nothing / Monitoring Only
        yield_c = base_yield * (1.0 - (params.disease_severity * 0.40))
        cost_c = 0.0
        net_c = (yield_c * msp) - cost_c

        return [
            ScenarioResult(
                id="A",
                label="Integrated Chemical Control",
                action="Apply recommended fungicide/pesticide during early morning spray window",
                expected_yield_kgha=round(yield_a, 1),
                expected_cost_inr=cost_a,
                expected_net_return_inr=round(net_a, 2),
                risk_level="low",
                water_stress_index=wsi,
                nitrogen_stress_index=0.1,
                modelled_estimate=True
            ).__dict__,
            ScenarioResult(
                id="B",
                label="Biological / Bio-control Option",
                action="Apply bio-control agent (Pseudomonas fluorescens) with organic mulch",
                expected_yield_kgha=round(yield_b, 1),
                expected_cost_inr=cost_b,
                expected_net_return_inr=round(net_b, 2),
                risk_level="medium",
                water_stress_index=wsi,
                nitrogen_stress_index=0.15,
                modelled_estimate=True
            ).__dict__,
            ScenarioResult(
                id="C",
                label="Monitoring & Cultural Only (Do Nothing)",
                action="Drain excess standing water, pause nitrogen application, observe 48 hours",
                expected_yield_kgha=round(yield_c, 1),
                expected_cost_inr=cost_c,
                expected_net_return_inr=round(net_c, 2),
                risk_level="high",
                water_stress_index=wsi,
                nitrogen_stress_index=0.25,
                modelled_estimate=True
            ).__dict__
        ]
