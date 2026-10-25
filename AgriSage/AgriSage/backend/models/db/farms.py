import uuid
from sqlalchemy import (
    Column, String, Boolean, Integer, Numeric, Text, Date, DateTime,
    ForeignKey, CheckConstraint, Index, func, text
)
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from backend.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(15), unique=True, nullable=False, index=True)
    name = Column(String(100), nullable=True)
    language = Column(String(10), nullable=False, default="ml")
    location_lat = Column(Numeric(9, 6), nullable=True)
    location_lon = Column(Numeric(9, 6), nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), default="India")
    subscription_tier = Column(String(20), nullable=False, default="free")
    role = Column(String(20), nullable=False, default="farmer", server_default="farmer")
    permissions = Column(JSONB, nullable=False, default=list, server_default=text("'[]'::jsonb"))
    subscription_expires = Column(DateTime(timezone=True), nullable=True)
    trial_started_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    advisories_this_month = Column(Integer, nullable=False, default=0)
    advisories_reset_at = Column(Date, nullable=False, server_default=func.current_date())
    is_active = Column(Boolean, nullable=False, default=True)
    fcm_token = Column(String(500), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())
    last_active_at = Column(DateTime(timezone=True), nullable=True)

    # Fully qualified relationship paths to avoid declarative registry ambiguity
    farms = relationship("backend.models.db.farms.Farm", back_populates="owner", cascade="all, delete-orphan")
    refresh_tokens = relationship("backend.models.db.farms.RefreshToken", back_populates="user", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint(
            "role IN ('farmer','employee','officer','expert')",
            name="chk_users_role",
        ),
    )


class OTPSession(Base):
    __tablename__ = "otp_sessions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    phone = Column(String(15), nullable=False, index=True)
    otp_hash = Column(String(255), nullable=False)
    attempts = Column(Integer, nullable=False, default=0)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    used = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        Index("idx_otp_phone", "phone", "expires_at"),
    )


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    token_hash = Column(String(255), unique=True, nullable=False)
    expires_at = Column(DateTime(timezone=True), nullable=False)
    revoked = Column(Boolean, nullable=False, default=False)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    user = relationship("backend.models.db.farms.User", back_populates="refresh_tokens")


class Farm(Base):
    __tablename__ = "farms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(200), nullable=False)
    location_lat = Column(Numeric(9, 6), nullable=True)
    location_lon = Column(Numeric(9, 6), nullable=True)
    district = Column(String(100), nullable=True)
    state = Column(String(100), nullable=True)
    area_ha = Column(Numeric(8, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    owner = relationship("backend.models.db.farms.User", back_populates="farms")
    fields = relationship("backend.models.db.farms.Field", back_populates="farm", cascade="all, delete-orphan")


class Field(Base):
    __tablename__ = "fields"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id", ondelete="CASCADE"), nullable=False, index=True)
    name = Column(String(100), nullable=True)
    area_ha = Column(Numeric(8, 2), nullable=True)
    slope = Column(String(20), nullable=True)
    irrigation = Column(String(30), nullable=True)
    soil_type = Column(String(50), nullable=True)
    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint("slope IN ('flat','gentle','moderate','steep')", name="chk_field_slope"),
    )

    farm = relationship("backend.models.db.farms.Farm", back_populates="fields")
    soil_profiles = relationship("backend.models.db.farms.SoilProfile", back_populates="field", cascade="all, delete-orphan")
    crop_cycles = relationship("backend.models.db.farms.CropCycle", back_populates="field", cascade="all, delete-orphan")


class SoilProfile(Base):
    __tablename__ = "soil_profiles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey("fields.id", ondelete="CASCADE"), nullable=False, index=True)
    pH = Column(Numeric(4, 2), nullable=True)
    nitrogen_kgha = Column(Numeric(8, 2), nullable=True)
    phosphorus_kgha = Column(Numeric(8, 2), nullable=True)
    potassium_kgha = Column(Numeric(8, 2), nullable=True)
    organic_carbon = Column(Numeric(5, 2), nullable=True)
    texture = Column(String(30), nullable=True)
    field_capacity = Column(Numeric(5, 2), nullable=True)
    wilting_point = Column(Numeric(5, 2), nullable=True)
    source = Column(String(50), default="estimated")
    measured_at = Column(Date, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    __table_args__ = (
        CheckConstraint('"pH" BETWEEN 0 AND 14', name="chk_soil_ph"),
    )

    field = relationship("backend.models.db.farms.Field", back_populates="soil_profiles")


class CropCycle(Base):
    __tablename__ = "crop_cycles"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    field_id = Column(UUID(as_uuid=True), ForeignKey("fields.id", ondelete="CASCADE"), nullable=False, index=True)
    crop = Column(String(50), nullable=False)
    cultivar = Column(String(100), nullable=True)
    season = Column(String(20), nullable=True)
    planting_date = Column(Date, nullable=False)
    expected_harvest = Column(Date, nullable=True)
    actual_harvest = Column(Date, nullable=True)
    status = Column(String(20), nullable=False, default="active")
    notes = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    __table_args__ = (
        CheckConstraint("status IN ('active','harvested','abandoned')", name="chk_cycle_status"),
    )

    field = relationship("backend.models.db.farms.Field", back_populates="crop_cycles")
    observations = relationship("backend.models.db.farms.Observation", back_populates="crop_cycle", cascade="all, delete-orphan")


class Observation(Base):
    __tablename__ = "observations"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    crop_cycle_id = Column(UUID(as_uuid=True), ForeignKey("crop_cycles.id", ondelete="CASCADE"), nullable=False, index=True)
    problem_description = Column(Text, nullable=True)
    voice_note_key = Column(String(500), nullable=True)
    irrigation_status = Column(String(20), nullable=True)
    fertilizer_recent = Column(Boolean, nullable=True)
    pesticide_recent = Column(Boolean, nullable=True)
    observed_growth_stage = Column(String(50), nullable=True)
    observed_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    crop_cycle = relationship("backend.models.db.farms.CropCycle", back_populates="observations")
    images = relationship("backend.models.db.farms.Image", back_populates="observation", cascade="all, delete-orphan")


class Image(Base):
    __tablename__ = "images"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    observation_id = Column(UUID(as_uuid=True), ForeignKey("observations.id", ondelete="CASCADE"), nullable=False, index=True)
    r2_key = Column(String(500), nullable=False, unique=True)
    mime_type = Column(String(50), nullable=False)
    file_size_bytes = Column(Integer, nullable=True)
    width_px = Column(Integer, nullable=True)
    height_px = Column(Integer, nullable=True)
    quality_score = Column(Numeric(4, 2), nullable=True)
    blur_score = Column(Numeric(8, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    observation = relationship("backend.models.db.farms.Observation", back_populates="images")
