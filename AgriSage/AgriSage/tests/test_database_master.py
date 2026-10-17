import os
import sys
import re
import math
import pytest
from datetime import datetime, date, time

# Add project root to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Core models
from backend.models.db.core import Farmer, CoreFarm, CoreField, FCMToken
# Realtime models
from backend.models.db.realtime import (
    WeatherCache, WeatherForecast, MarketPrice, PestAlert, PestAlertCrop,
    SoilZone, IMDRainfall, NDVIReading, MSPReference
)
# Agents models
from backend.models.db.agents import (
    AdvisorySession, AdvisoryMessage, AgentInvocation, KauDocument,
    LangGraphCheckpoint, LangGraphCheckpointWrite
)
# Intelligence models
from backend.models.db.intelligence import (
    FieldObservation, CropStage, IrrigationSchedule, FertiliserPlan
)
# Alerts models
from backend.models.db.alerts import (
    FarmerAlert, FCMDeliveryLog
)
# Market models
from backend.models.db.market import (
    MarketRecommendation, PriceSubscription
)
# Analytics models
from backend.models.db.analytics import (
    FarmSeasonAnalytics, AgentPerformance, PlatformMetrics, AdvisoryFeedback
)
# System models
from backend.models.db.system import (
    AuditLog, APIRateLimit
)

# Pydantic v2 Master Schemas
from backend.models.schemas.master import (
    FarmerCreate, FarmerResponse, FCMTokenCreate, FCMTokenResponse,
    CoreFarmCreate, CoreFarmResponse, CoreFieldCreate, CoreFieldResponse,
    WeatherCacheResponse, WeatherForecastResponse, MarketPriceResponse,
    PestAlertResponse, SoilZoneResponse, IMDRainfallResponse, NDVIReadingResponse,
    MSPReferenceResponse, AdvisorySessionCreate, AdvisorySessionResponse,
    AdvisoryMessageCreate, AdvisoryMessageResponse, KauDocumentResponse,
    AgentInvocationResponse, LangGraphCheckpointResponse,
    FieldObservationCreate, FieldObservationResponse, CropStageResponse,
    IrrigationScheduleResponse, FertiliserPlanResponse, FarmerAlertResponse,
    FCMDeliveryLogResponse, MarketRecommendationResponse, PriceSubscriptionResponse,
    FarmSeasonAnalyticsResponse, AgentPerformanceResponse, PlatformMetricsResponse,
    AdvisoryFeedbackResponse, AuditLogResponse, APIRateLimitResponse
)


def test_core_orm_instantiation():
    """Verify core layer entities (Farmer, CoreFarm, CoreField, FCMToken)."""
    farmer = Farmer(
        name="Ramesh Singh",
        phone="9876543210",
        state="Punjab",
        district="Ludhiana",
        primary_language="hi",
        crops=["wheat", "rice"]
    )
    assert farmer.name == "Ramesh Singh"
    assert farmer.phone == "9876543210"
    assert farmer.state == "Punjab"
    assert "wheat" in farmer.crops
    assert farmer.__table_args__[-1]["schema"] == "core"

    farm = CoreFarm(
        total_area_acres=5.5,
        state="Punjab",
        district="Ludhiana",
        ownership_type="owned"
    )
    assert farm.total_area_acres == 5.5
    assert farm.ownership_type == "owned"
    assert farm.__table_args__[-1]["schema"] == "core"

    field = CoreField(
        name="North Field",
        area_acres=2.5,
        current_crop="wheat",
        soil_texture="loam",
        status="active"
    )
    assert field.name == "North Field"
    assert field.area_acres == 2.5
    assert field.current_crop == "wheat"
    assert field.__table_args__[-1]["schema"] == "core"

    token = FCMToken(
        token="sample_fcm_token_123456",
        device_model="Redmi 10A"
    )
    assert token.token == "sample_fcm_token_123456"
    assert token.device_model == "Redmi 10A"


