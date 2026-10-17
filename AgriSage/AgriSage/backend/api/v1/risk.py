from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Query
from backend.simulation.rules import DiseaseFavorabilityRules

router = APIRouter(tags=["Risk & Radar"])


@router.get("/risk/dfi")
async def calculate_dfi_index(
    humidity_pct: float = Query(75.0, ge=0.0, le=100.0),
    temp_c: float = Query(27.0, ge=-10.0, le=50.0),
    consecutive_wet_days: int = Query(2, ge=0, le=30)
) -> Dict[str, Any]:
    """Calculate Disease Favorability Index (DFI) for micro-climate conditions."""
    dfi = DiseaseFavorabilityRules.calculate_dfi(
        relative_humidity_pct=humidity_pct,
        temp_c=temp_c,
        consecutive_wet_days=consecutive_wet_days
    )
    
    risk_level = "LOW"
    if dfi >= 0.70:
        risk_level = "CRITICAL"
    elif dfi >= 0.50:
        risk_level = "HIGH"
    elif dfi >= 0.30:
        risk_level = "MEDIUM"

    return {
        "dfi": dfi,
        "risk_level": risk_level,
        "humidity_pct": humidity_pct,
        "temp_c": temp_c,
        "consecutive_wet_days": consecutive_wet_days,
        "recommendation": "High fungal spore germination risk. Monitor crop leaf sheaths closely." if dfi >= 0.5 else "Low favorability for major fungal pathogens."
    }


@router.get("/risk/radar")
async def get_outbreak_radar_clusters(
    state: str = Query("Kerala", description="State name filter")
) -> List[Dict[str, Any]]:
    """Retrieve regional disease and pest outbreak radar clusters."""
    return [
        {
            "cluster_id": "CLUST-KL-01",
            "district": "Palakkad",
            "crop": "Paddy",
            "disease": "Rice Blast (Pyricularia oryzae)",
            "risk_score": 0.82,
            "severity": "HIGH",
            "reported_cases": 142,
            "center_lat": 10.7867,
            "center_lng": 76.6548,
            "radius_km": 15.0,
            "last_updated": "2026-10-03T08:00:00Z"
        },
        {
            "cluster_id": "CLUST-KL-02",
            "district": "Wayanad",
            "crop": "Pepper",
            "disease": "Quick Wilt (Phytophthora capsici)",
            "risk_score": 0.76,
            "severity": "HIGH",
            "reported_cases": 89,
            "center_lat": 11.6854,
            "center_lng": 76.1320,
            "radius_km": 12.0,
            "last_updated": "2026-10-03T09:30:00Z"
        },
        {
            "cluster_id": "CLUST-KL-03",
            "district": "Thrissur",
            "crop": "Banana",
            "disease": "Banana Bunchy Top Virus (BBTV)",
            "risk_score": 0.45,
            "severity": "MEDIUM",
            "reported_cases": 34,
            "center_lat": 10.5276,
            "center_lng": 76.2144,
            "radius_km": 8.0,
            "last_updated": "2026-10-02T16:00:00Z"
        }
    ]
