import uuid
from datetime import datetime, date
from typing import List, Optional
from sqlalchemy import (
    Column, String, Boolean, Integer, Float, Date, DateTime,
    ForeignKey, CheckConstraint, Index, UniqueConstraint, func, ARRAY, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from backend.database import Base


class FieldObservation(Base):
    __tablename__ = "field_observations"
    __table_args__ = (
        Index("idx_observations_field", "field_id", "observed_at"),
        Index("idx_observations_type", "observation_type", "observed_at"),
        Index("idx_observations_severity", "severity_estimate"),
        {"schema": "intelligence"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey("core.fields.id", ondelete="CASCADE"), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id", ondelete="CASCADE"), nullable=False)
    observed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    observation_type = Column(String(50), nullable=False)
    description_native = Column(Text, nullable=False)
    description_en = Column(Text, nullable=True)
    severity_estimate = Column(String(20), default="info")
    area_affected_pct = Column(Float, nullable=True)

    photo_url = Column(Text, nullable=True)
    photo_analysis = Column(JSONB, nullable=True)
    detected_disease = Column(String, nullable=True)
    detected_pest = Column(String, nullable=True)
    confidence_pct = Column(Float, nullable=True)

    triggered_advisory = Column(UUID(as_uuid=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class CropStage(Base):
    __tablename__ = "crop_stages"
    __table_args__ = (
        UniqueConstraint("field_id", "crop_name", "season_year"),
        Index("idx_crop_stages_field", "field_id"),
        Index("idx_crop_stages_harvest", "predicted_harvest_date"),
        {"schema": "intelligence"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey("core.fields.id", ondelete="CASCADE"), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id"), nullable=False)
    crop_name = Column(String, nullable=False)
    crop_variety = Column(String, nullable=True)
    season = Column(String(20), nullable=True)
    season_year = Column(Integer, nullable=False)

    current_stage = Column(String(50), nullable=False)
    stage_started_at = Column(Date, nullable=True)
    next_stage = Column(String(50), nullable=True)
    next_stage_eta_days = Column(Integer, nullable=True)
    days_since_sowing = Column(Integer, nullable=True)

    predicted_yield_kg_ha = Column(Float, nullable=True)
    predicted_harvest_date = Column(Date, nullable=True)
    yield_confidence_pct = Column(Float, nullable=True)
    simulated_at = Column(DateTime(timezone=True), nullable=True)
    dssat_scenario = Column(JSONB, nullable=True)

    cumulative_et_mm = Column(Float, nullable=True)
    water_stress_index = Column(Float, nullable=True)
    heat_stress_index = Column(Float, nullable=True)

    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())


class IrrigationSchedule(Base):
    __tablename__ = "irrigation_schedules"
    __table_args__ = (
        UniqueConstraint("field_id", "valid_for_date"),
        Index("idx_irrigation_field_date", "field_id", "valid_for_date"),
        Index("idx_irrigation_due", "valid_for_date", postgresql_where=Column("should_irrigate") == True),
        {"schema": "intelligence"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey("core.fields.id", ondelete="CASCADE"), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id"), nullable=False)
    generated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    valid_for_date = Column(Date, nullable=False)

    should_irrigate = Column(Boolean, nullable=False)
    reason = Column(Text, nullable=False)
    reason_native = Column(Text, nullable=True)
    next_irrigation_date = Column(Date, nullable=True)
    irrigation_amount_mm = Column(Float, nullable=True)
    irrigation_duration_hours = Column(Float, nullable=True)

    et0_mm = Column(Float, nullable=True)
    kc_factor = Column(Float, nullable=True)
    etc_mm = Column(Float, nullable=True)
    soil_moisture_pct = Column(Float, nullable=True)
    field_capacity_pct = Column(Float, nullable=True)
    wilting_point_pct = Column(Float, nullable=True)
    rain_forecast_mm = Column(Float, default=0)

    was_followed = Column(Boolean, nullable=True)
    farmer_notes = Column(Text, nullable=True)


class FertiliserPlan(Base):
    __tablename__ = "fertiliser_plans"
    __table_args__ = (
        UniqueConstraint("field_id", "crop_stage", "application_date"),
        Index("idx_fertiliser_field", "field_id", "application_date"),
        Index("idx_fertiliser_due", "application_date", postgresql_where=Column("was_followed") == None),
        {"schema": "intelligence"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey("core.fields.id", ondelete="CASCADE"), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id"), nullable=False)
    crop_name = Column(String, nullable=False)
    crop_stage = Column(String(50), nullable=False)
    generated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    application_date = Column(Date, nullable=False)

    nitrogen_kg_acre = Column(Float, nullable=True)
    phosphorus_kg_acre = Column(Float, nullable=True)
    potassium_kg_acre = Column(Float, nullable=True)

    primary_fertiliser = Column(String, nullable=True)
    primary_dose_kg_acre = Column(Float, nullable=True)
    secondary_fertiliser = Column(String, nullable=True)
    secondary_dose_kg_acre = Column(Float, nullable=True)
    micronutrient_needed = Column(String, nullable=True)

    application_method = Column(String(50), nullable=True)
    best_time_of_day = Column(String(30), nullable=True)
    avoid_if_rain = Column(Boolean, default=False)

    rationale = Column(Text, nullable=False)
    rationale_native = Column(Text, nullable=True)
    source_doc = Column(String, nullable=True)

    was_followed = Column(Boolean, nullable=True)
