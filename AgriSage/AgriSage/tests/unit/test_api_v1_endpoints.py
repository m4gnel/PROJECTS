import pytest
from fastapi.testclient import TestClient
from backend.main import app
from backend.dependencies import get_current_user

client = TestClient(app)


@pytest.fixture(autouse=True)
def override_user():
    app.dependency_overrides[get_current_user] = lambda: {"sub": "test-user"}
    yield
    app.dependency_overrides.pop(get_current_user, None)


def test_markets_prices_endpoint():
    response = client.get("/api/v1/markets/prices")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "modal_price_inr_quintal" in data[0]


def test_markets_msp_endpoint():
    response = client.get("/api/v1/markets/msp")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(item["commodity"].startswith("Paddy") for item in data)


def test_notifications_endpoint():
    response = client.get("/api/v1/notifications")
    assert response.status_code == 200
    assert response.json() == []


def test_risk_dfi_endpoint():
    response = client.get("/api/v1/risk/dfi?humidity_pct=85&temp_c=26&consecutive_wet_days=3")
    assert response.status_code == 200
    data = response.json()
    assert "dfi" in data
    assert data["dfi"] >= 0.70
    assert data["risk_level"] == "CRITICAL"


def test_risk_radar_endpoint():
    response = client.get("/api/v1/risk/radar?state=Kerala")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert "district" in data[0]


def test_schemes_endpoint():
    response = client.get("/api/v1/schemes")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert any(s["scheme_id"] == "PMFBY" for s in data)
    for scheme in data:
        assert "mandatory_caveat" in scheme
        assert "concerned authority" in scheme["mandatory_caveat"]


def test_simulate_scenario_endpoint():
    payload = {
        "crop": "paddy",
        "stage_code": "tillering",
        "gdd_accumulated": 400.0,
        "temp_c": 28.0,
        "rainfall_mm": 5.0,
        "humidity_pct": 80.0,
        "disease_severity": 0.25
    }
    response = client.post("/api/v1/simulate/scenario", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "scenarios" in data
    assert len(data["scenarios"]) == 3


def test_sync_package_endpoint():
    response = client.get("/api/v1/sync/package?crop=paddy&language=ml")
    assert response.status_code == 200
    data = response.json()
    assert data["crop"] == "paddy"
    assert "onnx_model_url" in data


def test_weather_current_endpoint():
    response = client.get("/api/v1/weather/current?lat=10.78&lng=76.65")
    assert response.status_code == 200
    data = response.json()
    assert "temp_c" in data
    assert "spray_window_open" in data