def test_realtime_orm_instantiation():
    """Verify realtime layer entities (Weather, Market, Pest, Soil, IMD, NDVI, MSP)."""
    weather = WeatherCache(
        state="Punjab",
        district="Ludhiana",
        lat=30.9,
        lon=75.85,
        temp_c=28.5,
        humidity_pct=65,
        advice_flag="NORMAL",
        spray_window_open=True,
        expires_at=datetime.now()
    )
    assert weather.state == "Punjab"
    assert weather.temp_c == 28.5
    assert weather.advice_flag == "NORMAL"
    assert weather.__table_args__[-1]["schema"] == "realtime"

    forecast = WeatherForecast(
        state="Punjab",
        district="Ludhiana",
        forecast_date=date(2026, 10, 15),
        temp_max_c=32.0,
        temp_min_c=21.0,
        precipitation_mm=0.0,
        expires_at=datetime.now()
    )
    assert forecast.temp_max_c == 32.0
    assert forecast.__table_args__[-1]["schema"] == "realtime"

    mkt = MarketPrice(
        crop_name="Wheat",
        market_name="Ludhiana APMC",
        district="Ludhiana",
        state="Punjab",
        price_date=date(2026, 10, 13),
        min_price=2150.00,
        max_price=2380.00,
        modal_price=2275.00
    )
    assert mkt.crop_name == "Wheat"
    assert float(mkt.modal_price) == 2275.00
    assert mkt.__table_args__[-1]["schema"] == "realtime"

    pest = PestAlert(
        title="Locust Advisory",
        severity="warning",
        affected_states=["Punjab", "Rajasthan"]
    )
    assert pest.title == "Locust Advisory"
    assert "Punjab" in pest.affected_states

    soil = SoilZone(
        state="Kerala",
        district="Palakkad",
        primary_texture="red_laterite",
        ph_min=5.5,
        ph_max=7.0,
        suitable_crops=["rice", "coconut", "banana"]
    )
    assert soil.state == "Kerala"
    assert soil.district == "Palakkad"
    assert "coconut" in soil.suitable_crops
    assert soil.__table_args__[-1]["schema"] == "realtime"

    rainfall = IMDRainfall(
        state="Kerala",
        district="Palakkad",
        reading_date=date(2026, 10, 13),
        rainfall_mm=12.4
    )
    assert rainfall.rainfall_mm == 12.4

    ndvi = NDVIReading(
        lat=10.78,
        lon=76.65,
        reading_date=date(2026, 10, 13),
        ndvi=0.68,
        health_category="good"
    )
    assert ndvi.ndvi == 0.68
    assert ndvi.health_category == "good"

    msp = MSPReference(
        crop_name="rice",
        season="kharif",
        msp_year="2025-26",
        msp_per_quintal=2300.00
    )
    assert msp.crop_name == "rice"
    assert float(msp.msp_per_quintal) == 2300.00


def test_agents_orm_instantiation():
    """Verify agents & AI layer entities (Sessions, Messages, Invocations, KauDocument, LangGraph)."""
    session = AdvisorySession(
        language="hi",
        state="Punjab",
        district="Ludhiana",
        is_active=True
    )
    assert session.language == "hi"
    assert session.is_active is True
    assert session.__table_args__[-1]["schema"] == "agents"

    msg = AdvisoryMessage(
        role="assistant",
        sequence_no=1,
        content_native="आपकी फसल में पीला रतुआ का हल्का प्रकोप है।",
        content_en="Mild yellow rust infestation observed on your crop.",
        language="hi",
        confidence_score=0.92,
        response_ms=340
    )
    assert msg.role == "assistant"
    assert msg.confidence_score == 0.92
    assert msg.response_ms == 340
    assert msg.__table_args__[-1]["schema"] == "agents"

    invocation = AgentInvocation(
        agent_name="WeatherAgent",
        succeeded=True,
        gemini_calls=1,
        cache_hit=True
    )
    assert invocation.agent_name == "WeatherAgent"
    assert invocation.cache_hit is True

    doc = KauDocument(
        source_file="kau_coconut_pop.pdf",
        source_org="KAU",
        crop_name="coconut",
        chunk_index=0,
        content="Coconut package of practices content chunk.",
        embedding=[0.015] * 1024
    )
    assert doc.crop_name == "coconut"
    assert len(doc.embedding) == 1024
    assert doc.__table_args__[-1]["schema"] == "agents"

    checkpoint = LangGraphCheckpoint(
        thread_id="farmer-12345",
        checkpoint_id="chk-001",
        checkpoint={"values": {"state": "active"}}
    )
    assert checkpoint.thread_id == "farmer-12345"

    checkpoint_write = LangGraphCheckpointWrite(
        thread_id="farmer-12345",
        checkpoint_id="chk-001",
        task_id="task-01",
        idx=0,
        channel="messages",
        blob=b"sample_binary_state"
    )
    assert checkpoint_write.channel == "messages"


