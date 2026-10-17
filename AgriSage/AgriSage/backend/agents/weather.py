import time
import httpx
from typing import Dict, Any, Tuple, Optional
from pydantic import BaseModel
from backend.agents.state import AgriSAGEState


class WeatherIndicators(BaseModel):
    temperature_c: float
    humidity_pct: float
    consecutive_wet_days: int
    dfi: float
    spray_window: Optional[str] = None
    provider: str = "open_meteo"



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
        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "hourly": "temperature_2m,relativehumidity_2m,precipitation_probability,windspeed_10m",
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

        # Fallback default values if API call fails
        return {
            "temperature_c": 27.5,
            "humidity_pct": 82.0,
            "consecutive_wet_days": 3,
            "dfi": 0.83,
            "spray_window": "07:00 AM - 11:00 AM",
            "provider": "open_meteo_fallback"
        }

    def _process_weather_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        daily = data.get("daily", {})
        hourly = data.get("hourly", {})

        precip_sums = daily.get("precipitation_sum", [0])
        tmax = daily.get("temperature_2m_max", [30])
        tmin = daily.get("temperature_2m_min", [22])

        # Compute consecutive wet days
        consecutive_wet_days = 0
        for p in precip_sums:
            if p > 1.0:
                consecutive_wet_days += 1
            else:
                break

        temps = hourly.get("temperature_2m", [27])
        humidities = hourly.get("relativehumidity_2m", [80])
        rain_probs = hourly.get("precipitation_probability", [0])
        winds = hourly.get("windspeed_10m", [5])

        current_temp = temps[0] if temps else 27.0
        current_humidity = humidities[0] if humidities else 80.0

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
