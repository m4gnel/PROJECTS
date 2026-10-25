from typing import Optional, List, Any
from datetime import date, datetime, time
from pydantic import BaseModel, Field, ConfigDict


# ==========================================
# Core Schema Pydantic Models
# ==========================================

class FarmerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    phone: Optional[str] = Field(None, pattern=r"^[6-9][0-9]{9}$")
    phone_verified: bool = False
    country: str = "India"
    state: str = Field(..., min_length=2, max_length=60)
    district: str = Field(..., min_length=2, max_length=60)
    taluk: Optional[str] = None
    village: Optional[str] = None
    pincode: Optional[str] = Field(None, pattern=r"^[1-9][0-9]{5}$")
    lat: Optional[float] = Field(None, ge=6.0, le=38.0)
    lon: Optional[float] = Field(None, ge=68.0, le=97.5)
    location_accuracy_m: Optional[float] = None
    primary_language: str = "hi"
    secondary_language: Optional[str] = None
    crops: List[str] = []
    agroclimatic_zone: Optional[str] = None
    onboarding_complete: bool = False
    demo_mode: bool = False


class FarmerCreate(FarmerBase):
    pass


class FarmerResponse(FarmerBase):
    id: str
    farmer_code: str
    fcm_topic: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class FCMTokenCreate(BaseModel):
    token: str
    device_id: Optional[str] = None
    device_model: Optional[str] = None


class FCMTokenResponse(FCMTokenCreate):
    id: str
    farmer_id: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Realtime Schema Pydantic Models
# ==========================================

class WeatherCacheResponse(BaseModel):
    id: str
    state: str
    district: str
    lat: float
    lon: float
    temp_c: float
    feels_like_c: Optional[float] = None
    humidity_pct: Optional[int] = None
    wind_kmh: Optional[float] = None
    wind_direction_deg: Optional[int] = None
    rain_mm_1h: float = 0
    rain_mm_24h: float = 0
    uv_index: Optional[float] = None
    cloud_cover_pct: Optional[int] = None
    visibility_km: Optional[float] = None
    weather_code: Optional[int] = None
    weather_description: Optional[str] = None
    advice_flag: str = "NORMAL"
    spray_window_open: bool = True
    field_work_suitable: bool = True
    fetched_at: datetime
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MarketPriceResponse(BaseModel):
    id: str
    crop_name: str
    crop_variety: Optional[str] = None
    market_name: str
    district: str
    state: str
    price_date: date
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    modal_price: Optional[float] = None
    msp_price: Optional[float] = None
    above_msp: Optional[bool] = None
    trend_7d: Optional[str] = None
    recommendation: Optional[str] = None
    fetched_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PestAlertResponse(BaseModel):
    id: str
    external_id: Optional[str] = None
    title: str
    description: Optional[str] = None
    severity: str
    affected_states: List[str] = []
    affected_districts: List[str] = []
    pest_name: Optional[str] = None
    pest_scientific: Optional[str] = None
    source_org: str = "NBAIR"
    published_at: Optional[datetime] = None
    fetched_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SoilZoneResponse(BaseModel):
    id: str
    state: str
    district: str
    agroclimatic_zone: Optional[str] = None
    primary_texture: str
    secondary_texture: Optional[str] = None
    ph_min: float
    ph_max: float
    ph_optimal: Optional[float] = None
    organic_carbon: str
    nitrogen_status: str
    phosphorus_status: str
    potassium_status: str
    suitable_crops: List[str] = []

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Agent & Advisory Pydantic Models
# ==========================================

class AdvisorySessionCreate(BaseModel):
    farmer_id: str
    language: str = "hi"
    state: str
    district: str
    primary_crop: Optional[str] = None
    active_field_id: Optional[str] = None


class AdvisorySessionResponse(AdvisorySessionCreate):
    id: str
    session_token: str
    is_active: bool
    message_count: int
    started_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AdvisoryMessageCreate(BaseModel):
    session_id: str
    farmer_id: str
    role: str
    sequence_no: int
    content_native: str
    content_en: Optional[str] = None
    language: str


