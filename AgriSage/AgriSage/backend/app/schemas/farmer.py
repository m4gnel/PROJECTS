from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class FarmerCreate(BaseModel):
    phone: str
    name: str
    password: str
    village: Optional[str] = None
    district: Optional[str] = None
    preferred_language: str = "ml"
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class FarmerUpdate(BaseModel):
    name: Optional[str] = None
    village: Optional[str] = None
    district: Optional[str] = None
    preferred_language: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None


class FarmerRead(BaseModel):
    id: str
    phone: str
    name: str
    village: Optional[str]
    district: Optional[str]
    state: str
    preferred_language: str
    latitude: Optional[float]
    longitude: Optional[float]
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
