import httpx
import uuid
import logging
from datetime import datetime, timezone, timedelta

logger = logging.getLogger(__name__)

# Default Kerala locations to cache weather for
KERALA_LOCATIONS = [
    (10.1632, 76.3986),  # Ernakulam
    (8.5241, 76.9366),   # Thiruvananthapuram
    (11.2588, 75.7804),  # Kozhikode
]


async def run_weather_pipeline():
    """Fetch weather for major Kerala locations and cache in DB."""
    try:
        from ..database import AsyncSessionLocal
        from ..models.chat import ChatMessage  # just to test DB connection
        from sqlalchemy import text
        tz = timezone(timedelta(hours=5, minutes=30))

        for lat, lon in KERALA_LOCATIONS:
            params = {
                "latitude": lat, "longitude": lon,
                "hourly": "temperature_2m,precipitation,windspeed_10m,uv_index,relativehumidity_2m",
                "forecast_days": 1, "timezone": "Asia/Kolkata",
            }
            async with httpx.AsyncClient(timeout=10) as client:
                resp = await client.get("https://api.open-meteo.com/v1/forecast", params=params)
                data = resp.json()

            hourly = data.get("hourly", {})
            temps = hourly.get("temperature_2m", [28.0])
            humidity = hourly.get("relativehumidity_2m", [70])
            rain = hourly.get("precipitation", [0.0])
            wind = hourly.get("windspeed_10m", [10.0])
            uv = hourly.get("uv_index", [5.0])

            async with AsyncSessionLocal() as session:
                await session.execute(text("""
                    INSERT INTO weather_cache (id, lat, lon, temperature_c, humidity_percent,
                        rainfall_mm, wind_kmh, uv_index, weather_condition, source, fetched_at)
                    VALUES (:id, :lat, :lon, :temp, :humidity, :rain, :wind, :uv, :cond, :src, NOW())
                """), {
                    "id": str(uuid.uuid4()), "lat": lat, "lon": lon,
                    "temp": temps[0] if temps else 28.0,
                    "humidity": int(humidity[0]) if humidity else 70,
                    "rain": float(rain[0]) if rain else 0.0,
                    "wind": float(wind[0]) if wind else 10.0,
                    "uv": float(uv[0]) if uv else 5.0,
                    "cond": "Partly Cloudy", "src": "open-meteo",
                })
                await session.commit()
        logger.info("weather_pipeline: completed for %d locations", len(KERALA_LOCATIONS))
    except Exception as e:
        logger.error("weather_pipeline error: %s", str(e))
