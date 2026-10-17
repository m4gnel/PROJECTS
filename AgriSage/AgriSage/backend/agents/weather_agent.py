import logging
from typing import Dict, Any
from backend.agents.state import AgriSageState
from backend.services.weather_service import weather_service

logger = logging.getLogger(__name__)


async def weather_node(state: AgriSageState) -> Dict[str, Any]:
    location = state.get("location", {})
    district = location.get("district", "Ernakulam") if isinstance(location, dict) else "Ernakulam"
    lat = location.get("lat") if isinstance(location, dict) else None
    lon = location.get("lon") if isinstance(location, dict) else None

    ctx = await weather_service.get_weather(district=district, lat=lat, lon=lon)
    res_dict = {
        "temp_c": ctx.temp_c,
        "humidity_pct": ctx.humidity_pct,
        "rain_mm_24h": ctx.rain_mm_24h,
        "rain_chance_pct": ctx.rain_chance_pct,
        "wind_kmh": ctx.wind_kmh,
        "advice_flag": ctx.advice_flag,
        "cached": ctx.cached,
        "stale": ctx.stale
    }

    return {
        "weather_context": res_dict,
        "weather_result": res_dict,
        "agent_outputs": {"weather": res_dict}
    }
