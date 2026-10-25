import httpx
import logging
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from backend.config import settings

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

# State/UT centroids keep the service useful across India when a device has
# not yet supplied precise coordinates. These are fallbacks, not field-level
# measurements; device coordinates always take precedence.
INDIA_STATE_COORDS: Dict[str, tuple[float, float]] = {
    "andaman and nicobar islands": (11.7401, 92.6586),
    "andhra pradesh": (15.9129, 79.7400),
    "arunachal pradesh": (28.2180, 94.7278),
    "assam": (26.2006, 92.9376),
    "bihar": (25.0961, 85.3131),
    "chandigarh": (30.7333, 76.7794),
    "chhattisgarh": (21.2787, 81.8661),
    "dadra and nagar haveli and daman and diu": (20.1809, 73.0169),
    "delhi": (28.7041, 77.1025),
    "goa": (15.2993, 74.1240),
    "gujarat": (22.2587, 71.1924),
    "haryana": (29.0588, 76.0856),
    "himachal pradesh": (31.1048, 77.1734),
    "jammu and kashmir": (33.7782, 76.5762),
    "jharkhand": (23.6102, 85.2799),
    "karnataka": (15.3173, 75.7139),
    "kerala": (10.8505, 76.2711),
    "ladakh": (34.1526, 77.5771),
    "lakshadweep": (10.5667, 72.6417),
    "madhya pradesh": (22.9734, 78.6569),
    "maharashtra": (19.7515, 75.7139),
    "manipur": (24.6637, 93.9063),
    "meghalaya": (25.4670, 91.3662),
    "mizoram": (23.1645, 92.9376),
    "nagaland": (26.1584, 94.5624),
    "odisha": (20.9517, 85.0985),
    "puducherry": (11.9416, 79.8083),
    "punjab": (31.1471, 75.3412),
    "rajasthan": (27.0238, 74.2179),
    "sikkim": (27.5330, 88.5122),
    "tamil nadu": (11.1271, 78.6569),
    "telangana": (18.1124, 79.0193),
    "tripura": (23.9408, 91.9882),
    "uttar pradesh": (26.8467, 80.9462),
    "uttarakhand": (30.0668, 79.0193),
    "west bengal": (22.9868, 87.8550),
}

INDIA_CENTROID = (22.5937, 78.9629)


def _normalise_location(value: str | None) -> str:
    return " ".join((value or "").casefold().split())


def resolve_coordinates(
    *,
    state: str = "India",
    district: str = "",
    lat: Optional[float] = None,
    lon: Optional[float] = None,
) -> tuple[float, float]:
    """Resolve safe weather coordinates without assuming Kerala."""

    district_key = next(
        (name for name in KERALA_DISTRICT_COORDS if _normalise_location(name) == _normalise_location(district)),
        None,
    )
    fallback = KERALA_DISTRICT_COORDS[district_key] if district_key else INDIA_STATE_COORDS.get(
        _normalise_location(state), INDIA_CENTROID
    )
    return (lat if lat is not None else fallback[0], lon if lon is not None else fallback[1])


@dataclass
class WeatherContext:
    temp_c: float
    humidity_pct: int
    rain_mm_24h: float
    rain_chance_pct: int
    wind_kmh: float
    advice_flag: str  # SPRAY_RISK | IRRIGATION_NEEDED | FLOOD_RISK | NORMAL | UNKNOWN
    cached: bool = False
    stale: bool = False
    available: bool = True


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
        state: str = "India",
        district: str = "",
        lat: Optional[float] = None,
        lon: Optional[float] = None
    ) -> WeatherContext:
        target_lat, target_lon = resolve_coordinates(
            state=state,
            district=district,
            lat=lat,
            lon=lon,
        )
        cache_key = (
            f"{_normalise_location(state)}_{_normalise_location(district)}_"
            f"{round(target_lat, 2)}_{round(target_lon, 2)}"
        )

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
                    stale=False,
                    available=ctx.available,
                )

        url = f"{settings.OPEN_METEO_BASE_URL.rstrip('/')}/forecast"
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
                    temps = hourly.get("temperature_2m")
                    humidities = hourly.get("relative_humidity_2m")
                    precip = hourly.get("precipitation")
                    winds = hourly.get("windspeed_10m")
                    precip_prob = hourly.get("precipitation_probability")
                    if any(not values for values in (temps, humidities, precip, winds, precip_prob)):
                        raise ValueError("Open-Meteo response omitted required hourly fields")

                    temp_c = float(temps[0])
                    humidity_pct = int(humidities[0])
                    rain_mm_24h = float(sum(precip[:24]))
                    rain_chance_pct = int(max(precip_prob[:12]))
                    wind_kmh = float(winds[0])

                    advice_flag = self.compute_advice_flag(humidity_pct, rain_mm_24h, temp_c)
                    context = WeatherContext(
                        temp_c=temp_c,
                        humidity_pct=humidity_pct,
                        rain_mm_24h=rain_mm_24h,
                        rain_chance_pct=rain_chance_pct,
                        wind_kmh=wind_kmh,
                        advice_flag=advice_flag,
                        cached=False,
                        stale=False,
                        available=True,
                    )

                    # Save to cache
                    _WEATHER_CACHE[cache_key] = {
                        "context": context,
                        "expires_at": now + timedelta(hours=1)
                    }
                    return context
        except Exception as e:
            logger.warning("weather_service_fetch_failed: %s", e)
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
                    stale=True,
                    available=cached_ctx.available,
                )

        # Do not turn a provider outage into synthetic weather that could drive
        # an irrigation or spray decision.  Numeric zeroes are compatibility
        # sentinels for existing clients; ``available`` and ``advice_flag`` are
        # the authoritative state.
        return WeatherContext(
            temp_c=0.0,
            humidity_pct=0,
            rain_mm_24h=0.0,
            rain_chance_pct=0,
            wind_kmh=0.0,
            advice_flag="UNKNOWN",
            cached=False,
            stale=True,
            available=False,
        )


weather_service = WeatherService()
