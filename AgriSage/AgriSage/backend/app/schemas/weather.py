from pydantic import BaseModel
from datetime import datetime
from typing import List


class WeatherDay(BaseModel):
    date: str
    max_temp_c: float
    min_temp_c: float
    rainfall_mm: float
    weather_condition: str
    uv_index: float
    agri_note: str


class WeatherCurrent(BaseModel):
    latitude: float
    longitude: float
    temperature_c: float
    humidity_percent: int
    rainfall_mm: float
    wind_kmh: float
    uv_index: float
    weather_condition: str
    agri_advisory: str
    fetched_at: datetime


class WeatherForecast(BaseModel):
    latitude: float
    longitude: float
    forecast: List[WeatherDay]
    fetched_at: datetime
