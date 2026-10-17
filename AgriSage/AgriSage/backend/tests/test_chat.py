import pytest
from app.schemas.chat import ChatRequest, ChatResponse


def test_chat_schemas():
    req = ChatRequest(
        session_id="session-1",
        message="ഇന്ന് വളം ഇടണോ?",
        language="ml",
        farmer_id="farmer-1",
        field_id="field-1",
        latitude=10.165,
        longitude=76.401,
    )
    assert req.language == "ml"
    assert req.farmer_id == "farmer-1"

    resp = ChatResponse(
        session_id="session-1",
        message="കാലാവസ്ഥ നല്ലതാണ്.",
        language="ml",
        confidence=0.9,
        alerts=[],
        agents_used=["weather", "fertilizer"],
        created_at="2026-10-01T08:30:00+05:30",
    )
    assert resp.confidence == 0.9
    assert len(resp.agents_used) == 2
