import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import (
    Column, String, Boolean, Integer, Float, Numeric, Date, DateTime, Time,
    ForeignKey, CheckConstraint, Index, UniqueConstraint, func, ARRAY, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from backend.database import Base


class WeatherCache(Base):
    __tablename__ = "weather_cache"
    __table_args__ = (
        UniqueConstraint("state", "district"),
        Index("idx_weather_district", "state", "district"),
        Index("idx_weather_expires", "expires_at"),
        Index("idx_weather_fetched", "fetched_at"),
        {"schema": "realtime"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)

    temp_c = Column(Float, nullable=False)
    feels_like_c = Column(Float, nullable=True)
    humidity_pct = Column(Integer, nullable=True)
    wind_kmh = Column(Float, nullable=True)
    wind_direction_deg = Column(Integer, nullable=True)
    rain_mm_1h = Column(Float, default=0)
    rain_mm_24h = Column(Float, default=0)
    uv_index = Column(Float, nullable=True)
    cloud_cover_pct = Column(Integer, nullable=True)
    visibility_km = Column(Float, nullable=True)
    weather_code = Column(Integer, nullable=True)
    weather_description = Column(String, nullable=True)

    advice_flag = Column(String, default="NORMAL")
    spray_window_open = Column(Boolean, default=True)
    field_work_suitable = Column(Boolean, default=True)

    fetched_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)
    source = Column(String, nullable=False, default="open-meteo")


class WeatherForecast(Base):
    __tablename__ = "weather_forecasts"
    __table_args__ = (
        UniqueConstraint("state", "district", "forecast_date"),
        Index("idx_forecasts_location_date", "state", "district", "forecast_date"),
        Index("idx_forecasts_expires", "expires_at"),
        {"schema": "realtime"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    forecast_date = Column(Date, nullable=False)
    temp_max_c = Column(Float, nullable=True)
    temp_min_c = Column(Float, nullable=True)
    precipitation_mm = Column(Float, default=0)
    rain_probability_pct = Column(Integer, nullable=True)
    wind_max_kmh = Column(Float, nullable=True)
    uv_index_max = Column(Float, nullable=True)
    weather_code = Column(Integer, nullable=True)
    weather_description = Column(String, nullable=True)
    sunrise_time = Column(Time, nullable=True)
    sunset_time = Column(Time, nullable=True)
    daylight_hours = Column(Float, nullable=True)

    spray_suitable = Column(Boolean, nullable=True)
    irrigation_needed = Column(Boolean, nullable=True)
    field_work_suitable = Column(Boolean, nullable=True)

    fetched_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=False)


class MarketPrice(Base):
    __tablename__ = "market_prices"
    __table_args__ = (
        UniqueConstraint("crop_name", "market_name", "district", "state", "price_date"),
        Index("idx_market_crop_state_date", "crop_name", "state", "price_date"),
        Index("idx_market_district", "district", "state", "price_date"),
        {"schema": "realtime"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop_name = Column(String, nullable=False)
    crop_variety = Column(String, nullable=True)
    market_name = Column(String, nullable=False)
    district = Column(String, nullable=False)
    state = Column(String, nullable=False)
    price_date = Column(Date, nullable=False)

    min_price = Column(Numeric(10, 2), nullable=True)
    max_price = Column(Numeric(10, 2), nullable=True)
    modal_price = Column(Numeric(10, 2), nullable=True)
    msp_price = Column(Numeric(10, 2), nullable=True)
    above_msp = Column(Boolean, nullable=True)

    trend_7d = Column(String(20), nullable=True)
    trend_30d = Column(String(20), nullable=True)
    pct_change_7d = Column(Float, nullable=True)
    recommendation = Column(String(30), nullable=True)

    fetched_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    source = Column(String, nullable=False, default="data.gov.in")


class PestAlert(Base):
    __tablename__ = "pest_alerts"
    __table_args__ = (
        Index("idx_pest_severity", "severity", "fetched_at"),
        Index("idx_pest_states", "affected_states", postgresql_using="gin"),
        Index("idx_pest_districts", "affected_districts", postgresql_using="gin"),
        Index("idx_pest_expires", "expires_at"),
        {"schema": "realtime"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    external_id = Column(String, unique=True, nullable=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    full_content = Column(Text, nullable=True)
    severity = Column(String(20), nullable=False, default="warning")

    affected_states = Column(ARRAY(Text), default=[])
    affected_districts = Column(ARRAY(Text), default=[])
    is_national = Column(Boolean, default=False)

    pest_name = Column(String, nullable=True)
    pest_scientific = Column(String, nullable=True)
    damage_type = Column(String, nullable=True)

    source_url = Column(String, nullable=True)
    source_org = Column(String, default="NBAIR")
    published_at = Column(DateTime(timezone=True), nullable=True)
    fetched_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    expires_at = Column(DateTime(timezone=True), nullable=True)

    crops = relationship("PestAlertCrop", back_populates="alert", cascade="all, delete-orphan")


class PestAlertCrop(Base):
    __tablename__ = "pest_alert_crops"
    __table_args__ = (
        Index("idx_pest_alert_crops_crop", "crop_name"),
        {"schema": "realtime"}
    )

    alert_id = Column(UUID(as_uuid=True), ForeignKey("realtime.pest_alerts.id", ondelete="CASCADE"), primary_key=True)
    crop_name = Column(String, primary_key=True)
    affinity_score = Column(Float, nullable=True)

    alert = relationship("PestAlert", back_populates="crops")


class SoilZone(Base):
    __tablename__ = "soil_zones"
    __table_args__ = (
        UniqueConstraint("state", "district"),
        Index("idx_soil_state_district", "state", "district"),
        Index("idx_soil_suitable_crops", "suitable_crops", postgresql_using="gin"),
        Index("idx_soil_zone", "agroclimatic_zone"),
        {"schema": "realtime"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    agroclimatic_zone = Column(String(50), nullable=True)

    primary_texture = Column(String(50), nullable=False)
    secondary_texture = Column(String(50), nullable=True)
    ph_min = Column(Float, nullable=False)
    ph_max = Column(Float, nullable=False)
    ph_optimal = Column(Float, nullable=True)
    organic_carbon = Column(String(20), nullable=False, default="medium")
    cec_meq = Column(Float, nullable=True)

    nitrogen_status = Column(String(20), nullable=False, default="medium")
    phosphorus_status = Column(String(20), nullable=False, default="medium")
    potassium_status = Column(String(20), nullable=False, default="high")

    zinc_deficient = Column(Boolean, default=False)
    boron_deficient = Column(Boolean, default=False)
    sulphur_deficient = Column(Boolean, default=False)
    iron_deficient = Column(Boolean, default=False)

    water_holding_capacity = Column(String(20), nullable=True)
    drainage = Column(String(20), nullable=True)
    annual_rainfall_mm_avg = Column(Float, nullable=True)

    suitable_crops = Column(ARRAY(Text), nullable=False, default=[])
    unsuitable_crops = Column(ARRAY(Text), default=[])
    special_notes = Column(Text, nullable=True)

    data_source = Column(String, default="NBSS&LUP")
    data_year = Column(Integer, default=2024)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class IMDRainfall(Base):
    __tablename__ = "imd_rainfall"
    __table_args__ = (
        UniqueConstraint("state", "district", "reading_date"),
        Index("idx_rainfall_location_date", "state", "district", "reading_date"),
        {"schema": "realtime"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    reading_date = Column(Date, nullable=False)
    rainfall_mm = Column(Float, nullable=False, default=0)
    normal_rainfall_mm = Column(Float, nullable=True)
    departure_pct = Column(Float, nullable=True)
    is_deficient = Column(Boolean, nullable=True)
    is_excess = Column(Boolean, nullable=True)
    season = Column(String(20), nullable=True)
    cumulative_mm = Column(Float, nullable=True)
    source = Column(String, default="IMD")
    fetched_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class NDVIReading(Base):
    __tablename__ = "ndvi_readings"
    __table_args__ = (
        UniqueConstraint("field_id", "reading_date"),
        Index("idx_ndvi_field_date", "field_id", "reading_date"),
        Index("idx_ndvi_farmer_date", "farmer_id", "reading_date"),
        Index("idx_ndvi_health", "health_category"),
        {"schema": "realtime"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey("core.fields.id", ondelete="CASCADE"), nullable=True)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id", ondelete="CASCADE"), nullable=False)
    lat = Column(Float, nullable=False)
    lon = Column(Float, nullable=False)
    reading_date = Column(Date, nullable=False)

    ndvi = Column(Float, nullable=True)
    evi = Column(Float, nullable=True)
    pixel_reliability = Column(Integer, nullable=True)
    is_cloud_affected = Column(Boolean, default=False)

    health_category = Column(String(30), nullable=True)
    health_score = Column(Integer, nullable=True)
    stress_type = Column(String(50), nullable=True)

    satellite_product = Column(String, default="MOD13Q1")
    spatial_resolution_m = Column(Integer, default=250)
    source = Column(String, default="NASA-EOSDIS")
    fetched_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class MSPReference(Base):
    __tablename__ = "msp_reference"
    __table_args__ = (
        UniqueConstraint("crop_name", "season", "msp_year"),
        {"schema": "realtime"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop_name = Column(String, nullable=False)
    season = Column(String(20), nullable=False)
    msp_year = Column(String(20), nullable=False)
    msp_per_quintal = Column(Numeric(10, 2), nullable=False)
    announced_by = Column(String, default="CACP")
    effective_from = Column(Date, nullable=True)
    source = Column(String, default="Ministry of Agriculture & Farmers Welfare")
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
