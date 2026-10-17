from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class AdvisoryRequest(BaseModel):
    question: str
    language: str = "en"
    farmer_id: str
    field_id: Optional[str] = None


class AdvisoryResponse(BaseModel):
    question: str
    answer: str
    language: str
    confidence: float
    sources: List[str]
    agents_used: List[str]
    created_at: datetime
