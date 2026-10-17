import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from backend.services.weather_service import WeatherService, WeatherContext
from backend.services.market_service import MarketService
from backend.services.pest_service import PestService
from backend.services.soil_service import get_soil_by_district


@pytest.mark.asyncio
async def test_weather_service_returns_context():
    service = WeatherService()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "hourly": {
            "temperature_2m": [33.0],
            "relative_humidity_2m": [88],
            "precipitation": [55.0] + [0.0] * 23,
            "windspeed_10m": [15.0],
            "precipitation_probability": [90]
        }
    }

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_get.return_value = mock_response
        ctx = await service.get_weather("Ernakulam")

        assert isinstance(ctx, WeatherContext)
        assert ctx.temp_c == 33.0
        assert ctx.humidity_pct == 88
        assert ctx.rain_mm_24h == 55.0
        assert ctx.advice_flag == "FLOOD_RISK"


@pytest.mark.asyncio
async def test_weather_service_uses_cache():
    service = WeatherService()

    with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "hourly": {
                "temperature_2m": [29.0],
                "relative_humidity_2m": [75],
                "precipitation": [0.0] * 24,
                "windspeed_10m": [8.0],
                "precipitation_probability": [10]
            }
        }
        mock_get.return_value = mock_response

        # First call fetches from HTTP
        ctx1 = await service.get_weather("Thrissur", lat=10.52, lon=76.21)
        assert ctx1.cached is False

        # Second call within TTL should return cached
        ctx2 = await service.get_weather("Thrissur", lat=10.52, lon=76.21)
        assert ctx2.cached is True


@pytest.mark.asyncio
async def test_market_service_upserts_prices():
    service = MarketService()
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {
        "records": [
            {"commodity": "Coconut", "variety": "Local", "district": "Thrissur", "min_price": "2500", "max_price": "3000", "modal_price": "2800", "arrival_date": "2026-10-04"},
            {"commodity": "Rice", "variety": "Jyothi", "district": "Palakkad", "min_price": "3200", "max_price": "3800", "modal_price": "3500", "arrival_date": "2026-10-04"},
            {"commodity": "Banana", "variety": "Nendran", "district": "Wayanad", "min_price": "4000", "max_price": "4500", "modal_price": "4200", "arrival_date": "2026-10-04"}
        ]
    }

    with patch("backend.config.settings.DATA_GOV_IN_KEY", "test_key_123"):
        with patch("httpx.AsyncClient.get", new_callable=AsyncMock) as mock_get:
            mock_get.return_value = mock_response
            records = await service.fetch_and_upsert_prices()
            assert len(records) >= 3

            ctx = await service.get_market_data("coconut", "Thrissur")
            assert ctx.modal_price == 2800.0


@pytest.mark.asyncio
async def test_pest_service_parses_rss():
    service = PestService()
    mock_feed = MagicMock()
    entry1 = MagicMock()
    entry1.title = "Severe outbreak of rugose whitefly on coconut palms in Kerala"
    entry1.description = "Emergency pest alert issued for coconut farmers."
    entry1.published = "Sun, 04 Oct 2026 08:00:00 GMT"
    mock_feed.entries = [entry1]

    mock_parser = MagicMock()
    mock_parser.parse.return_value = mock_feed

    with patch.object(service, "classify_severity", return_value="HIGH"):
        with patch("backend.services.pest_service.feedparser", mock_parser):
            alerts = await service.fetch_rss_alerts()
            assert len(alerts) >= 1

            ctx = await service.get_alerts_for_district_and_crop("Ernakulam", "coconut")
            assert ctx.highest_severity == "HIGH"
            assert any("coconut" in a.get("affected_crops", []) for a in ctx.alerts)


def test_soil_service_ernakulam():
    context = get_soil_by_district("Ernakulam")
    assert context is not None
    assert context.district == "Ernakulam"
    assert context.texture == "laterite"
    assert "coconut" in context.suitable_crops


def test_soil_service_unknown_district():
    context = get_soil_by_district("InvalidDistrict")
    assert context is None
