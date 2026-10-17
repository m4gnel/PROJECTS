from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException, status
from backend.agents.scheme import SchemeAgent

router = APIRouter(tags=["Schemes"])

scheme_agent = SchemeAgent()

MOCK_SCHEMES = [
    {
        "scheme_id": "PMFBY",
        "scheme_name": "Pradhan Mantri Fasal Bima Yojana (PMFBY)",
        "type": "Crop Insurance",
        "category": "Central",
        "subsidy_percentage": 85.0,
        "valid_until": "2028-03-31",
        "eligibility_summary": "All farmers growing notified crops in notified areas including sharecroppers & tenant farmers.",
        "mandatory_caveat": "Final eligibility determined by concerned authority / അന്തിമ യോഗ്യത ബന്ധപ്പെട്ട അധികാരി നിർണ്ണയിക്കും"
    },
    {
        "scheme_id": "PM-KISAN",
        "scheme_name": "PM-KISAN Samman Nidhi",
        "type": "Direct Income Support",
        "category": "Central",
        "financial_benefit": "INR 6,000 / year in 3 equal installments",
        "valid_until": "2030-12-31",
        "eligibility_summary": "Small and marginal farmer families with cultivable landholding up to 2 hectares.",
        "mandatory_caveat": "Final eligibility determined by concerned authority / അന്തിമ യോഗ്യത ബന്ധപ്പെട്ട അധികാരി നിർണ്ണയിക്കും"
    },
    {
        "scheme_id": "RKVY-RAFTAAR",
        "scheme_name": "Rashtriya Krishi Vikas Yojana (RKVY)",
        "type": "Infrastructure & Innovation",
        "category": "Central / State Shared",
        "subsidy_percentage": 50.0,
        "valid_until": "2027-03-31",
        "eligibility_summary": "Registered farmer producer organizations (FPO), individual farmers, and Agri-startups.",
        "mandatory_caveat": "Final eligibility determined by concerned authority / അന്തിമ യോഗ്യത ബന്ധപ്പെട്ട അധികാരി നിർണ്ണയിക്കും"
    }
]


@router.get("/schemes")
async def list_government_schemes(
    category: Optional[str] = None
) -> List[Dict[str, Any]]:
    """Retrieve verified government agricultural schemes with statutory disclaimers."""
    valid_schemes = scheme_agent.filter_valid_schemes(MOCK_SCHEMES)
    if category:
        valid_schemes = [s for s in valid_schemes if category.lower() in s.get("category", "").lower()]
    return scheme_agent.format_matches(valid_schemes)


@router.get("/schemes/{scheme_id}")
async def get_scheme_detail(scheme_id: str) -> Dict[str, Any]:
    """Retrieve detailed scheme information by scheme ID."""
    for s in MOCK_SCHEMES:
        if s["scheme_id"].upper() == scheme_id.upper():
            return s
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Scheme with ID '{scheme_id}' not found."
    )
