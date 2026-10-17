import pytest
from app.schemas.weather import WeatherCurrent, WeatherForecast, WeatherDay


def test_weather_current_schema():
    data = {
        "latitude": 10.165,
        "longitude": 76.401,
        "temperature_c": 29.5,
        "humidity_percent": 78,
        "rainfall_mm": 2.3,
        "wind_kmh": 12.4,
        "uv_index": 7.2,
        "weather_condition": "Partly Cloudy",
        "agri_advisory": "Good day for spraying.",
        "fetched_at": "2026-10-01T08:30:00+05:30"
    }
    obj = WeatherCurrent(**data)
    assert obj.temperature_c == 29.5
    assert obj.humidity_percent == 78


def test_weather_forecast_schema():
    day = {
        "date": "2026-10-01",
        "max_temp_c": 32.1,
        "min_temp_c": 24.8,
        "rainfall_mm": 5.0,
        "weather_condition": "Rain",
        "uv_index": 5.0,
        "agri_note": "Avoid harvesting"
    }
    obj = WeatherDay(**day)
    assert obj.max_temp_c == 32.1
    forecast = WeatherForecast(latitude=10.165, longitude=76.401, forecast=[obj], fetched_at="2026-10-01T08:30:00+05:30")
    assert len(forecast.forecast) == 1
