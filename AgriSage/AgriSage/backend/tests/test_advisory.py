import pytest
from app.schemas.advisory import AdvisoryRequest, AdvisoryResponse


def test_advisory_schemas():
    req = AdvisoryRequest(
        question="When should I apply second dose of urea?",
        language="en",
        farmer_id="farmer-uuid-1",
        field_id="field-uuid-1",
    )
    assert req.question.startswith("When")
    assert req.farmer_id == "farmer-uuid-1"

    resp = AdvisoryResponse(
        question="When should I apply second dose of urea?",
        answer="Apply within 5-7 days.",
        language="en",
        confidence=0.91,
        sources=["KAU Package of Practices 2024"],
        agents_used=["crop", "weather", "rag"],
        created_at="2026-10-01T08:30:00+05:30",
    )
    assert resp.confidence == 0.91
    assert len(resp.sources) == 1
    assert "rag" in resp.agents_used
