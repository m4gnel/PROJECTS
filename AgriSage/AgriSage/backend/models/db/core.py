import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import (
    Column, String, Boolean, Integer, Float, DateTime, ForeignKey, CheckConstraint, Index, UniqueConstraint, func, ARRAY, Text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from backend.database import Base


class Farmer(Base):
    __tablename__ = "farmers"
    __table_args__ = (
        Index("idx_farmers_phone", "phone", postgresql_where=Column("phone") != None),
        Index("idx_farmers_state_district", "state", "district"),
        Index("idx_farmers_crops", "crops", postgresql_using="gin"),
        Index("idx_farmers_location", "lat", "lon", postgresql_where=Column("lat") != None),
        Index("idx_farmers_active", "last_active_at", postgresql_where=Column("deleted_at") == None),
        Index("idx_farmers_fcm_topic", "fcm_topic"),
        {"schema": "core"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_code = Column(String, unique=True, nullable=False)
    name = Column(String(100), nullable=False)
    phone = Column(String(10), unique=True, nullable=True)
    phone_verified = Column(Boolean, nullable=False, default=False)

    country = Column(String, nullable=False, default="India")
    state = Column(String(60), nullable=False)
    district = Column(String(60), nullable=False)
    taluk = Column(String, nullable=True)
    village = Column(String, nullable=True)
    pincode = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    location_accuracy_m = Column(Float, nullable=True)

    primary_language = Column(String(10), nullable=False, default="hi")
    secondary_language = Column(String(10), nullable=True)
    crops = Column(ARRAY(Text), nullable=False, default=[])
    agroclimatic_zone = Column(String(50), nullable=True)

    onboarding_complete = Column(Boolean, nullable=False, default=False)
    demo_mode = Column(Boolean, nullable=False, default=False)
    fcm_topic = Column(String, nullable=True)

    app_version = Column(String, nullable=True)
    device_model = Column(String, nullable=True)
    android_api_level = Column(Integer, nullable=True)
    last_active_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    farms = relationship("CoreFarm", back_populates="farmer", cascade="all, delete-orphan")
    fields = relationship("CoreField", back_populates="farmer", cascade="all, delete-orphan")
    fcm_tokens = relationship("FCMToken", back_populates="farmer", cascade="all, delete-orphan")


class FCMToken(Base):
    __tablename__ = "fcm_tokens"
    __table_args__ = (
        UniqueConstraint("farmer_id", "token"),
        Index("idx_fcm_tokens_farmer", "farmer_id", postgresql_where=Column("is_active") == True),
        {"schema": "core"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id", ondelete="CASCADE"), nullable=False)
    token = Column(Text, nullable=False)
    device_id = Column(Text, nullable=True)
    device_model = Column(Text, nullable=True)
    is_active = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    farmer = relationship("Farmer", back_populates="fcm_tokens")


class CoreFarm(Base):
    __tablename__ = "farms"
    __table_args__ = (
        Index("idx_farms_farmer_id", "farmer_id", postgresql_where=Column("deleted_at") == None),
        Index("idx_farms_state_district", "state", "district"),
        {"schema": "core"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False, default="My Farm")
    total_area_acres = Column(Float, nullable=False)
    ownership_type = Column(String(30), nullable=True)
    land_record_number = Column(String, nullable=True)

    state = Column(String, nullable=False)
    district = Column(String, nullable=False)
    taluk = Column(String, nullable=True)
    village = Column(String, nullable=True)
    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)

    primary_soil_type = Column(String(50), nullable=True)
    avg_ph = Column(Float, nullable=True)

    water_source = Column(String(50), default="rain_fed")
    annual_rainfall_mm = Column(Float, nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    farmer = relationship("Farmer", back_populates="farms")
    fields = relationship("CoreField", back_populates="farm", cascade="all, delete-orphan")


class CoreField(Base):
    __tablename__ = "fields"
    __table_args__ = (
        Index("idx_fields_farm_id", "farm_id", postgresql_where=Column("deleted_at") == None),
        Index("idx_fields_farmer_id", "farmer_id", postgresql_where=Column("deleted_at") == None),
        Index("idx_fields_crop", "current_crop", postgresql_where=Column("current_crop") != None),
        Index("idx_fields_status", "status"),
        Index("idx_fields_location", "lat", "lon", postgresql_where=Column("lat") != None),
        Index("idx_fields_harvest", "expected_harvest", postgresql_where=Column("status") == "active"),
        {"schema": "core"}
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey("core.farms.id", ondelete="CASCADE"), nullable=False)
    farmer_id = Column(UUID(as_uuid=True), ForeignKey("core.farmers.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    area_acres = Column(Float, nullable=False)
    status = Column(String(30), nullable=False, default="active")

    current_crop = Column(String, nullable=True)
    crop_variety = Column(String, nullable=True)
    sowing_date = Column(DateTime(timezone=True), nullable=True)
    expected_harvest = Column(DateTime(timezone=True), nullable=True)
    current_stage = Column(String(50), default="fallow")

    soil_texture = Column(String(50), nullable=True)
    soil_ph = Column(Float, nullable=True)
    organic_carbon_pct = Column(Float, nullable=True)
    nitrogen_status = Column(String(30), default="medium")
    phosphorus_status = Column(String(30), default="medium")
    potassium_status = Column(String(30), default="medium")

    irrigation_type = Column(String(50), default="rain_fed")
    has_drip = Column(Boolean, default=False)

    lat = Column(Float, nullable=True)
    lon = Column(Float, nullable=True)
    boundary_geojson = Column(JSONB, nullable=True)

    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    farm = relationship("CoreFarm", back_populates="fields")
    farmer = relationship("Farmer", back_populates="fields")
