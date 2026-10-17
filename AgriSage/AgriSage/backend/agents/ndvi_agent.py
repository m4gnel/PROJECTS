"""
NDVIAgent (Agent 13) — NASA EarthData satellite crop health index.
Retrieves MODIS NDVI (MOD13Q1, 250m, 16-day product) for farmer's fields.
Uses NASA EarthData AppEEARS API (free signup). Falls back to synthetic
estimate from weather data when API unavailable or no token configured.
"""
import logging
from typing import Dict, Any, Optional

import httpx

from backend.agents.state import AgriSageState
from backend.config import settings

logger = logging.getLogger(__name__)

# NDVI in-memory cache: keyed by "lat_lon_rounded"
_NDVI_CACHE: Dict[str, Dict[str, Any]] = {}


def _synthetic_ndvi_from_weather(weather: Dict[str, Any]) -> float:
    """
    Deterministic NDVI proxy from weather context when API unavailable.
    NDVI range: 0.0 (bare soil) to 1.0 (dense vegetation).
    Uses rainfall and temperature as proxies for greenness.
    """
    rain = weather.get("rain_mm_24h", 5.0)
    temp = weather.get("temp_c", 28.0)
    advice_flag = weather.get("advice_flag", "NORMAL")

    base = 0.55  # Typical Kerala tropical vegetation baseline
    if advice_flag == "FLOOD_RISK":
        base -= 0.10  # Waterlogging stress
    elif advice_flag == "IRRIGATION_NEEDED":
        base -= 0.12  # Drought stress
    if rain > 10:
        base += 0.05  # Recent rain boosts green cover
    if temp > 38:
        base -= 0.08  # Heat stress

    return round(max(0.1, min(0.95, base)), 3)


def _interpret_ndvi(ndvi: float) -> Dict[str, str]:
    """Map NDVI value to crop health label and farming recommendation."""
    if ndvi >= 0.7:
        return {
            "health": "Excellent",
            "label": "Dense healthy vegetation",
            "recommendation": "Crop is performing well. Maintain current management practices.",
        }
    if ndvi >= 0.5:
        return {
            "health": "Good",
            "label": "Moderate-to-good vegetation cover",
            "recommendation": "Crop health is good. Monitor for pest or disease signs.",
        }
    if ndvi >= 0.3:
        return {
            "health": "Fair",
            "label": "Sparse or stressed vegetation",
            "recommendation": "Vegetation stress detected. Check irrigation and soil moisture.",
        }
    return {
        "health": "Poor",
        "label": "Low vegetation / possible crop stress",
        "recommendation": "Significant stress detected. Inspect field for disease, drought, or pest damage.",
    }


async def _fetch_ndvi_appeears(
    lat: float,
    lon: float,
    token: str,
) -> Optional[float]:
    """
    Attempt to fetch NDVI from NASA EarthData AppEEARS point sample API.
    Product: MOD13Q1.061 (MODIS 250m, 16-day NDVI).
    Returns float NDVI value or None if unavailable.
    """
    url = "https://appeears.earthdatacloud.nasa.gov/api/point"
    headers = {"Authorization": f"Bearer {token}"}
    params = {
        "product": "MOD13Q1.061",
        "layer": "_250m_16_days_NDVI",
        "latitude": lat,
        "longitude": lon,
    }
    try:
        async with httpx.AsyncClient(timeout=8.0) as client:
            resp = await client.get(url, headers=headers, params=params)
            if resp.status_code == 200:
                data = resp.json()
                # Extract latest NDVI value from response
                values = data.get("value", [])
                if values:
                    raw = float(values[-1].get("value", 0))
                    # MODIS NDVI is scaled by 10000
                    ndvi = raw / 10000.0 if raw > 1.0 else raw
                    return round(ndvi, 3)
    except Exception as e:
        logger.warning("ndvi_appeears_fetch_failed", error=str(e))
    return None


async def ndvi_node(state: AgriSageState) -> Dict[str, Any]:
    """
    NDVIAgent: Satellite crop health index using NASA MODIS NDVI.
    16-day product update cycle, 250m resolution.
    """
    location = state.get("location", {})
    lat = location.get("lat") if isinstance(location, dict) else None
    lon = location.get("lon") if isinstance(location, dict) else None
    weather = state.get("weather_context", {})

    ndvi_value: Optional[float] = None

    # Try live AppEEARS API if token configured and coordinates available
    token = getattr(settings, "NASA_EARTHDATA_TOKEN", "")
    if token and lat and lon:
        cache_key = f"{round(lat, 2)}_{round(lon, 2)}"
        import datetime
        now = datetime.datetime.now(datetime.timezone.utc)

        if cache_key in _NDVI_CACHE:
            cached = _NDVI_CACHE[cache_key]
            age_days = (now - cached["fetched_at"]).days
            if age_days < 16:  # MODIS product is 16-day
                ndvi_value = cached["ndvi"]
                logger.debug("ndvi_cache_hit", cache_key=cache_key, age_days=age_days)

        if ndvi_value is None:
            ndvi_value = await _fetch_ndvi_appeears(lat, lon, token)
            if ndvi_value is not None:
                _NDVI_CACHE[cache_key] = {"ndvi": ndvi_value, "fetched_at": now}

    # Fallback: synthetic NDVI from weather context
    if ndvi_value is None:
        ndvi_value = _synthetic_ndvi_from_weather(weather)
        source = "synthetic_weather_proxy"
    else:
        source = "nasa_modis_mod13q1"

    interpretation = _interpret_ndvi(ndvi_value)

    res_dict = {
        "ndvi": ndvi_value,
        "health": interpretation["health"],
        "label": interpretation["label"],
        "recommendation": interpretation["recommendation"],
        "source": source,
        "product": "MOD13Q1 (250m, 16-day)",
    }

    logger.info("ndvi_agent_complete", ndvi=ndvi_value, health=interpretation["health"], source=source)

    return {
        "agent_outputs": {"ndvi": res_dict}
    }
