import pytest
from backend.simulation.dssat import DSSATSimulator
from backend.simulation.interface import SimulationParams
from backend.simulation.rules import PhenologyRules, WaterStressRules, DiseaseFavorabilityRules


@pytest.mark.asyncio
async def test_dssat_simulator_scenarios():
    simulator = DSSATSimulator()
    params = SimulationParams(
        crop="rice",
        stage_code="tillering",
        gdd_accumulated=450.0,
        daily_temp_c=28.0,
        daily_rainfall_mm=5.0,
        relative_humidity_pct=82.0,
        disease_severity=0.30
    )
    
    res = await simulator.run_simulation(params)
    assert res["crop"] == "rice"
    assert "scenarios" in res
    assert len(res["scenarios"]) == 3
    
    sc_a = next(s for s in res["scenarios"] if s["id"] == "A")
    sc_c = next(s for s in res["scenarios"] if s["id"] == "C")
    
    # Scenario A should yield higher expected return than Scenario C
    assert sc_a["expected_yield_kgha"] > sc_c["expected_yield_kgha"]
    assert sc_a["expected_net_return_inr"] > sc_c["expected_net_return_inr"]
    assert sc_a["modelled_estimate"] is True


def test_phenology_gdd_calc():
    gdd = PhenologyRules.calculate_daily_gdd(crop="rice", temp_max=32.0, temp_min=24.0)
    assert gdd == 18.0  # (32+24)/2 - 10 = 28 - 10 = 18


def test_disease_favorability_dfi():
    dfi = DiseaseFavorabilityRules.calculate_dfi(relative_humidity_pct=85.0, temp_c=25.0, consecutive_wet_days=3)
    assert dfi >= 0.70
