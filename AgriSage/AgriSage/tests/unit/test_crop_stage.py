import pytest
from backend.agents.crop_stage import CropStageAgent


def compute_gdd(tmax: float, tmin: float, crop: str) -> float:
    base_temps = {"rice": 10.0, "maize": 10.0, "tomato": 10.0, "banana": 15.0, "coconut": 20.0}
    base = base_temps.get(crop, 10.0)
    avg_temp = (tmax + tmin) / 2.0
    return max(0.0, avg_temp - base)


class TestGDDCalculation:
    def test_rice_gdd_formula(self):
        gdd = compute_gdd(tmax=30.0, tmin=22.0, crop="rice")
        assert gdd == pytest.approx(16.0, abs=0.1)  # ((30+22)/2) - 10 = 16

    def test_gdd_below_base_returns_zero(self):
        gdd = compute_gdd(tmax=12.0, tmin=8.0, crop="rice")
        assert gdd == 0.0  # Never negative

    def test_banana_different_base_temp(self):
        gdd = compute_gdd(tmax=30.0, tmin=22.0, crop="banana")
        assert gdd == pytest.approx(11.0, abs=0.1)  # ((30+22)/2) - 15 = 11

    def test_rice_tillering_at_260_gdd(self):
        agent = CropStageAgent()
        result = agent.estimate_stage(crop="rice", cumulative_gdd=260.0)
        assert result.stage_code == "tillering"
        assert result.vulnerability == "high"

    def test_rice_flowering_at_700_gdd(self):
        agent = CropStageAgent()
        result = agent.estimate_stage(crop="rice", cumulative_gdd=700.0)
        assert result.stage_code == "flowering"
        assert result.vulnerability == "critical"