class AdvisoryMessageResponse(AdvisoryMessageCreate):
    id: str
    agents_used: List[str] = []
    intent_detected: List[str] = []
    confidence_score: Optional[float] = None
    response_ms: Optional[int] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class KauDocumentResponse(BaseModel):
    id: str
    source_file: str
    source_org: str
    crop_name: str
    chunk_index: int
    content: str
    doc_type: Optional[str] = None
    ingested_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Field Intelligence & Alerts Pydantic Models
# ==========================================

class FieldObservationCreate(BaseModel):
    field_id: str
    farmer_id: str
    observation_type: str
    description_native: str
    description_en: Optional[str] = None
    severity_estimate: str = "info"
    area_affected_pct: Optional[float] = None
    photo_url: Optional[str] = None


class FieldObservationResponse(FieldObservationCreate):
    id: str
    detected_disease: Optional[str] = None
    detected_pest: Optional[str] = None
    confidence_pct: Optional[float] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FarmerAlertResponse(BaseModel):
    id: str
    farmer_id: str
    category: str
    severity: str
    title_native: str
    title_en: str
    body_native: str
    body_en: str
    language: str
    action_type: Optional[str] = None
    is_read: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MarketRecommendationResponse(BaseModel):
    id: str
    farmer_id: str
    crop_name: str
    state: str
    district: str
    current_modal_price: Optional[float] = None
    recommendation: str
    rationale: str
    target_price: Optional[float] = None
    valid_until: Optional[date] = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Core Farms & Fields Pydantic Models
# ==========================================

class CoreFarmBase(BaseModel):
    name: str = "My Farm"
    total_area_acres: float = Field(..., gt=0, lt=10000)
    ownership_type: Optional[str] = None
    land_record_number: Optional[str] = None
    state: str
    district: str
    taluk: Optional[str] = None
    village: Optional[str] = None
    lat: Optional[float] = Field(None, ge=6.0, le=38.0)
    lon: Optional[float] = Field(None, ge=68.0, le=97.5)
    primary_soil_type: Optional[str] = None
    avg_ph: Optional[float] = Field(None, ge=3.0, le=10.0)
    water_source: str = "rain_fed"
    annual_rainfall_mm: Optional[float] = None


class CoreFarmCreate(CoreFarmBase):
    farmer_id: str


class CoreFarmResponse(CoreFarmBase):
    id: str
    farmer_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CoreFieldBase(BaseModel):
    name: str
    area_acres: float = Field(..., gt=0, lt=500)
    status: str = "active"
    current_crop: Optional[str] = None
    crop_variety: Optional[str] = None
    sowing_date: Optional[datetime] = None
    expected_harvest: Optional[datetime] = None
    current_stage: str = "fallow"
    soil_texture: Optional[str] = None
    soil_ph: Optional[float] = Field(None, ge=3.0, le=10.0)
    organic_carbon_pct: Optional[float] = Field(None, ge=0.0, le=10.0)
    nitrogen_status: str = "medium"
    phosphorus_status: str = "medium"
    potassium_status: str = "medium"
    irrigation_type: str = "rain_fed"
    has_drip: bool = False
    lat: Optional[float] = Field(None, ge=6.0, le=38.0)
    lon: Optional[float] = Field(None, ge=68.0, le=97.5)
    boundary_geojson: Optional[dict] = None


class CoreFieldCreate(CoreFieldBase):
    farm_id: str
    farmer_id: str


class CoreFieldResponse(CoreFieldBase):
    id: str
    farm_id: str
    farmer_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Realtime Forecast, IMD, NDVI & MSP Models
# ==========================================

