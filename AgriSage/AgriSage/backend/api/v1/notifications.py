from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Body
from backend.services.morning_briefing import MorningBriefingService

router = APIRouter(tags=["Notifications"])

briefing_service = MorningBriefingService()

MOCK_NOTIFICATIONS = [
    {
        "id": "notif-001",
        "title": "Morning Spray Window Alert",
        "message": "Favorable spray conditions today between 6:00 AM - 9:30 AM (Wind < 10 km/h).",
        "category": "spray_window",
        "priority": "high",
        "created_at": "2026-10-03T06:00:00Z",
        "is_read": False
    },
    {
        "id": "notif-002",
        "title": "High Humidity & Disease Favorability Warning",
        "message": "High relative humidity (88%) in Palakkad increases Rice Blast favorability index (DFI 0.72). Inspect lower leaf sheath.",
        "category": "disease_risk",
        "priority": "critical",
        "created_at": "2026-10-03T07:15:00Z",
        "is_read": False
    },
    {
        "id": "notif-003",
        "title": "PMFBY Crop Insurance Renewal Deadline",
        "message": "Enrolment for Kharif PMFBY ends soon. Verify crop sowing certificate at your nearest Krishi Bhavan.",
        "category": "scheme",
        "priority": "medium",
        "created_at": "2026-10-02T10:00:00Z",
        "is_read": True
    }
]


@router.get("/notifications")
async def get_user_notifications() -> List[Dict[str, Any]]:
    """Retrieve user advisory, risk, and scheme notifications."""
    return MOCK_NOTIFICATIONS


@router.post("/notifications/briefing")
async def generate_morning_briefing(
    payload: Dict[str, Any] = Body(...)
) -> Dict[str, Any]:
    """Generate daily morning briefing for farmer."""
    farmer_name = payload.get("farmer_name", "Farmer")
    crop = payload.get("crop", "paddy")
    weather = payload.get("weather", {"temp_c": 28.5, "humidity_pct": 78.0, "wind_speed_kmh": 9.0})
    risk = payload.get("risk", {"dfi": 0.45})
    lang = payload.get("language", "ml")

    return briefing_service.generate_briefing(
        farmer_name=farmer_name,
        crop=crop,
        weather_data=weather,
        risk_data=risk,
        language=lang
    )
