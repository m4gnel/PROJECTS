from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class ActiveCrop(BaseModel):
    id: str
    crop_name: str
    variety: Optional[str]
    sowing_date: str
    growth_stage: Optional[str]
    expected_harvest_date: Optional[str]


class FieldCreate(BaseModel):
    name: str
    area_sq_m: float
    latitude: float
    longitude: float
    soil_type: Optional[str] = None
    irrigation_type: Optional[str] = None
    crop_name: Optional[str] = None
    crop_variety: Optional[str] = None
    sowing_date: Optional[str] = None


class FieldUpdate(BaseModel):
    name: Optional[str] = None
    area_sq_m: Optional[float] = None
    soil_type: Optional[str] = None
    irrigation_type: Optional[str] = None


class FieldRead(BaseModel):
    id: str
    farmer_id: str
    name: str
    area_sq_m: float
    latitude: float
    longitude: float
    soil_type: Optional[str]
    irrigation_type: Optional[str]
    last_ndvi: Optional[float]
    active_crop: Optional[ActiveCrop]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
