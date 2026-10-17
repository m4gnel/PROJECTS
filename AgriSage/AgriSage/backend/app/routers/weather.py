from fastapi import APIRouter, Query
from datetime import datetime, timezone, timedelta
import httpx
from ..schemas.weather import WeatherCurrent, WeatherForecast, WeatherDay

router = APIRouter()


def _get_tz():
    return timezone(timedelta(hours=5, minutes=30))


@router.get("/current", response_model=WeatherCurrent)
async def get_current_weather(lat: float = Query(...), lon: float = Query(...)):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m,precipitation,windspeed_10m,uv_index,relativehumidity_2m",
        "forecast_days": 1,
        "timezone": "Asia/Kolkata",
    }
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            data = resp.json()
        hourly = data.get("hourly", {})
        temps = hourly.get("temperature_2m", [28.0])
        humidity = hourly.get("relativehumidity_2m", [70])
        rain = hourly.get("precipitation", [0.0])
        wind = hourly.get("windspeed_10m", [10.0])
        uv = hourly.get("uv_index", [5.0])
        temp_c = temps[0] if temps else 28.0
        humidity_pct = int(humidity[0]) if humidity else 70
        rain_mm = float(rain[0]) if rain else 0.0
        wind_kmh = float(wind[0]) if wind else 10.0
        uv_idx = float(uv[0]) if uv else 5.0
        condition = "Partly Cloudy"
        if rain_mm > 5:
            condition = "Rainy"
        elif uv_idx > 7:
            condition = "Sunny"
        advisory = "Monitor crops for weather-related stress."
        if rain_mm > 10:
            advisory = "Heavy rain expected. Avoid field operations."
        elif humidity_pct > 80:
            advisory = "High humidity — monitor for fungal disease."
    except Exception:
        temp_c, humidity_pct, rain_mm, wind_kmh, uv_idx = 28.0, 70, 0.0, 10.0, 5.0
        condition = "Data unavailable"
        advisory = "Weather data unavailable. Check conditions manually."

    return WeatherCurrent(
        latitude=lat, longitude=lon, temperature_c=temp_c,
        humidity_percent=humidity_pct, rainfall_mm=rain_mm, wind_kmh=wind_kmh,
        uv_index=uv_idx, weather_condition=condition, agri_advisory=advisory,
        fetched_at=datetime.now(_get_tz()),
    )


@router.get("/forecast", response_model=WeatherForecast)
async def get_weather_forecast(lat: float = Query(...), lon: float = Query(...)):
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat, "longitude": lon,
        "daily": "temperature_2m_max,temperature_2m_min,precipitation_sum,uv_index_max",
        "forecast_days": 7, "timezone": "Asia/Kolkata",
    }
    days = []
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            resp = await client.get(url, params=params)
            data = resp.json()
        daily = data.get("daily", {})
        dates = daily.get("time", [])
        for i, d in enumerate(dates):
            rain = daily.get("precipitation_sum", [0]*7)[i] or 0.0
            uv = daily.get("uv_index_max", [5]*7)[i] or 5.0
            note = "Good for field work"
            if rain > 20:
                note = "Avoid harvesting — heavy rain expected"
            elif rain > 5:
                note = "Light rain possible — plan accordingly"
            days.append(WeatherDay(
                date=d,
                max_temp_c=daily.get("temperature_2m_max", [32]*7)[i] or 32.0,
                min_temp_c=daily.get("temperature_2m_min", [24]*7)[i] or 24.0,
                rainfall_mm=rain,
                weather_condition="Rain" if rain > 5 else "Sunny",
                uv_index=uv,
                agri_note=note,
            ))
    except Exception:
        pass

    return WeatherForecast(latitude=lat, longitude=lon, forecast=days, fetched_at=datetime.now(_get_tz()))
