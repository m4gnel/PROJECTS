from typing import Any, Dict, List, Literal
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from backend.services.morning_briefing import MorningBriefingService
from backend.services.weather_service import weather_service
from backend.simulation.rules import DiseaseFavorabilityRules
from backend.dependencies import get_current_user

router = APIRouter(tags=["Notifications"])

briefing_service = MorningBriefingService()


class MorningBriefingRequest(BaseModel):
    """Inputs used to select a farmer's crop and weather location.

    Weather and risk values are deliberately not accepted from the client. The
    endpoint obtains them from the configured provider so a caller cannot turn
    fabricated readings into an actionable briefing.
    """

    crop: str = Field(..., min_length=1, max_length=50)
    language: Literal["hi", "en", "ta", "ml", "te", "pa"] = "ml"
    state: str | None = Field(default=None, max_length=100)
    district: str | None = Field(default=None, max_length=100)
    latitude: float | None = Field(default=None, ge=6.0, le=38.0)
    longitude: float | None = Field(default=None, ge=68.0, le=97.5)

@router.get("/notifications")
async def get_user_notifications(
    auth: Dict[str, Any] = Depends(get_current_user),
) -> List[Dict[str, Any]]:
    """Retrieve user advisory, risk, and scheme notifications."""
    # Notifications are not yet backed by the canonical alerts store.  Return
    # an empty set rather than broadcasting sample alerts to every tenant.
    return []


@router.post("/notifications/briefing")
async def generate_morning_briefing(
    payload: MorningBriefingRequest,
    auth: Dict[str, Any] = Depends(get_current_user),
) -> Dict[str, Any]:
    """Generate a briefing from current provider-backed weather data."""
    user = auth["user"]
    state = payload.state or getattr(user, "state", None) or "India"
    district = payload.district or getattr(user, "district", None) or ""
    latitude = payload.latitude
    longitude = payload.longitude
    if latitude is None and getattr(user, "location_lat", None) is not None:
        latitude = float(user.location_lat)
    if longitude is None and getattr(user, "location_lon", None) is not None:
        longitude = float(user.location_lon)

    weather = await weather_service.get_weather(
        state=state,
        district=district,
        lat=latitude,
        lon=longitude,
    )
    if not weather.available or weather.stale:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Current weather data is unavailable for the briefing",
        )

    risk = {
        "dfi": DiseaseFavorabilityRules.calculate_dfi(
            relative_humidity_pct=weather.humidity_pct,
            temp_c=weather.temp_c,
            consecutive_wet_days=1 if weather.rain_mm_24h >= 1.0 else 0,
        )
    }

    return briefing_service.generate_briefing(
        farmer_name=getattr(user, "name", None) or "Farmer",
        crop=payload.crop.strip(),
        weather_data={
            "temp_c": weather.temp_c,
            "humidity_pct": weather.humidity_pct,
            "wind_speed_kmh": weather.wind_kmh,
            "rainfall_mm": weather.rain_mm_24h,
        },
        risk_data=risk,
        language=payload.language,
    )
