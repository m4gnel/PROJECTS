from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum


class AlertSeverity(str, Enum):
    CRITICAL = "CRITICAL"
    WARNING = "WARNING"
    INFO = "INFO"
    SUCCESS = "SUCCESS"


class AlertRead(BaseModel):
    id: str
    farmer_id: str
    field_id: Optional[str]
    severity: str
    title: str
    message: str
    source_agent: Optional[str]
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class AlertCreate(BaseModel):
    farmer_id: str
    field_id: Optional[str] = None
    severity: str
    title: str
    message: str
    source_agent: Optional[str] = None


class MarkReadRequest(BaseModel):
    alert_ids: list[str]
