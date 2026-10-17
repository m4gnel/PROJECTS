from typing import Dict, Any


class PhenologyRules:
    """Growing Degree Days (GDD) phenological development rules."""

    CARDINAL_TEMPS = {
        "rice": {"t_base": 10.0, "t_opt": 30.0, "t_max": 40.0},
        "tomato": {"t_base": 10.0, "t_opt": 25.0, "t_max": 35.0},
        "potato": {"t_base": 7.0, "t_opt": 20.0, "t_max": 30.0},
        "corn": {"t_base": 10.0, "t_opt": 30.0, "t_max": 40.0},
    }

    @classmethod
    def calculate_daily_gdd(cls, crop: str, temp_max: float, temp_min: float) -> float:
        crop_clean = crop.strip().lower()
        temps = cls.CARDINAL_TEMPS.get(crop_clean, {"t_base": 10.0, "t_opt": 28.0, "t_max": 38.0})
        t_base = temps["t_base"]
        
        t_avg = (temp_max + temp_min) / 2.0
        if t_avg < t_base:
            return 0.0
        return round(t_avg - t_base, 2)


class WaterStressRules:
    """Evapotranspiration and Soil Moisture Water Stress Index (WSI) rules."""

    @classmethod
    def calculate_water_stress_index(cls, rainfall_mm: float, humidity_pct: float, temp_c: float) -> float:
        """Calculate Water Stress Index WSI (0.0 = zero stress, 1.0 = severe drought stress)."""
        # Potential Evapotranspiration (PET estimate in mm/day)
        pet = max(1.0, 0.0023 * (temp_c + 17.8) * (30.0 - temp_c * 0.2))
        water_deficit = max(0.0, pet - rainfall_mm)
        wsi = min(1.0, water_deficit / max(1.0, pet * 2.0))
        return round(wsi, 2)


class DiseaseFavorabilityRules:
    """Disease Favorability Index (DFI) calculation engine."""

    @classmethod
    def calculate_dfi(cls, relative_humidity_pct: float, temp_c: float, consecutive_wet_days: int) -> float:
        """Calculate DFI (0.0 to 1.0) based on micro-climate suitability."""
        # Optimal fungal spore germination range: 22°C - 28°C and RH > 80%
        temp_score = 1.0 if 22.0 <= temp_c <= 28.0 else max(0.2, 1.0 - abs(temp_c - 25.0) * 0.1)
        humidity_score = max(0.0, (relative_humidity_pct - 60.0) / 40.0)
        wetness_score = min(1.0, consecutive_wet_days * 0.3)
        
        dfi = (temp_score * 0.4) + (humidity_score * 0.4) + (wetness_score * 0.2)
        return round(min(1.0, max(0.0, dfi)), 2)