class WeatherForecastResponse(BaseModel):
    id: str
    state: str
    district: str
    forecast_date: date
    temp_max_c: Optional[float] = None
    temp_min_c: Optional[float] = None
    precipitation_mm: float = 0
    rain_probability_pct: Optional[int] = None
    wind_max_kmh: Optional[float] = None
    uv_index_max: Optional[float] = None
    weather_code: Optional[int] = None
    weather_description: Optional[str] = None
    sunrise_time: Optional[time] = None
    sunset_time: Optional[time] = None
    daylight_hours: Optional[float] = None
    spray_suitable: Optional[bool] = None
    irrigation_needed: Optional[bool] = None
    field_work_suitable: Optional[bool] = None
    fetched_at: datetime
    expires_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IMDRainfallResponse(BaseModel):
    id: str
    state: str
    district: str
    reading_date: date
    rainfall_mm: float
    normal_rainfall_mm: Optional[float] = None
    departure_pct: Optional[float] = None
    is_deficient: Optional[bool] = None
    is_excess: Optional[bool] = None
    season: Optional[str] = None
    cumulative_mm: Optional[float] = None
    source: str = "IMD"
    fetched_at: datetime

    model_config = ConfigDict(from_attributes=True)


class NDVIReadingResponse(BaseModel):
    id: str
    field_id: Optional[str] = None
    farmer_id: str
    lat: float
    lon: float
    reading_date: date
    ndvi: Optional[float] = None
    evi: Optional[float] = None
    pixel_reliability: Optional[int] = None
    is_cloud_affected: bool = False
    health_category: Optional[str] = None
    health_score: Optional[int] = None
    stress_type: Optional[str] = None
    satellite_product: str = "MOD13Q1"
    spatial_resolution_m: int = 250
    source: str = "NASA-EOSDIS"
    fetched_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MSPReferenceResponse(BaseModel):
    id: str
    crop_name: str
    season: str
    msp_year: str
    msp_per_quintal: float
    announced_by: str = "CACP"
    effective_from: Optional[date] = None
    source: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Agents Execution & State Models
# ==========================================

class AgentInvocationResponse(BaseModel):
    id: str
    message_id: str
    session_id: str
    farmer_id: str
    agent_name: str
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_ms: Optional[int] = None
    succeeded: bool = True
    error_type: Optional[str] = None
    error_message: Optional[str] = None
    input_summary: Optional[dict] = None
    output_summary: Optional[dict] = None
    gemini_calls: int = 0
    gemini_tokens: int = 0
    cache_hit: bool = False

    model_config = ConfigDict(from_attributes=True)


class LangGraphCheckpointResponse(BaseModel):
    thread_id: str
    checkpoint_ns: str
    checkpoint_id: str
    checkpoint: dict
    metadata_: dict = Field(default={}, alias="metadata")
    parent_checkpoint_id: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


# ==========================================
# Field Intelligence DSSAT & Schedules Models
# ==========================================

class CropStageResponse(BaseModel):
    id: str
    field_id: str
    farmer_id: str
    crop_name: str
    crop_variety: Optional[str] = None
    season: Optional[str] = None
    season_year: int
    current_stage: str
    stage_started_at: Optional[date] = None
    next_stage: Optional[str] = None
    next_stage_eta_days: Optional[int] = None
    days_since_sowing: Optional[int] = None
    predicted_yield_kg_ha: Optional[float] = None
    predicted_harvest_date: Optional[date] = None
    yield_confidence_pct: Optional[float] = None
    simulated_at: Optional[datetime] = None
    cumulative_et_mm: Optional[float] = None
    water_stress_index: Optional[float] = None
    heat_stress_index: Optional[float] = None
    updated_at: datetime
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class IrrigationScheduleResponse(BaseModel):
    id: str
    field_id: str
    farmer_id: str
    generated_at: datetime
    valid_for_date: date
    should_irrigate: bool
    reason: str
    reason_native: Optional[str] = None
    next_irrigation_date: Optional[date] = None
    irrigation_amount_mm: Optional[float] = None
    irrigation_duration_hours: Optional[float] = None
    et0_mm: Optional[float] = None
    kc_factor: Optional[float] = None
    etc_mm: Optional[float] = None
    soil_moisture_pct: Optional[float] = None
    rain_forecast_mm: float = 0
    was_followed: Optional[bool] = None
    farmer_notes: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class FertiliserPlanResponse(BaseModel):
    id: str
    field_id: str
    farmer_id: str
    crop_name: str
    crop_stage: str
    generated_at: datetime
    application_date: date
    nitrogen_kg_acre: Optional[float] = None
    phosphorus_kg_acre: Optional[float] = None
    potassium_kg_acre: Optional[float] = None
    primary_fertiliser: Optional[str] = None
    primary_dose_kg_acre: Optional[float] = None
    secondary_fertiliser: Optional[str] = None
    secondary_dose_kg_acre: Optional[float] = None
    micronutrient_needed: Optional[str] = None
    application_method: Optional[str] = None
    best_time_of_day: Optional[str] = None
    avoid_if_rain: bool = False
    rationale: str
    rationale_native: Optional[str] = None
    source_doc: Optional[str] = None
    was_followed: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Alerts FCM Log & Market Subscriptions