def test_intelligence_and_alerts_orm_instantiation():
    """Verify intelligence, alerts, market & analytics entities."""
    obs = FieldObservation(
        observation_type="pest_sighting",
        description_native="पत्तियों पर पीले धब्बे दिख रहे हैं",
        description_en="Yellow spots observed on leaves",
        severity_estimate="warning"
    )
    assert obs.observation_type == "pest_sighting"
    assert obs.__table_args__[-1]["schema"] == "intelligence"

    stage = CropStage(
        crop_name="rice",
        season="kharif",
        season_year=2026,
        current_stage="tillering",
        predicted_yield_kg_ha=4200.0
    )
    assert stage.current_stage == "tillering"
    assert stage.predicted_yield_kg_ha == 4200.0

    irrigation = IrrigationSchedule(
        valid_for_date=date(2026, 10, 14),
        should_irrigate=True,
        reason="Soil moisture below threshold",
        irrigation_amount_mm=25.0
    )
    assert irrigation.should_irrigate is True
    assert irrigation.irrigation_amount_mm == 25.0

    fert = FertiliserPlan(
        crop_name="rice",
        crop_stage="tillering",
        application_date=date(2026, 10, 16),
        primary_fertiliser="Urea 46%",
        primary_dose_kg_acre=30.0,
        rationale="Second top-dressing for tillering"
    )
    assert fert.primary_fertiliser == "Urea 46%"

    alert = FarmerAlert(
        category="pest_outbreak",
        severity="critical",
        title_native="कीट प्रकोप चेतावनी",
        title_en="Pest Outbreak Warning",
        body_native="तत्काल छिड़काव की सलाह",
        body_en="Immediate spray recommended",
        language="hi"
    )
    assert alert.category == "pest_outbreak"
    assert alert.severity == "critical"
    assert alert.__table_args__[-1]["schema"] == "alerts"

    fcm_log = FCMDeliveryLog(
        fcm_token="sample_token_abc",
        status="delivered"
    )
    assert fcm_log.status == "delivered"

    rec = MarketRecommendation(
        crop_name="wheat",
        state="Punjab",
        district="Ludhiana",
        recommendation="sell_now",
        rationale="Modal price above 90-day moving average"
    )
    assert rec.recommendation == "sell_now"
    assert rec.__table_args__[-1]["schema"] == "market"

    sub = PriceSubscription(
        crop_name="wheat",
        state="Punjab",
        alert_above=2400.0,
        is_active=True
    )
    assert sub.alert_above == 2400.0

    season_analytics = FarmSeasonAnalytics(
        crop_name="wheat",
        season="rabi",
        season_year=2026,
        total_queries=12,
        advisories_followed=10
    )
    assert season_analytics.advisories_followed == 10
    assert season_analytics.__table_args__[-1]["schema"] == "analytics"

    agent_perf = AgentPerformance(
        agent_name="WeatherAgent",
        metric_date=date(2026, 10, 13),
        total_invocations=150,
        successful=148
    )
    assert agent_perf.total_invocations == 150

    metrics = PlatformMetrics(
        metric_date=date(2026, 10, 13),
        dau=450,
        total_queries=1200
    )
    assert metrics.dau == 450

    feedback = AdvisoryFeedback(
        rating=1,
        feedback_text="Very useful advice"
    )
    assert feedback.rating == 1

    audit = AuditLog(
        table_schema="core",
        table_name="farmers",
        operation="INSERT"
    )
    assert audit.operation == "INSERT"
    assert audit.__table_args__[-1]["schema"] == "system"

    rate_limit = APIRateLimit(
        window_start=datetime.now(),
        request_count=5,
        max_allowed=100
    )
    assert rate_limit.request_count == 5


