"""
GET /api/v1/weather — Weather endpoints using real Open-Meteo data via WeatherService.
"""
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Depends, Query

from backend.services.weather_service import weather_service
from backend.dependencies import require_auth

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
    lat: Optional[float] = Query(None, description="Latitude (optional if district provided)"),
    lng: Optional[float] = Query(None, description="Longitude (optional if district provided)"),
    district: str = Query("Ernakulam", description="District name (used if lat/lon not provided)"),
    state: str = Query("Kerala", description="State name"),
    auth: Dict[str, Any] = Depends(require_auth),
) -> Dict[str, Any]:
    """Retrieve real current micro-climate data from Open-Meteo."""
    ctx = await weather_service.get_weather(district=district, lat=lat, lon=lng)

    return {
        "location": {
            "lat": lat,
            "lng": lng,
            "district": district,
            "state": state,
        },
        "temp_c": ctx.temp_c,
        "humidity_pct": ctx.humidity_pct,
        "rain_mm_24h": ctx.rain_mm_24h,
        "rain_chance_pct": ctx.rain_chance_pct,
        "wind_kmh": ctx.wind_kmh,
        "advice_flag": ctx.advice_flag,
        "spray_window_open": ctx.advice_flag not in ("SPRAY_RISK", "FLOOD_RISK"),
        "cached": ctx.cached,
        "stale": ctx.stale,
        "farming_advisory": _get_farming_advisory(ctx.advice_flag),
    }


@router.get(
    "/weather/forecast",
    summary="7-day weather forecast",
    description="Returns 7-day Open-Meteo forecast with farming condition indicators.",
)
async def get_weather_forecast(
    lat: Optional[float] = Query(None),
    lng: Optional[float] = Query(None),
    district: str = Query("Ernakulam"),
    state: str = Query("Kerala"),
    days: int = Query(7, ge=1, le=14),
    auth: Dict[str, Any] = Depends(require_auth),
) -> List[Dict[str, Any]]:
    """Returns 7-day forecast. Falls back to deterministic estimates if API unavailable."""
    import httpx
    from backend.services.weather_service import KERALA_DISTRICT_COORDS

    # Resolve coords
    coords = KERALA_DISTRICT_COORDS.get(district, (9.9816, 76.2999))
    target_lat = lat if lat is not None else coords[0]
    target_lon = lng if lng is not None else coords[1]

    url = "https://api.open-meteo.com/v1/forecast"
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
                dates = daily.get("time", [])
                max_temps = daily.get("temperature_2m_max", [])
                min_temps = daily.get("temperature_2m_min", [])
                precip_sums = daily.get("precipitation_sum", [])
                wind_speeds = daily.get("windspeed_10m_max", [])
                weathercodes = daily.get("weathercode", [])

                forecast = []
                for i in range(min(days, len(dates))):
                    rain = float(precip_sums[i]) if i < len(precip_sums) else 0.0
                    max_t = float(max_temps[i]) if i < len(max_temps) else 30.0
                    min_t = float(min_temps[i]) if i < len(min_temps) else 22.0
                    wind = float(wind_speeds[i]) if i < len(wind_speeds) else 10.0
                    wc = int(weathercodes[i]) if i < len(weathercodes) else 0
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

    # Fallback — deterministic estimates
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
    }
    return mapping.get(advice_flag, "Conditions are within normal range.")


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
    """Returns a safe deterministic fallback when Open-Meteo is unavailable."""
    import datetime
    today = datetime.date.today()
    result = []
    for i in range(days):
        day = today + datetime.timedelta(days=i)
        result.append({
            "day_offset": i,
            "date": str(day),
            "temp_max_c": 30.0,
            "temp_min_c": 22.0,
            "rain_mm": 0.0,
            "wind_kmh": 10.0,
            "spray_window_open": True,
            "condition": "Partly Cloudy",
            "farming_tip": "Forecast unavailable — monitor local conditions.",
        })
    return result