# ==========================================

class FCMDeliveryLogResponse(BaseModel):
    id: str
    alert_id: str
    farmer_id: str
    fcm_token: str
    fcm_message_id: Optional[str] = None
    topic: Optional[str] = None
    status: str
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    sent_at: datetime
    delivered_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class PriceSubscriptionResponse(BaseModel):
    id: str
    farmer_id: str
    crop_name: str
    state: str
    alert_above: Optional[float] = None
    alert_below: Optional[float] = None
    is_active: bool = True
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# Analytics & Feedback Models
# ==========================================

class FarmSeasonAnalyticsResponse(BaseModel):
    id: str
    farm_id: str
    farmer_id: str
    crop_name: str
    season: str
    season_year: int
    total_queries: int = 0
    queries_about_pest: int = 0
    queries_about_weather: int = 0
    queries_about_market: int = 0
    queries_about_soil: int = 0
    advisories_followed: int = 0
    advisories_ignored: int = 0
    critical_alerts_received: int = 0
    alerts_acted_upon: int = 0
    actual_yield_kg_ha: Optional[float] = None
    dssat_predicted_yield: Optional[float] = None
    yield_accuracy_pct: Optional[float] = None
    sold_price_per_quintal: Optional[float] = None
    total_revenue_inr: Optional[float] = None
    overall_satisfaction: Optional[int] = None
    nps_score: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AgentPerformanceResponse(BaseModel):
    id: str
    agent_name: str
    metric_date: date
    total_invocations: int = 0
    successful: int = 0
    failed: int = 0
    success_rate_pct: Optional[float] = None
    avg_duration_ms: Optional[float] = None
    p50_duration_ms: Optional[float] = None
    p95_duration_ms: Optional[float] = None
    p99_duration_ms: Optional[float] = None
    total_gemini_calls: int = 0
    total_tokens_used: int = 0
    cache_hit_count: int = 0
    cache_hit_rate_pct: Optional[float] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class PlatformMetricsResponse(BaseModel):
    id: str
    metric_date: date
    dau: int = 0
    new_registrations: int = 0
    total_registered: int = 0
    total_queries: int = 0
    avg_response_ms: Optional[float] = None
    p95_response_ms: Optional[float] = None
    total_agent_calls: int = 0
    gemini_calls_total: int = 0
    gemini_tokens_total: int = 0
    alerts_sent: int = 0
    fcm_success_rate_pct: Optional[float] = None
    error_count: int = 0
    error_rate_pct: Optional[float] = None
    weather_cache_hits: int = 0
    market_cache_hits: int = 0
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AdvisoryFeedbackResponse(BaseModel):
    id: str
    message_id: str
    session_id: str
    farmer_id: str
    rating: int
    feedback_text: Optional[str] = None
    feedback_text_en: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


# ==========================================
# System Audit & Rate Limit Models
# ==========================================

class AuditLogResponse(BaseModel):
    id: str
    table_schema: str
    table_name: str
    operation: str
    record_id: Optional[str] = None
    farmer_id: Optional[str] = None
    old_data: Optional[dict] = None
    new_data: Optional[dict] = None
    changed_fields: Optional[List[str]] = None
    performed_at: datetime

    model_config = ConfigDict(from_attributes=True)


class APIRateLimitResponse(BaseModel):
    farmer_id: str
    window_start: datetime
    window_minutes: int = 60
    request_count: int = 1
    max_allowed: int = 100
    is_limited: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)
