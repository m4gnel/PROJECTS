from typing import TypedDict, Annotated, Optional
from operator import add


class WeatherData(TypedDict):
    temperature: float          # Celsius
    humidity: float             # percentage
    rainfall_mm: float
    wind_speed: float           # km/h
    uv_index: float
    forecast_7day: list[dict]   # [{date, max_temp, min_temp, rainfall_mm}]


class SoilData(TypedDict):
    soil_type: str              # "laterite", "alluvial", "red_loam", "coastal_sandy"
    ph: float
    nitrogen_kg_ha: float
    phosphorus_kg_ha: float
    potassium_kg_ha: float
    organic_matter_percent: float


class CropInfo(TypedDict):
    crop_name: str              # e.g., "rice", "coconut", "banana", "pepper"
    variety: str
    sowing_date: str            # ISO format YYYY-MM-DD
    current_growth_stage: str
    field_area_hectares: float


class AgriState(TypedDict):
    # Input
    query: str
    language: str               # "ml", "en", "ta", "hi"
    farmer_id: str
    field_id: Optional[str]
    location_lat: float
    location_lon: float
    crop_info: Optional[CropInfo]

    # Data collected by agents (Annotated[list, add] = append-only)
    weather_data: Optional[WeatherData]
    soil_data: Optional[SoilData]
    ndvi_value: Optional[float]       # -1.0 to 1.0 from satellite
    pest_alerts: Annotated[list[str], add]
    market_prices: Annotated[list[dict], add]
    dssat_result: Optional[dict]      # crop simulation output

    # Intermediate results (Annotated[list, add] = append-only)
    agent_findings: Annotated[list[str], add]

    # Final output
    advisory_text: str          # in the farmer's language
    alerts_generated: Annotated[list[dict], add]
    confidence_score: float     # 0.0 to 1.0

    # Routing
    agents_needed: list[str]    # set by orchestrator
    agents_completed: Annotated[list[str], add]
    error_messages: Annotated[list[str], add]
