import pytest
from backend.services.morning_briefing import MorningBriefingService
from backend.services.speech_provider import SpeechProvider
from backend.knowledge.freshness import KnowledgeFreshnessTracker


def test_morning_briefing_generation():
    service = MorningBriefingService()
    weather = {"temp_c": 27.5, "humidity_pct": 75.0, "wind_speed_kmh": 8.0, "rainfall_mm": 0.0}
    risk = {"dfi": 0.35}
    
    briefing = service.generate_briefing("Ramesh", "paddy", weather, risk, language="ml")
    assert briefing["farmer_name"] == "Ramesh"
    assert briefing["spray_window_open"] is True
    assert "നമസ്കാരം Ramesh" in briefing["headline"]


@pytest.mark.asyncio
async def test_speech_provider_synthesis():
    provider = SpeechProvider()
    res = await provider.synthesize_speech("നമസ്കാരം രാമൻ, ഇന്ന് കാലാവസ്ഥ അനുയോജ്യമാണ്.", language="ml")
    assert res["language"] == "ml"
    assert "audio_base64" in res
    assert res["duration_seconds"] > 0


def test_knowledge_freshness():
    tracker = KnowledgeFreshnessTracker(default_ttl_days=90)
    meta = {"last_updated": "2026-09-01"}
    res = tracker.evaluate_freshness(meta)
    assert res["is_fresh"] is True
    assert res["status"] == "FRESH"
