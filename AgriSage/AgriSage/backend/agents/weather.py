import time
import httpx
from typing import Dict, Any, Tuple, Optional
from pydantic import BaseModel
from backend.agents.state import AgriSAGEState
from backend.config import settings


class WeatherIndicators(BaseModel):
    temperature_c: float
    humidity_pct: float
    consecutive_wet_days: int
    dfi: float
    spray_window: Optional[str] = None
    provider: str = "open_meteo"


def _unavailable_weather() -> Dict[str, Any]:
    return {
        "temperature_c": 0.0,
        "humidity_pct": 0.0,
        "consecutive_wet_days": 0,
        "dfi": 0.0,
        "spray_window": None,
        "provider": "unavailable",
        "safe_to_act": False,
        "warning": "Weather data is unavailable; do not make field-treatment decisions from this result.",
    }



class WeatherAgent:
    _cache: Dict[Tuple[float, float], Tuple[float, Dict[str, Any]]] = {}

    async def run(self, state: AgriSAGEState) -> AgriSAGEState:
        farm_state = state.get("farm_state") or {}
        lat = farm_state.get("location_lat") or 10.8505
        lon = farm_state.get("location_lon") or 76.2711

        cache_key = (round(float(lat), 2), round(float(lon), 2))
        now_ts = time.time()

        # Check cache (30 minutes = 1800 seconds)
        if cache_key in self._cache and (now_ts - self._cache[cache_key][0]) < 1800:
            weather_result = self._cache[cache_key][1]
        else:
            weather_result = await self._fetch_open_meteo(float(lat), float(lon))
            self._cache[cache_key] = (now_ts, weather_result)

        state["weather_result"] = weather_result
        return state

    async def _fetch_open_meteo(self, lat: float, lon: float) -> Dict[str, Any]:
        url = f"{settings.OPEN_METEO_BASE_URL.rstrip('/')}/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,relative_humidity_2m,precipitation_probability,windspeed_10m",
            "daily": "precipitation_sum,temperature_2m_max,temperature_2m_min",
            "forecast_days": 7
        }
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(url, params=params)
                if res.status_code == 200:
                    data = res.json()
                    return self._process_weather_data(data)
        except Exception:
            pass

        # Fail closed instead of presenting synthetic weather as an observation
        # that could drive spraying or irrigation decisions.
        return _unavailable_weather()

    def _process_weather_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        daily = data.get("daily", {})
        hourly = data.get("hourly", {})

        required = (
            daily.get("precipitation_sum"),
            daily.get("temperature_2m_max"),
            daily.get("temperature_2m_min"),
            hourly.get("temperature_2m"),
            hourly.get("relative_humidity_2m"),
            hourly.get("precipitation_probability"),
            hourly.get("windspeed_10m"),
        )
        if any(not isinstance(values, list) or not values for values in required):
            return _unavailable_weather()

        precip_sums = daily["precipitation_sum"]

        # Compute consecutive wet days
        consecutive_wet_days = 0
        for p in precip_sums:
            if p > 1.0:
                consecutive_wet_days += 1
            else:
                break

        temps = hourly["temperature_2m"]
        humidities = hourly["relative_humidity_2m"]
        rain_probs = hourly["precipitation_probability"]
        winds = hourly["windspeed_10m"]

        current_temp = temps[0]
        current_humidity = humidities[0]

        # Compute DFI (Disease Favorability Index) exact formula from prompt:
        # dfi = ((humidity_pct > 80) * 0.4 + (20 <= temperature_c <= 30) * 0.3 + (consecutive_wet_days / 7) * 0.3)
        h_flag = 1.0 if current_humidity > 80 else 0.0
        t_flag = 1.0 if (20 <= current_temp <= 30) else 0.0
        w_factor = min(1.0, consecutive_wet_days / 7.0)

        dfi = (h_flag * 0.4) + (t_flag * 0.3) + (w_factor * 0.3)
        dfi = max(0.0, min(1.0, dfi))

        # Spray window calculation
        spray_window = "07:00 AM - 11:00 AM" if (rain_probs[0] < 20 and winds[0] < 15) else None

        return {
            "temperature_c": current_temp,
            "humidity_pct": current_humidity,
            "consecutive_wet_days": consecutive_wet_days,
            "dfi": round(dfi, 2),
            "spray_window": spray_window,
            "provider": "open_meteo"
        }