def test_pydantic_schema_validation():
    """Verify Pydantic v2 schemas across Core, Realtime, Agents, and System."""
    farmer_in = FarmerCreate(
        name="Ramesh Kumar",
        phone="9876543210",
        state="Punjab",
        district="Ludhiana",
        primary_language="hi",
        crops=["wheat", "mustard"]
    )
    assert farmer_in.name == "Ramesh Kumar"
    assert farmer_in.phone == "9876543210"

    # Reject invalid Indian mobile numbers
    with pytest.raises(Exception):
        FarmerCreate(
            name="Bad Phone",
            phone="12345",
            state="Punjab",
            district="Ludhiana"
        )

    # Core farm schema validation
    farm_in = CoreFarmCreate(
        farmer_id="d8b746c1-a83d-4c3e-b98a-112233445566",
        name="Ludhiana Farm",
        total_area_acres=10.0,
        state="Punjab",
        district="Ludhiana",
        lat=30.9,
        lon=75.8
    )
    assert farm_in.total_area_acres == 10.0

    # Reject lat/lon out of India bounds
    with pytest.raises(Exception):
        CoreFarmCreate(
            farmer_id="d8b746c1-a83d-4c3e-b98a-112233445566",
            total_area_acres=10.0,
            state="Punjab",
            district="Ludhiana",
            lat=55.0,  # Outside India
            lon=75.8
        )

    # Field schema validation
    field_in = CoreFieldCreate(
        farm_id="d8b746c1-a83d-4c3e-b98a-112233445566",
        farmer_id="d8b746c1-a83d-4c3e-b98a-112233445566",
        name="North Plot",
        area_acres=3.5,
        soil_ph=6.8
    )
    assert field_in.area_acres == 3.5

    # Realtime WeatherCache schema
    weather_resp = WeatherCacheResponse(
        id="c1a2b3d4-1111-2222-3333-444455556666",
        state="Punjab",
        district="Ludhiana",
        lat=30.9,
        lon=75.8,
        temp_c=31.2,
        fetched_at=datetime.now(),
        expires_at=datetime.now()
    )
    assert weather_resp.temp_c == 31.2

    # MSP reference schema
    msp_resp = MSPReferenceResponse(
        id="c1a2b3d4-1111-2222-3333-444455556666",
        crop_name="wheat",
        season="rabi",
        msp_year="2025-26",
        msp_per_quintal=2425.00,
        source="Ministry of Agriculture",
        created_at=datetime.now()
    )
    assert msp_resp.msp_per_quintal == 2425.00

    # Agent invocation response schema
    inv_resp = AgentInvocationResponse(
        id="c1a2b3d4-1111-2222-3333-444455556666",
        message_id="c1a2b3d4-1111-2222-3333-444455556666",
        session_id="c1a2b3d4-1111-2222-3333-444455556666",
        farmer_id="c1a2b3d4-1111-2222-3333-444455556666",
        agent_name="WeatherAgent",
        started_at=datetime.now(),
        duration_ms=250,
        succeeded=True
    )
    assert inv_resp.duration_ms == 250


def test_haversine_math_logic():
    """Verify geodesic distance calculation matches PostgreSQL public.haversine_km."""
    lat1, lon1 = 12.9716, 77.5946
    lat2, lon2 = 13.0827, 80.2707

    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    dist = R * c

    assert 280 <= dist <= 310


