from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class CropInfoSchema(BaseModel):
    crop_name: str
    variety: str
    sowing_date: str
    current_growth_stage: str
    field_area_hectares: float


class ChatRequest(BaseModel):
    session_id: str
    message: str
    language: str = "ml"
    farmer_id: str
    field_id: Optional[str] = None
    latitude: float = 10.1632
    longitude: float = 76.3986
    crop_info: Optional[CropInfoSchema] = None


class AlertInChat(BaseModel):
    id: str
    severity: str
    title: str
    message: str
    created_at: datetime


class ChatResponse(BaseModel):
    session_id: str
    message: str
    language: str
    confidence: float
    alerts: List[AlertInChat]
    agents_used: List[str]
    created_at: datetime


class MessageRead(BaseModel):
    id: str
    session_id: str
    content: str
    is_from_user: bool
    created_at: datetime

    class Config:
        from_attributes = True
