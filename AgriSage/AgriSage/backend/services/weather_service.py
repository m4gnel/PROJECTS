import httpx
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any

logger = logging.getLogger(__name__)

# District coordinate lookup table for Kerala
KERALA_DISTRICT_COORDS: Dict[str, tuple[float, float]] = {
    "Thiruvananthapuram": (8.5241, 76.9366),
    "Kollam": (8.8932, 76.6141),
    "Pathanamthitta": (9.2648, 76.7870),
    "Alappuzha": (9.4981, 76.3388),
    "Kottayam": (9.5916, 76.5222),
    "Idukki": (9.8497, 76.9804),
    "Ernakulam": (9.9816, 76.2999),
    "Thrissur": (10.5276, 76.2144),
    "Palakkad": (10.7867, 76.6548),
    "Malappuram": (11.0732, 76.0740),
    "Kozhikode": (11.2588, 75.7804),
    "Wayanad": (11.6854, 76.1320),
    "Kannur": (11.8745, 75.3704),
    "Kasaragod": (12.5102, 74.9852)
}


@dataclass
class WeatherContext:
    temp_c: float
    humidity_pct: int
    rain_mm_24h: float
    rain_chance_pct: int
    wind_kmh: float
    advice_flag: str  # SPRAY_RISK | IRRIGATION_NEEDED | FLOOD_RISK | NORMAL
    cached: bool = False
    stale: bool = False


# In-memory cache for fast lookup & test execution
_WEATHER_CACHE: Dict[str, Dict[str, Any]] = {}


class WeatherService:
    def compute_advice_flag(self, humidity_pct: int, rain_mm_24h: float, temp_c: float) -> str:
        if rain_mm_24h > 50.0:
            return "FLOOD_RISK"
        if humidity_pct > 85 and rain_mm_24h < 2.0:
            return "SPRAY_RISK"
        if rain_mm_24h < 1.0 and temp_c > 32.0:
            return "IRRIGATION_NEEDED"
        return "NORMAL"

    async def get_weather(
        self,
        district: str = "Ernakulam",
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> WeatherContext:
        coords = KERALA_DISTRICT_COORDS.get(district, (9.9816, 76.2999))
        target_lat = lat if lat is not None else coords[0]
        target_lon = lon if lon is not None else coords[1]
        cache_key = f"{district}_{round(target_lat, 2)}_{round(target_lon, 2)}"

        # Check in-memory cache first (1 hour TTL)
        now = datetime.now(timezone.utc)
        if cache_key in _WEATHER_CACHE:
            cached_data = _WEATHER_CACHE[cache_key]
            if now < cached_data["expires_at"]:
                ctx = cached_data["context"]
                return WeatherContext(
                    temp_c=ctx.temp_c,
                    humidity_pct=ctx.humidity_pct,
                    rain_mm_24h=ctx.rain_mm_24h,
                    rain_chance_pct=ctx.rain_chance_pct,
                    wind_kmh=ctx.wind_kmh,
                    advice_flag=ctx.advice_flag,
                    cached=True,
                    stale=False
                )

        url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": target_lat,
            "longitude": target_lon,
            "hourly": "temperature_2m,precipitation,relative_humidity_2m,windspeed_10m,precipitation_probability",
            "forecast_days": 7,
            "timezone": "Asia/Kolkata"
        }

        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                resp = await client.get(url, params=params)
                if resp.status_code == 200:
                    data = resp.json()
                    hourly = data.get("hourly", {})
                    temps = hourly.get("temperature_2m", [28.0])
                    humidities = hourly.get("relative_humidity_2m", [80])
                    precip = hourly.get("precipitation", [0.0])
                    winds = hourly.get("windspeed_10m", [10.0])
                    precip_prob = hourly.get("precipitation_probability", [0])

                    temp_c = float(temps[0]) if temps else 28.0
                    humidity_pct = int(humidities[0]) if humidities else 80
                    rain_mm_24h = float(sum(precip[:24])) if precip else 0.0
                    rain_chance_pct = int(max(precip_prob[:12])) if precip_prob else 0
                    wind_kmh = float(winds[0]) if winds else 10.0

                    advice_flag = self.compute_advice_flag(humidity_pct, rain_mm_24h, temp_c)
                    context = WeatherContext(
                        temp_c=temp_c,
                        humidity_pct=humidity_pct,
                        rain_mm_24h=rain_mm_24h,
                        rain_chance_pct=rain_chance_pct,
                        wind_kmh=wind_kmh,
                        advice_flag=advice_flag,
                        cached=False,
                        stale=False
                    )

                    # Save to cache
                    _WEATHER_CACHE[cache_key] = {
                        "context": context,
                        "expires_at": now + timedelta(hours=1)
                    }
                    return context
        except Exception as e:
            logger.warning("weather_service_fetch_failed", error=str(e))
            if cache_key in _WEATHER_CACHE:
                cached_ctx = _WEATHER_CACHE[cache_key]["context"]
                return WeatherContext(
                    temp_c=cached_ctx.temp_c,
                    humidity_pct=cached_ctx.humidity_pct,
                    rain_mm_24h=cached_ctx.rain_mm_24h,
                    rain_chance_pct=cached_ctx.rain_chance_pct,
                    wind_kmh=cached_ctx.wind_kmh,
                    advice_flag=cached_ctx.advice_flag,
                    cached=True,
                    stale=True
                )

        # Fallback default
        return WeatherContext(
            temp_c=28.5,
            humidity_pct=82,
            rain_mm_24h=5.0,
            rain_chance_pct=30,
            wind_kmh=12.0,
            advice_flag="NORMAL",
            cached=False,
            stale=True
        )


weather_service = WeatherService()
