"""
GET /api/v1/weather — Weather endpoints using real Open-Meteo data via WeatherService.
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query

from backend.services.weather_service import weather_service
from backend.dependencies import get_current_user
from backend.config import settings

try:
    import structlog
    logger = structlog.get_logger(__name__)
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

router = APIRouter(tags=["Weather & Micro-climate"])


@router.get(
    "/weather/current",
    summary="Current weather for a lat/lon or district",
    description=(
        "Returns real weather data from Open-Meteo API (1-hour in-memory cache). "
        "Accepts explicit lat/lon or falls back to district name lookup."
    ),
)
async def get_current_weather(
    lat: Optional[float] = Query(None, ge=6.0, le=38.0, description="Latitude (optional if district provided)"),
    lon: Optional[float] = Query(None, ge=68.0, le=97.5, description="Longitude (optional if district provided)"),
    lng: Optional[float] = Query(None, ge=68.0, le=97.5, description="Deprecated alias for lon"),
    district: str = Query("", description="District name (used if coordinates are not provided)"),
    state: str = Query("India", description="State or union territory name"),
    auth: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """Retrieve real current micro-climate data from Open-Meteo."""
    target_lon = lon if lon is not None else lng
    ctx = await weather_service.get_weather(state=state, district=district, lat=lat, lon=target_lon)

    farming_advisory = _get_farming_advisory(ctx.advice_flag)
    if ctx.stale:
        farming_advisory = (
            "Weather provider is unavailable and this is stale data. "
            "Do not make spray or irrigation decisions solely from this reading. "
            + farming_advisory
        )

    return {
        "location": {
            "lat": lat,
            "lng": target_lon,
            "lon": target_lon,
            "district": district,
            "state": state,
        },
        "temp_c": ctx.temp_c,
        "humidity_pct": ctx.humidity_pct,
        "rain_mm_24h": ctx.rain_mm_24h,
        "rain_chance_pct": ctx.rain_chance_pct,
        "wind_kmh": ctx.wind_kmh,
        "advice_flag": ctx.advice_flag,
        # Stale/unavailable weather is never an actionable spray signal.
        "spray_window_open": (
            not ctx.stale
            and ctx.available
            and ctx.advice_flag not in ("SPRAY_RISK", "FLOOD_RISK")
        ),
        "cached": ctx.cached,
        "stale": ctx.stale,
        "available": ctx.available,
        "farming_advisory": farming_advisory,
    }


@router.get(
    "/weather/forecast",
    summary="7-day weather forecast",
    description="Returns 7-day Open-Meteo forecast with farming condition indicators.",
)
async def get_weather_forecast(
    lat: Optional[float] = Query(None, ge=6.0, le=38.0),
    lon: Optional[float] = Query(None, ge=68.0, le=97.5),
    lng: Optional[float] = Query(None, ge=68.0, le=97.5, description="Deprecated alias for lon"),
    district: str = Query(""),
    state: str = Query("India"),
    days: int = Query(7, ge=1, le=14),
    auth: Dict[str, Any] = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """Return a provider-backed 7-day forecast, or an empty list if unavailable."""
    import httpx
    from backend.services.weather_service import resolve_coordinates

    # Resolve coords
    target_lon = lon if lon is not None else lng
    target_lat, target_lon = resolve_coordinates(
        state=state,
        district=district,
        lat=lat,
        lon=target_lon,
    )

    url = f"{settings.OPEN_METEO_BASE_URL.rstrip('/')}/forecast"
    params = {
        "latitude": target_lat,
        "longitude": target_lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,weathercode,windspeed_10m_max",
        "forecast_days": days,
        "timezone": "Asia/Kolkata",
    }

    try:
        async with httpx.AsyncClient(timeout=6.0) as client:
            resp = await client.get(url, params=params)
            if resp.status_code == 200:
                data = resp.json()
                daily = data.get("daily", {})
                dates = daily.get("time")
                max_temps = daily.get("temperature_2m_max")
                min_temps = daily.get("temperature_2m_min")
                precip_sums = daily.get("precipitation_sum")
                wind_speeds = daily.get("windspeed_10m_max")
                weathercodes = daily.get("weathercode")
                if any(not values for values in (dates, max_temps, min_temps, precip_sums, wind_speeds, weathercodes)):
                    raise ValueError("Open-Meteo response omitted required daily fields")

                forecast = []
                for i in range(min(days, len(dates))):
                    rain = float(precip_sums[i]) if i < len(precip_sums) else 0.0
                    max_t = float(max_temps[i])
                    min_t = float(min_temps[i])
                    wind = float(wind_speeds[i])
                    wc = int(weathercodes[i])
                    spray_open = rain < 2.0 and max_t < 35.0

                    # WMO weathercode → simple label
                    condition = _wmo_to_label(wc)

                    forecast.append({
                        "day_offset": i,
                        "date": dates[i] if i < len(dates) else "",
                        "temp_max_c": round(max_t, 1),
                        "temp_min_c": round(min_t, 1),
                        "rain_mm": round(rain, 1),
                        "wind_kmh": round(wind, 1),
                        "spray_window_open": spray_open,
                        "condition": condition,
                        "farming_tip": _day_farming_tip(rain, max_t, spray_open),
                    })
                return forecast
    except Exception as e:
        logger.warning("weather_forecast_api_failed", error=str(e))

    # A provider outage must not be represented as a forecast with invented
    # temperatures or rainfall values.
    return _fallback_forecast(days)


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _get_farming_advisory(advice_flag: str) -> str:
    mapping = {
        "FLOOD_RISK": "Heavy rain expected (>50mm). Ensure field drainage channels are clear. Delay all spraying operations.",
        "SPRAY_RISK": "High humidity conditions. Fungal disease risk elevated. Avoid spraying — wait for drier weather.",
        "IRRIGATION_NEEDED": "Low rainfall and high temperature detected. Irrigate crops within 24 hours to prevent moisture stress.",
        "NORMAL": "Conditions are within normal range. Standard farm operations can proceed.",
        "UNKNOWN": "Weather data is unavailable. Do not make spray or irrigation decisions from this reading.",
    }
    return mapping.get(advice_flag, mapping["UNKNOWN"])


def _wmo_to_label(code: int) -> str:
    if code == 0:
        return "Clear Sky"
    if code in (1, 2, 3):
        return "Partly Cloudy"
    if code in (45, 48):
        return "Foggy"
    if code in (51, 53, 55):
        return "Drizzle"
    if code in (61, 63, 65):
        return "Rain"
    if code in (71, 73, 75):
        return "Snowfall"
    if code in (80, 81, 82):
        return "Rain Showers"
    if code in (95, 96, 99):
        return "Thunderstorm"
    return "Cloudy"


def _day_farming_tip(rain_mm: float, max_temp: float, spray_open: bool) -> str:
    if rain_mm > 20:
        return "Heavy rain day — avoid field operations."
    if rain_mm > 5:
        return "Light rain expected — check drainage."
    if not spray_open:
        return "High humidity — delay chemical spraying."
    if max_temp > 35:
        return "Hot day — irrigate morning or evening."
    return "Good conditions for field work."


def _fallback_forecast(days: int) -> List[Dict[str, Any]]:
    """Return no forecast when Open-Meteo is unavailable."""
    return []
