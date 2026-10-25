from pathlib import Path
from types import SimpleNamespace

import httpx
import pytest
from fastapi import HTTPException

from backend.config import Settings, settings
from backend.dependencies import get_current_user
from backend.main import app
from backend.services.otp_provider import GenericHTTPOTPProvider
from backend.services.rate_limit import enforce_rate_limit, hashed_rate_key
from backend.services.market_service import MarketService
from backend.services.storage import StorageNotConfigured, r2_storage
from backend.services.weather_service import WeatherContext, WeatherService
from backend.agents.weather import WeatherAgent


def test_request_identity_must_match_jwt_subject():
    subject = "00000000-0000-0000-0000-000000000001"
    principal = {"sub": subject}

    from backend.dependencies import require_subject_identity

    assert require_subject_identity(subject, principal) == subject
    with pytest.raises(HTTPException) as exc_info:
        require_subject_identity("00000000-0000-0000-0000-000000000002", principal)
    assert exc_info.value.status_code == 403


@pytest.mark.asyncio
async def test_advisory_rejects_cross_tenant_farmer_id():
    subject = "00000000-0000-0000-0000-000000000001"

    async def principal():
        return {"sub": subject}

    app.dependency_overrides[get_current_user] = principal
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/advisory",
                json={
                    "farmer_id": "00000000-0000-0000-0000-000000000002",
                    "query": "Should I irrigate today?",
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403
    assert "must match" in response.json()["detail"]


@pytest.mark.asyncio
async def test_offline_sync_rejects_cross_tenant_farmer_id():
    subject = "00000000-0000-0000-0000-000000000001"

    async def principal():
        return {"sub": subject}

    app.dependency_overrides[get_current_user] = principal
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/sync/upload",
                json={
                    "observations": [{"farmer_id": "00000000-0000-0000-0000-000000000002"}]
                },
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 403


@pytest.mark.asyncio
async def test_generic_otp_provider_uses_documented_contract(monkeypatch):
    calls = []

    class FakeResponse:
        status_code = 202

    class FakeClient:
        def __init__(self, **kwargs):
            assert kwargs["timeout"] == 4.0

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def post(self, url, *, headers, json):
            calls.append((url, headers, json))
            return FakeResponse()

    monkeypatch.setattr("backend.services.otp_provider.httpx.AsyncClient", FakeClient)
    provider = GenericHTTPOTPProvider(
        Settings(
            _env_file=None,
            OTP_PROVIDER_URL="https://sms.example.test/send",
            OTP_PROVIDER_KEY="provider-key",
            OTP_PROVIDER_TIMEOUT_SECONDS=4.0,
        )
    )

    await provider.deliver(phone="+919876543210", otp="123456")

    assert calls[0][0] == "https://sms.example.test/send"
    assert calls[0][1]["Authorization"] == "Bearer provider-key"
    assert calls[0][2] == {
        "to": "+919876543210",
        "otp": "123456",
        "message": "Your Agri-SAGE verification code is 123456.",
        "sender": "Agri-SAGE",
    }


def test_rate_limit_keys_are_hashed():
    key = hashed_rate_key("refresh-ip", "203.0.113.10")
    assert key != "203.0.113.10"
    assert len(key) == 64
    assert key == hashed_rate_key("refresh-ip", "203.0.113.10")


@pytest.mark.asyncio
async def test_rate_limit_rejects_after_atomic_counter_is_committed():
    class Result:
        def mappings(self):
            return self

        def one(self):
            return {"request_count": 6}

    class Session:
        commits = 0

        async def execute(self, statement, params):
            return Result()

        async def commit(self):
            self.commits += 1

    session = Session()
    with pytest.raises(HTTPException) as exc_info:
        await enforce_rate_limit(
            session,
            key=hashed_rate_key("otp-send-phone", "+919876543210"),
            limit=5,
            window_seconds=600,
        )
    assert exc_info.value.status_code == 429
    assert session.commits == 1


@pytest.mark.asyncio
async def test_storage_fails_closed_without_r2_in_production(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    monkeypatch.setattr(settings, "ALLOW_LOCAL_STORAGE", False)
    monkeypatch.setattr(r2_storage, "client", None)

    with pytest.raises(StorageNotConfigured):
        await r2_storage.upload_image(b"image", "observations/object.jpg")


@pytest.mark.asyncio
async def test_weather_provider_failure_is_not_actionable(monkeypatch):
    class FailingClient:
        def __init__(self, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def get(self, *args, **kwargs):
            raise RuntimeError("provider down")

    monkeypatch.setattr("backend.agents.weather.httpx.AsyncClient", FailingClient)
    result = await WeatherAgent()._fetch_open_meteo(10.7, 76.6)

    assert result["provider"] == "unavailable"
    assert result["safe_to_act"] is False
    assert result["spray_window"] is None


@pytest.mark.asyncio
async def test_weather_service_provider_failure_returns_unavailable(monkeypatch):
    class FailingClient:
        def __init__(self, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, *args):
            return None

        async def get(self, *args, **kwargs):
            raise RuntimeError("provider down")

    monkeypatch.setattr("backend.services.weather_service.httpx.AsyncClient", FailingClient)
    context = await WeatherService().get_weather(
        state="Rajasthan",
        district="Jodhpur",
        lat=26.2389,
        lon=73.0243,
    )

    assert context.available is False
    assert context.advice_flag == "UNKNOWN"
    assert context.stale is True


@pytest.mark.asyncio
async def test_market_provider_fails_closed_in_production(monkeypatch):
    monkeypatch.setattr(settings, "ENVIRONMENT", "production")
    from backend.services import market_service as market_module

    market_module._MARKET_DB.clear()
    assert await MarketService().get_market_data("rice", "Palakkad") is None


@pytest.mark.asyncio
async def test_morning_briefing_rejects_unavailable_provider_data(monkeypatch):
    subject = "00000000-0000-0000-0000-000000000001"

    async def principal():
        return {"sub": subject, "user": SimpleNamespace(name="Farmer", state="Kerala", district="Palakkad")}

    async def unavailable_weather(**kwargs):
        return WeatherContext(
            temp_c=0.0,
            humidity_pct=0,
            rain_mm_24h=0.0,
            rain_chance_pct=0,
            wind_kmh=0.0,
            advice_flag="UNKNOWN",
            stale=True,
            available=False,
        )

    from backend.api.v1 import notifications

    app.dependency_overrides[get_current_user] = principal
    monkeypatch.setattr(notifications.weather_service, "get_weather", unavailable_weather)
    try:
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/notifications/briefing",
                json={"crop": "rice", "language": "en"},
            )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 503


def test_legacy_stack_has_no_deployment_dockerfile():
    project_root = Path(__file__).parents[2]
    assert not (project_root / "backend" / "Dockerfile").exists()
    assert not (project_root / "backend" / "railway.toml").exists()
    from backend.app.main import app as legacy_app

    assert legacy_app is None


def test_mobile_contract_paths_are_registered_on_canonical_app():
    paths = app.openapi()["paths"]
    assert "/api/v1/farmers/me" in paths
    assert "/api/v1/fields/" in paths
    assert "/api/v1/advisory" in paths


def test_diagnosis_pipeline_does_not_inject_sample_image_or_treatment_data():
    source = (
        Path(__file__).parents[2] / "backend" / "api" / "v1" / "diagnose.py"
    ).read_text(encoding="utf-8")
    assert '"key": "sample_key"' not in source
    assert '"safe_to_act": critic.get("safe_to_act", True)' not in source
    weather_source = (
        Path(__file__).parents[2] / "backend" / "api" / "v1" / "weather.py"
    ).read_text(encoding="utf-8")
    assert '"spray_window_open": True' not in weather_source