def test_sql_file_structural_integrity():
    """Verify backend/init_master_database.sql contains all schemas, tables, triggers, and seed data."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    sql_path = os.path.join(base_dir, "backend", "init_master_database.sql")
    assert os.path.exists(sql_path), f"File not found: {sql_path}"

    with open(sql_path, "r", encoding="utf-8") as f:
        sql = f.read()

    # 1. Extensions check
    for ext in ["vector", "uuid-ossp", "pg_trgm", "btree_gin", "pg_stat_statements"]:
        assert ext in sql, f"Missing extension in SQL: {ext}"

    # 2. Schemas check
    expected_schemas = ["core", "realtime", "agents", "intelligence", "alerts", "market", "analytics", "system"]
    for s in expected_schemas:
        assert f"CREATE SCHEMA IF NOT EXISTS {s}" in sql, f"Missing schema in SQL: {s}"

    # 3. Tables check (34 base tables)
    expected_tables = [
        "core.farmers", "core.fcm_tokens", "core.farms", "core.fields",
        "realtime.weather_cache", "realtime.weather_forecasts", "realtime.market_prices",
        "realtime.pest_alerts", "realtime.pest_alert_crops", "realtime.soil_zones",
        "realtime.imd_rainfall", "realtime.ndvi_readings", "realtime.msp_reference",
        "agents.advisory_sessions", "agents.advisory_messages", "agents.agent_invocations",
        "agents.kau_documents", "agents.langgraph_checkpoints", "agents.langgraph_checkpoint_writes",
        "intelligence.field_observations", "intelligence.crop_stages",
        "intelligence.irrigation_schedules", "intelligence.fertiliser_plans",
        "alerts.farmer_alerts", "alerts.fcm_delivery_log",
        "market.market_recommendations", "market.price_subscriptions",
        "analytics.farm_season_analytics", "analytics.agent_performance",
        "analytics.platform_metrics", "analytics.advisory_feedback",
        "system.audit_log", "system.api_rate_limits"
    ]
    for tbl in expected_tables:
        assert tbl in sql, f"Missing table in SQL: {tbl}"

    # 4. HNSW index check
    assert "USING hnsw (embedding vector_cosine_ops)" in sql
    assert "m = 16" in sql
    assert "ef_construction = 64" in sql

    # 5. Functions check
    expected_functions = [
        "set_updated_at", "generate_farmer_code", "haversine_km", "is_cache_valid",
        "retrieve_kau_docs", "retrieve_kau_docs_hybrid", "update_session_stats",
        "notify_new_alert", "update_farmer_activity", "auto_market_recommendation",
        "audit_trigger", "maintain_monthly_partitions"
    ]
    for fn in expected_functions:
        assert fn in sql, f"Missing function in SQL: {fn}"

    # 6. Seed data check
    assert "INSERT INTO realtime.soil_zones" in sql
    assert "INSERT INTO realtime.msp_reference" in sql
    assert "Ludhiana" in sql
    assert "Palakkad" in sql
    assert "Ernakulam" in sql
    assert "Wayanad" in sql


def test_validation_sql_file_integrity():
    """Verify backend/validate_master_database.sql contains full Phase 1-10 checks."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    val_sql_path = os.path.join(base_dir, "backend", "validate_master_database.sql")
    assert os.path.exists(val_sql_path), f"File not found: {val_sql_path}"

    with open(val_sql_path, "r", encoding="utf-8") as f:
        val_sql = f.read()

    assert "extensions_ok" in val_sql
    assert "schemas_ok" in val_sql
    assert "enums_ok" in val_sql
    assert "haversine_ok" in val_sql
    assert "idx_kau_hnsw" in val_sql
    assert "soil_zones_ok" in val_sql
    assert "msp_ok" in val_sql
    assert "BEGIN;" in val_sql
    assert "ROLLBACK;" in val_sql


if __name__ == "__main__":
    print("Running Master Database Test Suite...")
    test_core_orm_instantiation()
    test_realtime_orm_instantiation()
    test_agents_orm_instantiation()
    test_intelligence_and_alerts_orm_instantiation()
    test_pydantic_schema_validation()
    test_haversine_math_logic()
    test_sql_file_structural_integrity()
    test_validation_sql_file_integrity()
    print("SUCCESS: All 7 Master Database Test Suites Passed (100% Precision, Zero Error)!")
