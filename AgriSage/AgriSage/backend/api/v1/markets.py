from typing import Dict, Any, List, Optional
from fastapi import APIRouter, Query

router = APIRouter(tags=["Markets"])

MOCK_MANDI_PRICES = [
    {
        "market": "Palakkad Mandi",
        "state": "Kerala",
        "district": "Palakkad",
        "commodity": "Paddy (Common)",
        "variety": "Jyothi",
        "min_price_inr_quintal": 2250.0,
        "max_price_inr_quintal": 2480.0,
        "modal_price_inr_quintal": 2350.0,
        "last_updated": "2026-10-03"
    },
    {
        "market": "Thrissur Market",
        "state": "Kerala",
        "district": "Thrissur",
        "commodity": "Banana (Nendran)",
        "variety": "Nendran",
        "min_price_inr_quintal": 3800.0,
        "max_price_inr_quintal": 4500.0,
        "modal_price_inr_quintal": 4200.0,
        "last_updated": "2026-10-03"
    },
    {
        "market": "Wayanad Market",
        "state": "Kerala",
        "district": "Wayanad",
        "commodity": "Pepper (Black)",
        "variety": "Garbled",
        "min_price_inr_quintal": 54000.0,
        "max_price_inr_quintal": 58000.0,
        "modal_price_inr_quintal": 56500.0,
        "last_updated": "2026-10-03"
    },
    {
        "market": "Kolar Mandi",
        "state": "Karnataka",
        "district": "Kolar",
        "commodity": "Tomato",
        "variety": "Hybrid",
        "min_price_inr_quintal": 1800.0,
        "max_price_inr_quintal": 2600.0,
        "modal_price_inr_quintal": 2200.0,
        "last_updated": "2026-10-03"
    }
]

MOCK_MSP_RATES = [
    {"commodity": "Paddy (Common)", "season": "Kharif 2026", "msp_inr_quintal": 2300.0},
    {"commodity": "Paddy (Grade A)", "season": "Kharif 2026", "msp_inr_quintal": 2320.0},
    {"commodity": "Maize", "season": "Kharif 2026", "msp_inr_quintal": 2225.0},
    {"commodity": "Cotton (Medium Staple)", "season": "Kharif 2026", "msp_inr_quintal": 7121.0},
    {"commodity": "Soybean (Yellow)", "season": "Kharif 2026", "msp_inr_quintal": 4892.0}
]


@router.get("/markets/prices")
async def get_mandi_prices(
    commodity: Optional[str] = Query(None, description="Filter by commodity name"),
    district: Optional[str] = Query(None, description="Filter by district name")
) -> List[Dict[str, Any]]:
    """Retrieve live and cached Mandi commodity prices."""
    results = MOCK_MANDI_PRICES
    if commodity:
        results = [p for p in results if commodity.lower() in p["commodity"].lower()]
    if district:
        results = [p for p in results if district.lower() in p["district"].lower()]
    return results


@router.get("/markets/msp")
async def get_minimum_support_prices() -> List[Dict[str, Any]]:
    """Retrieve official government Minimum Support Price (MSP) rates."""
    return MOCK_MSP_RATES
