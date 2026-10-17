import httpx
from .state import AgriState


async def weather_node(state: AgriState) -> dict:
    """
    Fetches from Open-Meteo API using state.location_lat, state.location_lon.
    Returns: {"weather_data": WeatherData, "agents_completed": ["weather"]}
    Never raises — returns error in error_messages on failure.
    """
    try:
        params = {
            "latitude": state["location_lat"],
            "longitude": state["location_lon"],
            "hourly": "temperature_2m,precipitation,windspeed_10m,uv_index,relativehumidity_2m",
            "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum",
            "forecast_days": 7,
            "timezone": "Asia/Kolkata",
        }
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get("https://api.open-meteo.com/v1/forecast", params=params)
            data = resp.json()

        hourly = data.get("hourly", {})
        daily = data.get("daily", {})
        temps = hourly.get("temperature_2m", [28.0])
        humidity = hourly.get("relativehumidity_2m", [70.0])
        rain = hourly.get("precipitation", [0.0])
        wind = hourly.get("windspeed_10m", [10.0])
        uv = hourly.get("uv_index", [5.0])
        dates = daily.get("time", [])
        max_t = daily.get("temperature_2m_max", [])
        min_t = daily.get("temperature_2m_min", [])
        rain_d = daily.get("precipitation_sum", [])

        forecast_7day = [
            {"date": dates[i], "max_temp": max_t[i] if i < len(max_t) else 32.0,
             "min_temp": min_t[i] if i < len(min_t) else 24.0,
             "rainfall_mm": rain_d[i] if i < len(rain_d) else 0.0}
            for i in range(len(dates))
        ]

        weather_data = {
            "temperature": temps[0] if temps else 28.0,
            "humidity": float(humidity[0]) if humidity else 70.0,
            "rainfall_mm": float(rain[0]) if rain else 0.0,
            "wind_speed": float(wind[0]) if wind else 10.0,
            "uv_index": float(uv[0]) if uv else 5.0,
            "forecast_7day": forecast_7day,
        }
        return {"weather_data": weather_data, "agents_completed": ["weather"]}
    except Exception as e:
        return {"error_messages": [f"weather: {str(e)}"], "agents_completed": ["weather"]}
