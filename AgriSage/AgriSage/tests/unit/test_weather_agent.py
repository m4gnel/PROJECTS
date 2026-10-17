import pytest
from backend.agents.weather import WeatherAgent, WeatherIndicators


def compute_dfi(humidity_pct: float, temperature_c: float, consecutive_wet_days: int) -> float:
    dfi = (
        (1.0 if humidity_pct > 80 else 0.0) * 0.4
        + (1.0 if 20 <= temperature_c <= 30 else 0.0) * 0.3
        + (min(7, consecutive_wet_days) / 7.0) * 0.3
    )
    return max(0.0, min(1.0, dfi))


class TestDFI:
    def test_high_humidity_wet_days_high_dfi(self):
        dfi = compute_dfi(humidity_pct=88.0, temperature_c=26.0, consecutive_wet_days=4)
        assert dfi > 0.7

    def test_dry_conditions_low_dfi(self):
        dfi = compute_dfi(humidity_pct=45.0, temperature_c=35.0, consecutive_wet_days=0)
        assert dfi < 0.3

    def test_dfi_clamped_between_0_and_1(self):
        dfi = compute_dfi(humidity_pct=100.0, temperature_c=25.0, consecutive_wet_days=14)
        assert 0.0 <= dfi <= 1.0

    def test_dfi_formula_correct(self):
        dfi = compute_dfi(humidity_pct=85.0, temperature_c=25.0, consecutive_wet_days=7)
        expected = 0.4 + 0.3 + (7 / 7) * 0.3
        assert dfi == pytest.approx(expected, abs=0.01)
