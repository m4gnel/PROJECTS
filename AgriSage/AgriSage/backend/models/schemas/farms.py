import re
from typing import Optional, List
from datetime import date, datetime
from pydantic import BaseModel, Field, field_validator, ConfigDict


class FarmBase(BaseModel):
    name: str = Field(..., max_length=200, example="Green Valley Paddy Field")
    district: Optional[str] = Field(None, max_length=100, example="Palakkad")
    state: Optional[str] = Field("Kerala", max_length=100)
    area_ha: Optional[float] = Field(None, ge=0, example=2.5)

    @field_validator("name", mode="before")
    @classmethod
    def sanitize_name(cls, v: str) -> str:
        if isinstance(v, str):
            # Strip HTML tags
            v = re.sub(r"<[^>]+>", "", v)
            # Strip control characters (\x00-\x1f\x7f)
            v = re.sub(r"[\x00-\x1f\x7f]", "", v)
            return v.strip()
        return v


class FarmCreate(FarmBase):
    pass


class FarmResponse(FarmBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class FieldBase(BaseModel):
    name: Optional[str] = Field(None, max_length=100, example="North Block Paddy")
    area_ha: Optional[float] = Field(None, ge=0, example=1.2)
    slope: Optional[str] = Field(None, example="flat")  # flat, gentle, moderate, steep
    irrigation: Optional[str] = Field(None, example="canals")
    soil_type: Optional[str] = Field(None, example="clay loam")

    @field_validator("name", mode="before")
    @classmethod
    def sanitize_field_name(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            v = re.sub(r"<[^>]+>", "", v)
            v = re.sub(r"[\x00-\x1f\x7f]", "", v)
            return v.strip()
        return v

    @field_validator("slope")
    @classmethod
    def validate_slope(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            allowed = {"flat", "gentle", "moderate", "steep"}
            if v.lower() not in allowed:
                raise ValueError(f"slope must be one of {allowed}")
            return v.lower()
        return v


class FieldCreate(FieldBase):
    pass


class FieldResponse(FieldBase):
    id: str
    farm_id: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CropCycleBase(BaseModel):
    crop: str = Field(..., max_length=50, example="rice")
    cultivar: Optional[str] = Field(None, max_length=100, example="Jyothi")
    season: Optional[str] = Field(None, max_length=20, example="Kharif")
    planting_date: date = Field(..., example="2026-06-15")
    expected_harvest: Optional[date] = Field(None, example="2026-10-15")
    actual_harvest: Optional[date] = None
    status: str = Field("active", example="active")  # active, harvested, abandoned
    notes: Optional[str] = None

    @field_validator("crop", "cultivar", "season", mode="before")
    @classmethod
    def sanitize_strings(cls, v: Optional[str]) -> Optional[str]:
        if isinstance(v, str):
            v = re.sub(r"<[^>]+>", "", v)
            v = re.sub(r"[\x00-\x1f\x7f]", "", v)
            return v.strip()
        return v

    @field_validator("status")
    @classmethod
    def validate_status(cls, v: str) -> str:
        allowed = {"active", "harvested", "abandoned"}
        if v.lower() not in allowed:
            raise ValueError(f"status must be one of {allowed}")
        return v.lower()


class CropCycleCreate(CropCycleBase):
    field_id: str


class CropCycleResponse(CropCycleBase):
    id: str
    field_id: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
