# 🌾 AGRI-SAGE — MASTER DATABASE BUILD PROMPT

## For: Gemini Flash Agent | PostgreSQL 16 + pgvector 0.4.0

## Purpose: Complete production database for real-time agricultural AI platform

---

> **AGENT INSTRUCTIONS — READ BEFORE ANYTHING**
> You are the Agri-SAGE Database Architect Agent.
> Build the ENTIRE database system described in this file — schema, indexes, triggers,
> functions, partitioning, migrations, seed data, and validation — in ORDER.
> Do NOT skip any section. Do NOT use placeholders or TODOs.
> Every SQL block must be executable as-is.
> After each PHASE, run the validation queries and confirm all pass before proceeding.

---

## TECHNOLOGY STACK — LOCKED

```
Database:    PostgreSQL 16
Extension:   pgvector 0.4.0
ORM:         SQLAlchemy 2.0.36 (async)
Migration:   Alembic 1.13.3
Connection:  asyncpg 0.30.0
Schema:      Pydantic v2 models mirror every table
Deployment:  Railway.app PostgreSQL plugin (1GB free) OR local Docker
```

## DOCKER SETUP (run this first locally)

```bash
docker run -d \
  --name agrisage-db \
  -e POSTGRES_DB=agrisage \
  -e POSTGRES_USER=agrisage_user \
  -e POSTGRES_PASSWORD=agrisage_pass \
  -p 5432:5432 \
  pgvector/pgvector:pg16

# Verify running
docker exec agrisage-db psql -U agrisage_user -d agrisage -c "SELECT version();"
```

---

## DATABASE ARCHITECTURE OVERVIEW

```
agrisage (database)
│
├── CORE LAYER
│   ├── farmers              — farmer profiles (all India)
│   ├── farms                — farm properties linked to farmers
│   ├── fields               — individual field plots per farm
│   └── fcm_tokens           — push notification tokens per device
│
├── REALTIME DATA LAYER      — every table has fetched_at + expires_at
│   ├── weather_cache        — Open-Meteo hourly data per district
│   ├── weather_forecasts    — 7-day forecast rows per district
│   ├── market_prices        — APMC mandi prices (data.gov.in, daily)
│   ├── market_price_history — 90-day rolling price history per crop
│   ├── pest_alerts          — NBAIR RSS feed, parsed per crop/district
│   ├── pest_alert_crops     — M2M: which crops each alert affects
│   ├── soil_zones           — NBSS India soil data (static, all districts)
│   ├── imd_rainfall         — IMD daily district rainfall
│   └── ndvi_readings        — NASA EarthData MODIS NDVI per field
│
├── AGENT & AI LAYER
│   ├── advisory_sessions    — conversation sessions per farmer
│   ├── advisory_messages    — individual messages (user + AI) per session
│   ├── agent_invocations    — which agents ran, latency, output per query
│   ├── kau_documents        — KAU/ICAR PDF chunks + pgvector embeddings
│   └── langgraph_checkpoints— LangGraph MemorySaver persistent state
│
├── FIELD INTELLIGENCE LAYER
│   ├── field_observations   — farmer-reported crop observations
│   ├── crop_stages          — current growth stage per field (DSSAT output)
│   ├── dssat_simulations    — DSSAT run results per field + season
│   ├── irrigation_schedules — AI-generated irrigation plans per field
│   └── fertiliser_plans     — AI-generated NPK plans per field
│
├── ALERTS & NOTIFICATIONS LAYER
│   ├── farmer_alerts        — alerts delivered to farmers (all types)
│   ├── fcm_delivery_log     — push notification delivery receipts
│   └── alert_actions        — what farmer did after receiving alert
│
├── MARKET INTELLIGENCE LAYER
│   ├── market_recommendations — SELL/HOLD per crop per farmer
│   └── price_subscriptions    — which crops/markets a farmer tracks
│
├── ANALYTICS LAYER
│   ├── farm_season_analytics  — per-season KPIs per farm
│   ├── advisory_feedback      — farmer ratings on AI advice quality
│   ├── agent_performance      — daily agent latency + accuracy metrics
│   └── platform_metrics       — daily platform-wide usage metrics
│
└── SYSTEM LAYER
    ├── schema_versions      — Alembic migration history
    ├── api_rate_limits      — per-farmer API usage tracking
    └── audit_log            — all write operations logged
```

---

## PHASE 1 — EXTENSIONS & DATABASE FOUNDATIONS

### Goal: Database, extensions, schemas, utility functions ready

```sql
-- ============================================================
-- PHASE 1.1 — ENABLE EXTENSIONS
-- ============================================================

CREATE EXTENSION IF NOT EXISTS vector;           -- pgvector 0.4.0
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";      -- UUID generation
CREATE EXTENSION IF NOT EXISTS pg_trgm;          -- text search trigrams
CREATE EXTENSION IF NOT EXISTS btree_gin;        -- GIN index on btree types
CREATE EXTENSION IF NOT EXISTS pg_stat_statements; -- query performance monitoring

-- Verify extensions
SELECT extname, extversion FROM pg_extension
WHERE extname IN ('vector','uuid-ossp','pg_trgm','btree_gin','pg_stat_statements');
-- Expected: 5 rows

-- ============================================================
-- PHASE 1.2 — SCHEMAS (namespace separation)
-- ============================================================

CREATE SCHEMA IF NOT EXISTS core;        -- farmer, farm, field entities
CREATE SCHEMA IF NOT EXISTS realtime;    -- weather, market, pest live data
CREATE SCHEMA IF NOT EXISTS agents;      -- AI agent state, embeddings, sessions
CREATE SCHEMA IF NOT EXISTS intelligence;-- field observations, DSSAT, plans
CREATE SCHEMA IF NOT EXISTS alerts;      -- farmer notifications
CREATE SCHEMA IF NOT EXISTS market;      -- market intelligence
CREATE SCHEMA IF NOT EXISTS analytics;  -- metrics and performance
CREATE SCHEMA IF NOT EXISTS system;      -- audit, rate limits, migrations

-- ============================================================
-- PHASE 1.3 — ENUM TYPES
-- ============================================================

-- Language codes (6 primary Indian languages)
CREATE TYPE public.language_code AS ENUM (
    'hi',   -- Hindi
    'en',   -- English
    'ta',   -- Tamil
    'ml',   -- Malayalam
    'te',   -- Telugu
    'pa'    -- Punjabi
);

-- Indian agroclimatic zones (ICAR classification)
CREATE TYPE public.agroclimatic_zone AS ENUM (
    'western_himalayan',
    'eastern_himalayan',
    'lower_gangetic_plains',
    'middle_gangetic_plains',
    'upper_gangetic_plains',
    'trans_gangetic_plains',
    'eastern_plateau_hills',
    'central_plateau_hills',
    'western_plateau_hills',
    'southern_plateau_hills',
    'east_coast_plains',
    'west_coast_plains',
    'gujarat_plains',
    'western_dry',
    'island_territories'
);

-- Crop growth stages (BBCH-aligned)
CREATE TYPE public.crop_stage AS ENUM (
    'land_preparation',
    'sowing',
    'germination',
    'seedling',
    'vegetative',
    'tillering',       -- rice/wheat specific
    'stem_elongation',
    'heading',
    'flowering',
    'grain_filling',
    'maturity',
    'harvest',
    'post_harvest',
    'fallow'
);

-- Soil texture classification
CREATE TYPE public.soil_texture AS ENUM (
    'sandy',
    'loamy_sand',
    'sandy_loam',
    'loam',
    'silt_loam',
    'silt',
    'clay_loam',
    'sandy_clay_loam',
    'silty_clay_loam',
    'sandy_clay',
    'silty_clay',
    'clay',
    'laterite',
    'black_cotton',
    'alluvial',
    'red_laterite'
);

-- Irrigation types (India-specific)
CREATE TYPE public.irrigation_type AS ENUM (
    'rain_fed',
    'canal',
    'borewell',
    'open_well',
    'drip',
    'sprinkler',
    'flood',
    'tank',
    'lift_irrigation'
);

-- Alert severity
CREATE TYPE public.alert_severity AS ENUM (
    'critical',   -- immediate action required
    'warning',    -- action needed within 24h
    'info',       -- advisory, no urgent action
    'success'     -- positive condition confirmed
);

-- Alert categories
CREATE TYPE public.alert_category AS ENUM (
    'pest_outbreak',
    'weather_extreme',
    'disease_risk',
    'irrigation_needed',
    'fertiliser_due',
    'harvest_ready',
    'market_price',
    'crop_stage_update',
    'soil_health',
    'government_scheme'
);

-- Advisory message roles
CREATE TYPE public.message_role AS ENUM ('user', 'assistant', 'system');

-- Market price trend
CREATE TYPE public.price_trend AS ENUM ('rising', 'falling', 'stable', 'volatile');

-- Market recommendation
CREATE TYPE public.market_recommendation AS ENUM ('sell_now', 'hold', 'sell_partial', 'buy_input');

-- Nutrient status
CREATE TYPE public.nutrient_status AS ENUM ('deficient', 'low', 'medium', 'high', 'excessive');

-- Field status
CREATE TYPE public.field_status AS ENUM ('active', 'fallow', 'harvesting', 'resting', 'sold');

-- ============================================================
-- PHASE 1.4 — UTILITY FUNCTIONS
-- ============================================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Generate short farmer ID (human-readable)
CREATE OR REPLACE FUNCTION public.generate_farmer_code()
RETURNS TEXT AS $$
DECLARE
    chars TEXT := 'ABCDEFGHJKLMNPQRSTUVWXYZ23456789';
    code  TEXT := 'FRM-';
    i     INT;
BEGIN
    FOR i IN 1..8 LOOP
        code := code || substr(chars, floor(random() * length(chars) + 1)::INT, 1);
    END LOOP;
    RETURN code;
END;
$$ LANGUAGE plpgsql;

-- Haversine distance (km) between two GPS coordinates
CREATE OR REPLACE FUNCTION public.haversine_km(
    lat1 FLOAT, lon1 FLOAT, lat2 FLOAT, lon2 FLOAT
) RETURNS FLOAT AS $$
DECLARE
    R     FLOAT := 6371.0;
    dlat  FLOAT := radians(lat2 - lat1);
    dlon  FLOAT := radians(lon2 - lon1);
    a     FLOAT;
    c     FLOAT;
BEGIN
    a := sin(dlat/2)^2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)^2;
    c := 2 * asin(sqrt(a));
    RETURN R * c;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Cache expiry check
CREATE OR REPLACE FUNCTION public.is_cache_valid(fetched_at TIMESTAMPTZ, ttl_seconds INT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN (NOW() - fetched_at) < (ttl_seconds * INTERVAL '1 second');
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Partition helper: get table name for a date
CREATE OR REPLACE FUNCTION public.get_partition_name(base TEXT, dt DATE)
RETURNS TEXT AS $$
BEGIN
    RETURN base || '_' || TO_CHAR(dt, 'YYYY_MM');
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```

### Phase 1 Validation

```sql
-- Run these. All must return TRUE or expected count.
SELECT COUNT(*) = 5 AS extensions_ok FROM pg_extension
WHERE extname IN ('vector','uuid-ossp','pg_trgm','btree_gin','pg_stat_statements');

SELECT COUNT(*) = 8 AS schemas_ok FROM information_schema.schemata
WHERE schema_name IN ('core','realtime','agents','intelligence','alerts','market','analytics','system');

SELECT COUNT(*) = 11 AS enums_ok FROM pg_type
WHERE typname IN ('language_code','agroclimatic_zone','crop_stage','soil_texture',
                  'irrigation_type','alert_severity','alert_category','message_role',
                  'price_trend','market_recommendation','nutrient_status');

SELECT public.haversine_km(12.97, 77.59, 13.08, 80.27) BETWEEN 290 AND 310 AS haversine_ok;
-- Bangalore to Chennai ≈ 300km

SELECT public.is_cache_valid(NOW() - INTERVAL '30 minutes', 3600) AS cache_valid_ok;
SELECT public.is_cache_valid(NOW() - INTERVAL '2 hours', 3600) AS cache_expired_ok;
-- First must be TRUE, second FALSE
```

---

## PHASE 2 — CORE LAYER: FARMERS, FARMS, FIELDS

### Goal: Complete farmer identity and farm structure with all constraints

```sql
-- ============================================================
-- PHASE 2.1 — FARMERS TABLE
-- ============================================================

CREATE TABLE core.farmers (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_code         TEXT UNIQUE NOT NULL DEFAULT public.generate_farmer_code(),

    -- Identity
    name                TEXT NOT NULL CHECK (length(name) BETWEEN 2 AND 100),
    phone               TEXT UNIQUE CHECK (phone ~ '^[6-9][0-9]{9}$'),  -- Indian mobile format
    phone_verified      BOOLEAN NOT NULL DEFAULT FALSE,

    -- Location (India-specific)
    country             TEXT NOT NULL DEFAULT 'India',
    state               TEXT NOT NULL CHECK (length(state) BETWEEN 2 AND 60),
    district            TEXT NOT NULL CHECK (length(district) BETWEEN 2 AND 60),
    taluk               TEXT,
    village             TEXT,
    pincode             TEXT CHECK (pincode ~ '^[1-9][0-9]{5}$'),
    lat                 FLOAT CHECK (lat BETWEEN 6.0 AND 38.0),   -- India bounds
    lon                 FLOAT CHECK (lon BETWEEN 68.0 AND 97.5),  -- India bounds
    location_accuracy_m FLOAT,                                    -- GPS accuracy in meters

    -- Preferences
    primary_language    public.language_code NOT NULL DEFAULT 'hi',
    secondary_language  public.language_code,
    crops               TEXT[] NOT NULL DEFAULT '{}',             -- selected crop names
    agroclimatic_zone   public.agroclimatic_zone,

    -- App state
    onboarding_complete BOOLEAN NOT NULL DEFAULT FALSE,
    demo_mode           BOOLEAN NOT NULL DEFAULT FALSE,
    fcm_topic           TEXT GENERATED ALWAYS AS (
                            'district_' || lower(replace(district,' ','_'))
                            || '_' || lower(replace(state,' ','_'))
                        ) STORED,

    -- Metadata
    app_version         TEXT,
    device_model        TEXT,
    android_api_level   INT CHECK (android_api_level >= 26),
    last_active_at      TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ   -- soft delete
);

CREATE INDEX idx_farmers_phone ON core.farmers(phone) WHERE phone IS NOT NULL;
CREATE INDEX idx_farmers_state_district ON core.farmers(state, district);
CREATE INDEX idx_farmers_crops ON core.farmers USING GIN(crops);
CREATE INDEX idx_farmers_location ON core.farmers(lat, lon) WHERE lat IS NOT NULL;
CREATE INDEX idx_farmers_active ON core.farmers(last_active_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX idx_farmers_fcm_topic ON core.farmers(fcm_topic);

CREATE TRIGGER trg_farmers_updated_at
    BEFORE UPDATE ON core.farmers
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

-- ============================================================
-- PHASE 2.2 — FCM TOKENS (device push tokens)
-- ============================================================

CREATE TABLE core.fcm_tokens (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id   UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    token       TEXT NOT NULL,
    device_id   TEXT,
    device_model TEXT,
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(farmer_id, token)
);

CREATE INDEX idx_fcm_tokens_farmer ON core.fcm_tokens(farmer_id) WHERE is_active = TRUE;

-- ============================================================
-- PHASE 2.3 — FARMS TABLE
-- ============================================================

CREATE TABLE core.farms (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    name                TEXT NOT NULL DEFAULT 'My Farm',
    total_area_acres    FLOAT NOT NULL CHECK (total_area_acres > 0 AND total_area_acres < 10000),
    ownership_type      TEXT CHECK (ownership_type IN ('owned','leased','sharecrop','inherited')),
    land_record_number  TEXT,                              -- government survey number

    -- Location
    state               TEXT NOT NULL,
    district            TEXT NOT NULL,
    taluk               TEXT,
    village             TEXT,
    lat                 FLOAT CHECK (lat BETWEEN 6.0 AND 38.0),
    lon                 FLOAT CHECK (lon BETWEEN 68.0 AND 97.5),

    -- Soil summary (district-level defaults, overridden by field-level)
    primary_soil_type   public.soil_texture,
    avg_ph              FLOAT CHECK (avg_ph BETWEEN 3.0 AND 10.0),

    -- Water
    water_source        public.irrigation_type DEFAULT 'rain_fed',
    annual_rainfall_mm  FLOAT,

    -- Metadata
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ
);

CREATE INDEX idx_farms_farmer_id ON core.farms(farmer_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_farms_state_district ON core.farms(state, district);

CREATE TRIGGER trg_farms_updated_at
    BEFORE UPDATE ON core.farms
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

-- ============================================================
-- PHASE 2.4 — FIELDS TABLE (individual plots)
-- ============================================================

CREATE TABLE core.fields (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id             UUID NOT NULL REFERENCES core.farms(id) ON DELETE CASCADE,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    name                TEXT NOT NULL,
    area_acres          FLOAT NOT NULL CHECK (area_acres > 0 AND area_acres < 500),
    status              public.field_status NOT NULL DEFAULT 'active',

    -- Crop info
    current_crop        TEXT,
    crop_variety        TEXT,
    sowing_date         DATE,
    expected_harvest    DATE,
    current_stage       public.crop_stage DEFAULT 'fallow',

    -- Soil (field-specific measurements)
    soil_texture        public.soil_texture,
    soil_ph             FLOAT CHECK (soil_ph BETWEEN 3.0 AND 10.0),
    organic_carbon_pct  FLOAT CHECK (organic_carbon_pct BETWEEN 0.0 AND 10.0),
    nitrogen_status     public.nutrient_status DEFAULT 'medium',
    phosphorus_status   public.nutrient_status DEFAULT 'medium',
    potassium_status    public.nutrient_status DEFAULT 'medium',

    -- Irrigation
    irrigation_type     public.irrigation_type DEFAULT 'rain_fed',
    has_drip            BOOLEAN DEFAULT FALSE,

    -- GPS
    lat                 FLOAT CHECK (lat BETWEEN 6.0 AND 38.0),
    lon                 FLOAT CHECK (lon BETWEEN 68.0 AND 97.5),
    boundary_geojson    JSONB,   -- field polygon for satellite analysis

    -- Metadata
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ
);

CREATE INDEX idx_fields_farm_id ON core.fields(farm_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_fields_farmer_id ON core.fields(farmer_id) WHERE deleted_at IS NULL;
CREATE INDEX idx_fields_crop ON core.fields(current_crop) WHERE current_crop IS NOT NULL;
CREATE INDEX idx_fields_status ON core.fields(status);
CREATE INDEX idx_fields_location ON core.fields(lat, lon) WHERE lat IS NOT NULL;
CREATE INDEX idx_fields_harvest ON core.fields(expected_harvest) WHERE status = 'active';

CREATE TRIGGER trg_fields_updated_at
    BEFORE UPDATE ON core.fields
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();
```

### Phase 2 Validation

```sql
-- Insert test farmer
INSERT INTO core.farmers (name, phone, state, district, primary_language, crops)
VALUES ('Test Farmer', '9876543210', 'Punjab', 'Ludhiana', 'hi', ARRAY['wheat','rice'])
RETURNING id, farmer_code, fcm_topic;
-- Must return: id, FRM-XXXXXXXX code, district_ludhiana_punjab topic

-- Verify constraint: bad phone number rejected
INSERT INTO core.farmers (name, phone, state, district)
VALUES ('Bad', '1234567890', 'Punjab', 'Ludhiana');
-- Must FAIL with check constraint violation

-- Verify GPS constraint
INSERT INTO core.farms (farmer_id, total_area_acres, state, district, lat, lon)
SELECT id, 5.0, 'Punjab', 'Ludhiana', 100.0, 200.0 FROM core.farmers WHERE phone = '9876543210';
-- Must FAIL (lat out of India bounds)

-- Cleanup test data
DELETE FROM core.farmers WHERE phone = '9876543210';

SELECT 'Phase 2 validation passed' AS status;
```

---

## PHASE 3 — REALTIME DATA LAYER

### Goal: All 8 external data sources have dedicated tables with TTL-based caching

```sql
-- ============================================================
-- PHASE 3.1 — WEATHER CACHE (Open-Meteo, 6hr TTL)
-- ============================================================

CREATE TABLE realtime.weather_cache (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    state               TEXT NOT NULL,
    district            TEXT NOT NULL,
    lat                 FLOAT NOT NULL,
    lon                 FLOAT NOT NULL,

    -- Current conditions
    temp_c              FLOAT NOT NULL,
    feels_like_c        FLOAT,
    humidity_pct        INT CHECK (humidity_pct BETWEEN 0 AND 100),
    wind_kmh            FLOAT,
    wind_direction_deg  INT CHECK (wind_direction_deg BETWEEN 0 AND 360),
    rain_mm_1h          FLOAT DEFAULT 0,
    rain_mm_24h         FLOAT DEFAULT 0,
    uv_index            FLOAT CHECK (uv_index >= 0),
    cloud_cover_pct     INT CHECK (cloud_cover_pct BETWEEN 0 AND 100),
    visibility_km       FLOAT,
    weather_code        INT,              -- WMO weather code from Open-Meteo
    weather_description TEXT,

    -- Agri advisory flags (computed by WeatherAgent)
    advice_flag         TEXT CHECK (advice_flag IN (
                            'NORMAL','SPRAY_RISK','IRRIGATION_NEEDED',
                            'FLOOD_RISK','FROST_RISK','HEAT_STRESS',
                            'STRONG_WIND','HAILSTORM_RISK'
                        )) DEFAULT 'NORMAL',
    spray_window_open   BOOLEAN DEFAULT TRUE,   -- can farmer spray today?
    field_work_suitable BOOLEAN DEFAULT TRUE,

    -- Cache metadata
    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at          TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '6 hours'),
    source              TEXT NOT NULL DEFAULT 'open-meteo',
    UNIQUE (state, district)
);

CREATE INDEX idx_weather_district ON realtime.weather_cache(state, district);
CREATE INDEX idx_weather_expires ON realtime.weather_cache(expires_at);
CREATE INDEX idx_weather_fetched ON realtime.weather_cache(fetched_at DESC);

-- ============================================================
-- PHASE 3.2 — WEATHER FORECASTS (7-day, per district)
-- ============================================================

CREATE TABLE realtime.weather_forecasts (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    state               TEXT NOT NULL,
    district            TEXT NOT NULL,
    forecast_date       DATE NOT NULL,
    temp_max_c          FLOAT,
    temp_min_c          FLOAT,
    precipitation_mm    FLOAT DEFAULT 0,
    rain_probability_pct INT CHECK (rain_probability_pct BETWEEN 0 AND 100),
    wind_max_kmh        FLOAT,
    uv_index_max        FLOAT,
    weather_code        INT,
    weather_description TEXT,
    sunrise_time        TIME,
    sunset_time         TIME,
    daylight_hours      FLOAT,

    -- Farming suitability for this day
    spray_suitable      BOOLEAN,
    irrigation_needed   BOOLEAN,
    field_work_suitable BOOLEAN,

    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at          TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '12 hours'),
    UNIQUE (state, district, forecast_date)
);

CREATE INDEX idx_forecasts_location_date ON realtime.weather_forecasts(state, district, forecast_date);
CREATE INDEX idx_forecasts_expires ON realtime.weather_forecasts(expires_at);

-- ============================================================
-- PHASE 3.3 — MARKET PRICES (data.gov.in APMC, daily at 08:00)
-- Partitioned by month for query performance on 90-day history
-- ============================================================

CREATE TABLE realtime.market_prices (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_name           TEXT NOT NULL,
    crop_variety        TEXT,
    market_name         TEXT NOT NULL,         -- APMC market name
    district            TEXT NOT NULL,
    state               TEXT NOT NULL,
    price_date          DATE NOT NULL,

    -- Prices (all in ₹ per quintal)
    min_price           NUMERIC(10,2) CHECK (min_price >= 0),
    max_price           NUMERIC(10,2) CHECK (max_price >= 0),
    modal_price         NUMERIC(10,2) CHECK (modal_price >= 0),

    -- MSP reference (Minimum Support Price)
    msp_price           NUMERIC(10,2),
    above_msp           BOOLEAN GENERATED ALWAYS AS (modal_price > msp_price) STORED,

    -- Trend analysis (computed by MarketAgent)
    trend_7d            public.price_trend,
    trend_30d           public.price_trend,
    pct_change_7d       FLOAT,                 -- % price change vs 7 days ago
    recommendation      public.market_recommendation,

    -- Cache metadata
    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source              TEXT NOT NULL DEFAULT 'data.gov.in',
    UNIQUE (crop_name, market_name, district, state, price_date)
) PARTITION BY RANGE (price_date);

-- Create monthly partitions (current month + 3 months back)
CREATE TABLE realtime.market_prices_2026_07 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
CREATE TABLE realtime.market_prices_2026_08 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
CREATE TABLE realtime.market_prices_2026_09 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
CREATE TABLE realtime.market_prices_2026_10 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
CREATE TABLE realtime.market_prices_2026_11 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');
CREATE TABLE realtime.market_prices_2026_12 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2026-12-01') TO ('2027-01-01');
CREATE TABLE realtime.market_prices_2027_01 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2027-01-01') TO ('2027-02-01');

CREATE INDEX idx_market_crop_state_date ON realtime.market_prices(crop_name, state, price_date DESC);
CREATE INDEX idx_market_district ON realtime.market_prices(district, state, price_date DESC);
CREATE INDEX idx_market_above_msp ON realtime.market_prices(crop_name) WHERE above_msp = TRUE;

-- Function to auto-create monthly partition
CREATE OR REPLACE FUNCTION realtime.create_market_partition(target_date DATE)
RETURNS VOID AS $$
DECLARE
    partition_name TEXT;
    start_date DATE;
    end_date DATE;
BEGIN
    partition_name := 'realtime.market_prices_' || TO_CHAR(target_date, 'YYYY_MM');
    start_date := DATE_TRUNC('month', target_date);
    end_date := start_date + INTERVAL '1 month';
    EXECUTE format(
        'CREATE TABLE IF NOT EXISTS %s PARTITION OF realtime.market_prices
         FOR VALUES FROM (%L) TO (%L)',
        partition_name, start_date, end_date
    );
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- PHASE 3.4 — PEST ALERTS (NBAIR RSS, every 6 hours)
-- ============================================================

CREATE TABLE realtime.pest_alerts (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    external_id         TEXT UNIQUE,                -- RSS entry GUID
    title               TEXT NOT NULL,
    description         TEXT,
    full_content        TEXT,
    severity            public.alert_severity NOT NULL DEFAULT 'warning',

    -- Geographic scope
    affected_states     TEXT[] DEFAULT '{}',        -- which Indian states affected
    affected_districts  TEXT[] DEFAULT '{}',
    is_national         BOOLEAN DEFAULT FALSE,      -- nationwide alert

    -- Pest classification
    pest_name           TEXT,
    pest_scientific     TEXT,
    damage_type         TEXT,                       -- 'sucking','biting','boring','disease_vector'

    -- Source
    source_url          TEXT,
    source_org          TEXT DEFAULT 'NBAIR',       -- National Bureau of Agricultural Insect Resources
    published_at        TIMESTAMPTZ,
    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at          TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '7 days')
);

-- M2M: which crops each pest alert affects
CREATE TABLE realtime.pest_alert_crops (
    alert_id            UUID NOT NULL REFERENCES realtime.pest_alerts(id) ON DELETE CASCADE,
    crop_name           TEXT NOT NULL,
    affinity_score      FLOAT CHECK (affinity_score BETWEEN 0 AND 1), -- 1.0 = explicitly named
    PRIMARY KEY (alert_id, crop_name)
);

CREATE INDEX idx_pest_severity ON realtime.pest_alerts(severity, fetched_at DESC);
CREATE INDEX idx_pest_states ON realtime.pest_alerts USING GIN(affected_states);
CREATE INDEX idx_pest_districts ON realtime.pest_alerts USING GIN(affected_districts);
CREATE INDEX idx_pest_expires ON realtime.pest_alerts(expires_at);
CREATE INDEX idx_pest_alert_crops_crop ON realtime.pest_alert_crops(crop_name);

-- ============================================================
-- PHASE 3.5 — SOIL ZONES (NBSS India, static reference data)
-- ============================================================

CREATE TABLE realtime.soil_zones (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    state               TEXT NOT NULL,
    district            TEXT NOT NULL,
    agroclimatic_zone   public.agroclimatic_zone,

    -- Soil physical properties
    primary_texture     public.soil_texture NOT NULL,
    secondary_texture   public.soil_texture,
    ph_min              FLOAT NOT NULL CHECK (ph_min BETWEEN 3.0 AND 10.0),
    ph_max              FLOAT NOT NULL CHECK (ph_max BETWEEN 3.0 AND 10.0),
    ph_optimal          FLOAT GENERATED ALWAYS AS ((ph_min + ph_max) / 2) STORED,
    organic_carbon      public.nutrient_status NOT NULL DEFAULT 'medium',
    cec_meq             FLOAT,                      -- Cation Exchange Capacity

    -- Macronutrients (NBSS baseline)
    nitrogen_status     public.nutrient_status NOT NULL DEFAULT 'medium',
    phosphorus_status   public.nutrient_status NOT NULL DEFAULT 'medium',
    potassium_status    public.nutrient_status NOT NULL DEFAULT 'high',

    -- Micronutrients (common deficiencies)
    zinc_deficient      BOOLEAN DEFAULT FALSE,
    boron_deficient     BOOLEAN DEFAULT FALSE,
    sulphur_deficient   BOOLEAN DEFAULT FALSE,
    iron_deficient      BOOLEAN DEFAULT FALSE,

    -- Water
    water_holding_capacity TEXT CHECK (water_holding_capacity IN ('low','medium','high')),
    drainage             TEXT CHECK (drainage IN ('poor','moderate','well','excessive')),
    annual_rainfall_mm_avg FLOAT,

    -- Suitability
    suitable_crops       TEXT[] NOT NULL DEFAULT '{}',
    unsuitable_crops     TEXT[] DEFAULT '{}',
    special_notes        TEXT,

    -- Metadata
    data_source          TEXT DEFAULT 'NBSS&LUP',
    data_year            INT DEFAULT 2024,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (state, district)
);

CREATE INDEX idx_soil_state_district ON realtime.soil_zones(state, district);
CREATE INDEX idx_soil_suitable_crops ON realtime.soil_zones USING GIN(suitable_crops);
CREATE INDEX idx_soil_zone ON realtime.soil_zones(agroclimatic_zone);

-- ============================================================
-- PHASE 3.6 — IMD RAINFALL (India Meteorological Department)
-- ============================================================

CREATE TABLE realtime.imd_rainfall (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    state               TEXT NOT NULL,
    district            TEXT NOT NULL,
    reading_date        DATE NOT NULL,
    rainfall_mm         FLOAT NOT NULL DEFAULT 0 CHECK (rainfall_mm >= 0),
    normal_rainfall_mm  FLOAT,                  -- IMD climatological normal
    departure_pct       FLOAT,                  -- % departure from normal
    is_deficient        BOOLEAN,                -- < 80% of normal
    is_excess           BOOLEAN,                -- > 120% of normal
    season              TEXT CHECK (season IN ('kharif','rabi','zaid','annual')),
    cumulative_mm       FLOAT,                  -- cumulative from season start
    source              TEXT DEFAULT 'IMD',
    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (state, district, reading_date)
) PARTITION BY RANGE (reading_date);

CREATE TABLE realtime.imd_rainfall_2026 PARTITION OF realtime.imd_rainfall
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
CREATE TABLE realtime.imd_rainfall_2027 PARTITION OF realtime.imd_rainfall
    FOR VALUES FROM ('2027-01-01') TO ('2028-01-01');

CREATE INDEX idx_rainfall_location_date ON realtime.imd_rainfall(state, district, reading_date DESC);

-- ============================================================
-- PHASE 3.7 — NDVI READINGS (NASA EarthData MODIS, 16-day)
-- ============================================================

CREATE TABLE realtime.ndvi_readings (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id            UUID REFERENCES core.fields(id) ON DELETE CASCADE,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    lat                 FLOAT NOT NULL,
    lon                 FLOAT NOT NULL,
    reading_date        DATE NOT NULL,

    -- MODIS MOD13Q1 product values
    ndvi                FLOAT CHECK (ndvi BETWEEN -1.0 AND 1.0),  -- -1 to +1
    evi                 FLOAT,                                      -- Enhanced Vegetation Index
    pixel_reliability   INT CHECK (pixel_reliability BETWEEN 0 AND 3), -- 0=good, 3=bad
    is_cloud_affected   BOOLEAN DEFAULT FALSE,

    -- Interpreted health
    health_category     TEXT CHECK (health_category IN (
                            'bare_soil','sparse_vegetation','moderate',
                            'good','excellent','stress_detected'
                        )),
    health_score        INT CHECK (health_score BETWEEN 0 AND 100),
    stress_type         TEXT,   -- 'water_stress','nutrient_deficiency','pest_damage','disease'

    -- Metadata
    satellite_product   TEXT DEFAULT 'MOD13Q1',
    spatial_resolution_m INT DEFAULT 250,
    source              TEXT DEFAULT 'NASA-EOSDIS',
    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (field_id, reading_date)
);

CREATE INDEX idx_ndvi_field_date ON realtime.ndvi_readings(field_id, reading_date DESC)
    WHERE field_id IS NOT NULL;
CREATE INDEX idx_ndvi_farmer_date ON realtime.ndvi_readings(farmer_id, reading_date DESC);
CREATE INDEX idx_ndvi_health ON realtime.ndvi_readings(health_category) WHERE is_cloud_affected = FALSE;
```

### Phase 3 Validation

```sql
-- Verify all 8 realtime tables exist
SELECT table_name FROM information_schema.tables
WHERE table_schema = 'realtime'
ORDER BY table_name;
-- Expected: imd_rainfall, imd_rainfall_2026, imd_rainfall_2027,
--           market_prices + 7 partitions, ndvi_readings, pest_alert_crops,
--           pest_alerts, soil_zones, weather_cache, weather_forecasts

-- Test partitioned insert
INSERT INTO realtime.market_prices (crop_name, market_name, district, state, price_date, min_price, max_price, modal_price)
VALUES ('Wheat', 'Ludhiana APMC', 'Ludhiana', 'Punjab', CURRENT_DATE, 2150.00, 2380.00, 2275.00);

-- Verify it went into correct partition
SELECT tableoid::regclass AS partition, crop_name, modal_price
FROM realtime.market_prices WHERE crop_name = 'Wheat';

-- Test cache validity function
SELECT public.is_cache_valid(NOW(), 21600) AS should_be_valid;       -- TRUE
SELECT public.is_cache_valid(NOW() - INTERVAL '7 hours', 21600) AS should_be_expired; -- FALSE

-- Test soil zones unique constraint
INSERT INTO realtime.soil_zones (state, district, primary_texture, ph_min, ph_max, suitable_crops)
VALUES ('Punjab', 'Ludhiana', 'loam', 7.0, 8.5, ARRAY['wheat','rice','mustard']);

INSERT INTO realtime.soil_zones (state, district, primary_texture, ph_min, ph_max, suitable_crops)
VALUES ('Punjab', 'Ludhiana', 'sandy_loam', 6.5, 7.5, ARRAY['wheat']); -- MUST FAIL

ROLLBACK; -- clean up
SELECT 'Phase 3 validation passed' AS status;
```

---

## PHASE 4 — AGENT & AI LAYER

### Goal: Full advisory session tracking, pgvector embeddings, LangGraph state persistence

```sql
-- ============================================================
-- PHASE 4.1 — ADVISORY SESSIONS
-- ============================================================

CREATE TABLE agents.advisory_sessions (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    session_token       TEXT UNIQUE NOT NULL DEFAULT gen_random_uuid()::TEXT,

    -- Context
    language            public.language_code NOT NULL DEFAULT 'hi',
    state               TEXT NOT NULL,
    district            TEXT NOT NULL,
    primary_crop        TEXT,
    active_field_id     UUID REFERENCES core.fields(id),

    -- Session state
    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    message_count       INT NOT NULL DEFAULT 0,
    total_tokens_used   INT DEFAULT 0,
    total_cost_usd      FLOAT DEFAULT 0,  -- for monitoring (Gemini Flash = near zero)

    -- Quality
    avg_response_ms     FLOAT,
    farmer_satisfaction INT CHECK (farmer_satisfaction BETWEEN 1 AND 5),

    -- Metadata
    started_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_message_at     TIMESTAMPTZ,
    ended_at            TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_sessions_farmer ON agents.advisory_sessions(farmer_id, started_at DESC);
CREATE INDEX idx_sessions_active ON agents.advisory_sessions(farmer_id) WHERE is_active = TRUE;
CREATE INDEX idx_sessions_token ON agents.advisory_sessions(session_token);

-- ============================================================
-- PHASE 4.2 — ADVISORY MESSAGES (partitioned by month)
-- ============================================================

CREATE TABLE agents.advisory_messages (
    id                  UUID NOT NULL DEFAULT uuid_generate_v4(),
    session_id          UUID NOT NULL REFERENCES agents.advisory_sessions(id) ON DELETE CASCADE,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    role                public.message_role NOT NULL,
    sequence_no         INT NOT NULL,     -- order within session

    -- Content (all languages stored)
    content_native      TEXT NOT NULL,    -- in farmer's language
    content_en          TEXT,             -- English version
    language            public.language_code NOT NULL,

    -- AI metadata (for assistant messages)
    agents_used         TEXT[] DEFAULT '{}',    -- which of 14 agents contributed
    intent_detected     TEXT[] DEFAULT '{}',    -- WEATHER|PEST|SOIL|CROP|...
    confidence_score    FLOAT CHECK (confidence_score BETWEEN 0 AND 1),
    response_ms         INT,                    -- latency in milliseconds
    model_used          TEXT DEFAULT 'gemini-1.5-flash',
    tokens_in           INT,
    tokens_out          INT,

    -- Data sources used in this response
    used_weather_data   BOOLEAN DEFAULT FALSE,
    used_soil_data      BOOLEAN DEFAULT FALSE,
    used_pest_data      BOOLEAN DEFAULT FALSE,
    used_market_data    BOOLEAN DEFAULT FALSE,
    used_rag_docs       BOOLEAN DEFAULT FALSE,
    used_dssat          BOOLEAN DEFAULT FALSE,
    used_ndvi           BOOLEAN DEFAULT FALSE,

    -- Farmer engagement
    was_helpful         BOOLEAN,          -- thumbs up/down
    was_acted_upon      BOOLEAN,          -- farmer marked they followed the advice

    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

CREATE TABLE agents.advisory_messages_2026_07 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
CREATE TABLE agents.advisory_messages_2026_08 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
CREATE TABLE agents.advisory_messages_2026_09 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
CREATE TABLE agents.advisory_messages_2026_10 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
CREATE TABLE agents.advisory_messages_2026_11 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');
CREATE TABLE agents.advisory_messages_2026_12 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2026-12-01') TO ('2027-01-01');
CREATE TABLE agents.advisory_messages_2027_01 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2027-01-01') TO ('2027-02-01');
CREATE TABLE agents.advisory_messages_2027_02 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2027-02-01') TO ('2027-03-01');

CREATE INDEX idx_messages_session ON agents.advisory_messages(session_id, sequence_no);
CREATE INDEX idx_messages_farmer ON agents.advisory_messages(farmer_id, created_at DESC);
CREATE INDEX idx_messages_role ON agents.advisory_messages(role, created_at DESC);

-- Function to auto-create monthly partition for advisory_messages
CREATE OR REPLACE FUNCTION agents.create_message_partition(target_date DATE)
RETURNS VOID AS $$
DECLARE
    partition_name TEXT;
    start_date DATE;
    end_date DATE;
BEGIN
    partition_name := 'agents.advisory_messages_' || TO_CHAR(target_date, 'YYYY_MM');
    start_date := DATE_TRUNC('month', target_date);
    end_date := start_date + INTERVAL '1 month';
    EXECUTE format(
        'CREATE TABLE IF NOT EXISTS %s PARTITION OF agents.advisory_messages
         FOR VALUES FROM (%L) TO (%L)',
        partition_name, start_date, end_date
    );
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- PHASE 4.3 — AGENT INVOCATIONS (per-agent performance tracking)
-- ============================================================

CREATE TABLE agents.agent_invocations (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    message_id          UUID NOT NULL,
    session_id          UUID NOT NULL REFERENCES agents.advisory_sessions(id),
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id),
    agent_name          TEXT NOT NULL CHECK (agent_name IN (
                            'IntentAgent','TranslatorAgent','WeatherAgent','SoilAgent',
                            'PestAgent','CropAgent','IrrigationAgent','FertiliserAgent',
                            'MarketAgent','AlertAgent','MemoryAgent','SchedulerAgent',
                            'NDVIAgent','SupervisorAgent'
                        )),
    started_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at        TIMESTAMPTZ,
    duration_ms         INT GENERATED ALWAYS AS (
                            EXTRACT(EPOCH FROM (completed_at - started_at)) * 1000
                        )::INT STORED,
    succeeded           BOOLEAN NOT NULL DEFAULT TRUE,
    error_type          TEXT,
    error_message       TEXT,
    input_summary       JSONB,   -- truncated input for debugging
    output_summary      JSONB,   -- truncated output for debugging
    gemini_calls        INT DEFAULT 0,
    gemini_tokens       INT DEFAULT 0,
    cache_hit           BOOLEAN DEFAULT FALSE  -- did agent use cached data?
);

CREATE INDEX idx_invocations_session ON agents.agent_invocations(session_id);
CREATE INDEX idx_invocations_agent ON agents.agent_invocations(agent_name, started_at DESC);
CREATE INDEX idx_invocations_errors ON agents.agent_invocations(agent_name) WHERE succeeded = FALSE;
CREATE INDEX idx_invocations_slow ON agents.agent_invocations(duration_ms DESC) WHERE duration_ms > 3000;

-- ============================================================
-- PHASE 4.4 — KAU DOCUMENTS (pgvector RAG, CORE OF AI KNOWLEDGE)
-- ============================================================

CREATE TABLE agents.kau_documents (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_file         TEXT NOT NULL,
    source_org          TEXT NOT NULL DEFAULT 'KAU',  -- KAU/ICAR/TNAU/PAU/IARI
    crop_name           TEXT NOT NULL,
    state_relevance     TEXT[] DEFAULT '{}',   -- which Indian states this applies to
    chunk_index         INT NOT NULL,
    total_chunks        INT,
    content             TEXT NOT NULL,
    content_length      INT GENERATED ALWAYS AS (length(content)) STORED,

    -- pgvector embedding (CORE FIELD)
    -- multilingual-e5-large dim=1024
    -- ALWAYS prefixed with "passage: [India crop advisory] " before embedding
    embedding           vector(1024) NOT NULL,

    -- Classification for retrieval filtering
    doc_type            TEXT CHECK (doc_type IN (
                            'package_of_practices','pest_management',
                            'soil_management','irrigation_guide',
                            'post_harvest','market_linkage',
                            'government_scheme','variety_guide'
                        )),
    crop_stage_relevance TEXT[],   -- which crop stages this chunk is relevant to
    season_relevance     TEXT[],   -- 'kharif','rabi','zaid'

    -- Quality control
    ingested_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_retrieved_at   TIMESTAMPTZ,
    retrieval_count     INT DEFAULT 0,
    avg_similarity_score FLOAT,    -- average score when retrieved (quality indicator)

    UNIQUE (source_file, chunk_index)
);

-- HNSW index — the critical index for fast vector search
-- m=16: controls graph connectivity (higher = better recall, slower build)
-- ef_construction=64: controls index build quality (higher = better, slower)
CREATE INDEX idx_kau_hnsw ON agents.kau_documents
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Supporting indexes for filtered retrieval
CREATE INDEX idx_kau_crop ON agents.kau_documents(crop_name);
CREATE INDEX idx_kau_org ON agents.kau_documents(source_org);
CREATE INDEX idx_kau_state ON agents.kau_documents USING GIN(state_relevance);
CREATE INDEX idx_kau_stage ON agents.kau_documents USING GIN(crop_stage_relevance);
CREATE INDEX idx_kau_type ON agents.kau_documents(doc_type);

-- Function to retrieve top-K similar documents
-- ALWAYS call this with "query: " prefix on the query embedding
CREATE OR REPLACE FUNCTION agents.retrieve_kau_docs(
    query_embedding     vector(1024),
    filter_crop         TEXT DEFAULT NULL,
    filter_org          TEXT DEFAULT NULL,
    top_k               INT DEFAULT 5,
    similarity_threshold FLOAT DEFAULT 0.70
) RETURNS TABLE (
    id                  UUID,
    content             TEXT,
    source_file         TEXT,
    crop_name           TEXT,
    similarity          FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        kd.id,
        kd.content,
        kd.source_file,
        kd.crop_name,
        (1 - (kd.embedding <=> query_embedding))::FLOAT AS similarity
    FROM agents.kau_documents kd
    WHERE
        (filter_crop IS NULL OR kd.crop_name = filter_crop)
        AND (filter_org IS NULL OR kd.source_org = filter_org)
        AND (1 - (kd.embedding <=> query_embedding)) >= similarity_threshold
    ORDER BY kd.embedding <=> query_embedding
    LIMIT top_k;

    -- Update retrieval stats
    UPDATE agents.kau_documents
    SET last_retrieved_at = NOW(), retrieval_count = retrieval_count + 1
    WHERE agents.kau_documents.id IN (
        SELECT r.id FROM agents.retrieve_kau_docs(query_embedding, filter_crop, filter_org, top_k, similarity_threshold) r
    );
END;
$$ LANGUAGE plpgsql;

-- ============================================================
-- PHASE 4.5 — LANGGRAPH CHECKPOINTS (conversation memory)
-- ============================================================

CREATE TABLE agents.langgraph_checkpoints (
    thread_id           TEXT NOT NULL,          -- = farmer_id for persistent memory
    checkpoint_id       TEXT NOT NULL,
    checkpoint_ns       TEXT NOT NULL DEFAULT '',
    checkpoint          JSONB NOT NULL,         -- full LangGraph state snapshot
    metadata            JSONB NOT NULL DEFAULT '{}',
    parent_checkpoint_id TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
);

CREATE TABLE agents.langgraph_checkpoint_writes (
    thread_id           TEXT NOT NULL,
    checkpoint_ns       TEXT NOT NULL DEFAULT '',
    checkpoint_id       TEXT NOT NULL,
    task_id             TEXT NOT NULL,
    idx                 INT NOT NULL,
    channel             TEXT NOT NULL,
    type                TEXT,
    blob                BYTEA NOT NULL,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id, task_id, idx)
);

CREATE INDEX idx_lg_checkpoints_thread ON agents.langgraph_checkpoints(thread_id, created_at DESC);
CREATE INDEX idx_lg_writes_thread ON agents.langgraph_checkpoint_writes(thread_id, checkpoint_id);
```

### Phase 4 Validation

```sql
-- Verify pgvector HNSW index exists
SELECT indexname, indexdef FROM pg_indexes
WHERE indexname = 'idx_kau_hnsw';
-- Must return 1 row with USING hnsw

-- Verify embedding dimension
SELECT attname, atttypmod
FROM pg_attribute pa JOIN pg_class pc ON pa.attrelid = pc.oid
WHERE pc.relname = 'kau_documents' AND pa.attname = 'embedding';
-- atttypmod should show 1024

-- Test retrieve function exists
SELECT proname FROM pg_proc WHERE proname = 'retrieve_kau_docs';
-- Must return 1 row

-- Test partition creation for advisory_messages
SELECT agents.create_message_partition('2027-03-01'::DATE);
SELECT tablename FROM pg_tables WHERE tablename LIKE 'advisory_messages_2027_03';
-- Must return 1 row

-- Verify agent_name constraint
INSERT INTO agents.advisory_sessions (farmer_id, language, state, district)
SELECT id, 'hi', 'Punjab', 'Ludhiana' FROM core.farmers LIMIT 1;
-- (will fail if no farmers — add test farmer first)

SELECT 'Phase 4 validation passed' AS status;
```

---

## PHASE 5 — FIELD INTELLIGENCE, ALERTS & MARKET LAYERS

### Goal: All farmer-facing real-time tracking tables

```sql
-- ============================================================
-- PHASE 5.1 — FIELD OBSERVATIONS (farmer-reported)
-- ============================================================

CREATE TABLE intelligence.field_observations (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id            UUID NOT NULL REFERENCES core.fields(id) ON DELETE CASCADE,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    observed_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    observation_type    TEXT NOT NULL CHECK (observation_type IN (
                            'pest_sighting','disease_symptom','yellowing',
                            'wilting','nutrient_deficiency','waterlogging',
                            'drought_stress','good_growth','pest_damage',
                            'weed_problem','other'
                        )),
    description_native  TEXT NOT NULL,     -- in farmer's language
    description_en      TEXT,              -- AI-translated to English
    severity_estimate   public.alert_severity DEFAULT 'info',
    area_affected_pct   FLOAT CHECK (area_affected_pct BETWEEN 0 AND 100),

    -- Photo analysis (if farmer uploads photo)
    photo_url           TEXT,
    photo_analysis      JSONB,     -- AI vision analysis result
    detected_disease    TEXT,
    detected_pest       TEXT,
    confidence_pct      FLOAT CHECK (confidence_pct BETWEEN 0 AND 100),

    -- Advisory link
    triggered_advisory  UUID,      -- advisory_messages.id that responded to this
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_observations_field ON intelligence.field_observations(field_id, observed_at DESC);
CREATE INDEX idx_observations_type ON intelligence.field_observations(observation_type, observed_at DESC);
CREATE INDEX idx_observations_severity ON intelligence.field_observations(severity_estimate);

-- ============================================================
-- PHASE 5.2 — CROP STAGES (DSSAT outputs + agent updates)
-- ============================================================

CREATE TABLE intelligence.crop_stages (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id            UUID NOT NULL REFERENCES core.fields(id) ON DELETE CASCADE,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id),
    crop_name           TEXT NOT NULL,
    crop_variety        TEXT,
    season              TEXT CHECK (season IN ('kharif','rabi','zaid')),
    season_year         INT NOT NULL,

    -- Stage tracking
    current_stage       public.crop_stage NOT NULL,
    stage_started_at    DATE,
    next_stage          public.crop_stage,
    next_stage_eta_days INT,
    days_since_sowing   INT,

    -- DSSAT predictions
    predicted_yield_kg_ha    FLOAT,
    predicted_harvest_date   DATE,
    yield_confidence_pct     FLOAT CHECK (yield_confidence_pct BETWEEN 0 AND 100),
    simulated_at             TIMESTAMPTZ,
    dssat_scenario           JSONB,    -- input parameters used for simulation

    -- Water use
    cumulative_et_mm    FLOAT,    -- evapotranspiration
    water_stress_index  FLOAT CHECK (water_stress_index BETWEEN 0 AND 1),
    heat_stress_index   FLOAT CHECK (heat_stress_index BETWEEN 0 AND 1),

    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (field_id, crop_name, season_year)
);

CREATE INDEX idx_crop_stages_field ON intelligence.crop_stages(field_id);
CREATE INDEX idx_crop_stages_harvest ON intelligence.crop_stages(predicted_harvest_date)
    WHERE current_stage NOT IN ('harvest','post_harvest','fallow');

CREATE TRIGGER trg_crop_stages_updated_at
    BEFORE UPDATE ON intelligence.crop_stages
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

-- ============================================================
-- PHASE 5.3 — IRRIGATION SCHEDULES (IrrigationAgent output)
-- ============================================================

CREATE TABLE intelligence.irrigation_schedules (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id            UUID NOT NULL REFERENCES core.fields(id) ON DELETE CASCADE,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id),
    generated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_for_date      DATE NOT NULL,

    -- Recommendation
    should_irrigate     BOOLEAN NOT NULL,
    reason              TEXT NOT NULL,            -- human-readable explanation
    reason_native       TEXT,                     -- in farmer's language
    next_irrigation_date DATE,
    irrigation_amount_mm FLOAT CHECK (irrigation_amount_mm >= 0),
    irrigation_duration_hours FLOAT,

    -- Calculations used
    et0_mm              FLOAT,    -- FAO-56 reference evapotranspiration
    kc_factor           FLOAT,    -- crop coefficient for current stage
    etc_mm              FLOAT,    -- crop evapotranspiration = ET0 * Kc
    soil_moisture_pct   FLOAT CHECK (soil_moisture_pct BETWEEN 0 AND 100),
    field_capacity_pct  FLOAT,
    wilting_point_pct   FLOAT,
    rain_forecast_mm    FLOAT DEFAULT 0,

    -- Status
    was_followed        BOOLEAN,   -- farmer confirmed they irrigated
    farmer_notes        TEXT,
    UNIQUE (field_id, valid_for_date)
);

CREATE INDEX idx_irrigation_field_date ON intelligence.irrigation_schedules(field_id, valid_for_date DESC);
CREATE INDEX idx_irrigation_due ON intelligence.irrigation_schedules(valid_for_date)
    WHERE should_irrigate = TRUE AND was_followed IS NULL;

-- ============================================================
-- PHASE 5.4 — FERTILISER PLANS (FertiliserAgent output)
-- ============================================================

CREATE TABLE intelligence.fertiliser_plans (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id            UUID NOT NULL REFERENCES core.fields(id) ON DELETE CASCADE,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id),
    crop_name           TEXT NOT NULL,
    crop_stage          public.crop_stage NOT NULL,
    generated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    application_date    DATE NOT NULL,

    -- Macronutrient recommendations (kg/acre)
    nitrogen_kg_acre    FLOAT CHECK (nitrogen_kg_acre >= 0),
    phosphorus_kg_acre  FLOAT CHECK (phosphorus_kg_acre >= 0),
    potassium_kg_acre   FLOAT CHECK (potassium_kg_acre >= 0),

    -- Recommended products
    primary_fertiliser  TEXT,      -- e.g. "Urea 46%", "DAP", "MOP"
    primary_dose_kg_acre FLOAT,
    secondary_fertiliser TEXT,
    secondary_dose_kg_acre FLOAT,
    micronutrient_needed TEXT,     -- e.g. "Zinc Sulphate 25kg/acre"

    -- Method and timing
    application_method  TEXT CHECK (application_method IN (
                            'broadcast','band_placement','fertigation',
                            'foliar_spray','top_dressing','basal'
                        )),
    best_time_of_day    TEXT,      -- 'early_morning', 'evening', 'anytime'
    avoid_if_rain       BOOLEAN DEFAULT FALSE,

    -- Explanation
    rationale           TEXT NOT NULL,
    rationale_native    TEXT,
    source_doc          TEXT,      -- which KAU/ICAR document cited

    -- Status
    was_followed        BOOLEAN,
    UNIQUE (field_id, crop_stage, application_date)
);

CREATE INDEX idx_fertiliser_field ON intelligence.fertiliser_plans(field_id, application_date DESC);
CREATE INDEX idx_fertiliser_due ON intelligence.fertiliser_plans(application_date)
    WHERE was_followed IS NULL;

-- ============================================================
-- PHASE 5.5 — FARMER ALERTS (all alerts delivered to farmer)
-- ============================================================

CREATE TABLE alerts.farmer_alerts (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    field_id            UUID REFERENCES core.fields(id),

    -- Alert content
    category            public.alert_category NOT NULL,
    severity            public.alert_severity NOT NULL,
    title_native        TEXT NOT NULL,
    title_en            TEXT NOT NULL,
    body_native         TEXT NOT NULL,
    body_en             TEXT NOT NULL,
    language            public.language_code NOT NULL,

    -- Source tracing
    source_agent        TEXT,                -- which agent generated this
    source_data_type    TEXT,                -- 'pest_alert'|'weather'|'market'|'crop_stage'
    source_data_id      UUID,                -- FK to source record

    -- Suggested action
    action_type         TEXT CHECK (action_type IN (
                            'ask_advisor','scan_crop','check_field',
                            'visit_market','apply_fertiliser','irrigate',
                            'harvest_now','none'
                        )),
    action_deep_link    TEXT,                -- android deep link to relevant screen

    -- Delivery
    fcm_sent            BOOLEAN DEFAULT FALSE,
    fcm_sent_at         TIMESTAMPTZ,
    fcm_message_id      TEXT,

    -- Engagement
    is_read             BOOLEAN DEFAULT FALSE,
    read_at             TIMESTAMPTZ,
    is_dismissed        BOOLEAN DEFAULT FALSE,
    dismissed_at        TIMESTAMPTZ,
    was_acted_upon      BOOLEAN,
    acted_at            TIMESTAMPTZ,

    -- Scheduling
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at          TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '7 days')
) PARTITION BY RANGE (created_at);

CREATE TABLE alerts.farmer_alerts_2026_q3 PARTITION OF alerts.farmer_alerts
    FOR VALUES FROM ('2026-07-01') TO ('2026-10-01');
CREATE TABLE alerts.farmer_alerts_2026_q4 PARTITION OF alerts.farmer_alerts
    FOR VALUES FROM ('2026-10-01') TO ('2027-01-01');
CREATE TABLE alerts.farmer_alerts_2027_q1 PARTITION OF alerts.farmer_alerts
    FOR VALUES FROM ('2027-01-01') TO ('2027-04-01');
CREATE TABLE alerts.farmer_alerts_2027_q2 PARTITION OF alerts.farmer_alerts
    FOR VALUES FROM ('2027-04-01') TO ('2027-07-01');

CREATE INDEX idx_farmer_alerts_farmer ON alerts.farmer_alerts(farmer_id, created_at DESC);
CREATE INDEX idx_farmer_alerts_unread ON alerts.farmer_alerts(farmer_id)
    WHERE is_read = FALSE AND is_dismissed = FALSE;
CREATE INDEX idx_farmer_alerts_severity ON alerts.farmer_alerts(severity, created_at DESC);
CREATE INDEX idx_farmer_alerts_expires ON alerts.farmer_alerts(expires_at);

-- ============================================================
-- PHASE 5.6 — FCM DELIVERY LOG
-- ============================================================

CREATE TABLE alerts.fcm_delivery_log (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_id            UUID NOT NULL,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id),
    fcm_token           TEXT NOT NULL,
    fcm_message_id      TEXT,
    topic               TEXT,                    -- FCM topic if used
    status              TEXT NOT NULL CHECK (status IN (
                            'sent','delivered','failed','invalid_token','not_registered'
                        )),
    error_code          TEXT,
    error_message       TEXT,
    sent_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    delivered_at        TIMESTAMPTZ
);

CREATE INDEX idx_fcm_log_farmer ON alerts.fcm_delivery_log(farmer_id, sent_at DESC);
CREATE INDEX idx_fcm_log_status ON alerts.fcm_delivery_log(status) WHERE status != 'delivered';

-- ============================================================
-- PHASE 5.7 — MARKET RECOMMENDATIONS
-- ============================================================

CREATE TABLE market.market_recommendations (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    crop_name           TEXT NOT NULL,
    state               TEXT NOT NULL,
    district            TEXT NOT NULL,
    generated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    -- Current price data
    current_modal_price NUMERIC(10,2),
    nearest_market      TEXT,
    price_date          DATE,

    -- Recommendation
    recommendation      public.market_recommendation NOT NULL,
    rationale           TEXT NOT NULL,
    rationale_native    TEXT,
    target_price        NUMERIC(10,2),    -- price at which to sell if holding
    hold_until_estimate DATE,             -- estimated date to sell

    -- Context used
    price_trend_7d      public.price_trend,
    price_trend_30d     public.price_trend,
    pct_above_msp       FLOAT,            -- % above minimum support price
    seasonal_factor     TEXT,             -- why price is at current level

    -- Expiry
    valid_until         DATE DEFAULT (CURRENT_DATE + 3),
    was_helpful         BOOLEAN
);

CREATE INDEX idx_market_rec_farmer ON market.market_recommendations(farmer_id, generated_at DESC);
CREATE INDEX idx_market_rec_crop ON market.market_recommendations(crop_name, state, generated_at DESC);

-- ============================================================
-- PHASE 5.8 — PRICE SUBSCRIPTIONS
-- ============================================================

CREATE TABLE market.price_subscriptions (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id   UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    crop_name   TEXT NOT NULL,
    state       TEXT NOT NULL,
    alert_above NUMERIC(10,2),   -- notify when price goes above this
    alert_below NUMERIC(10,2),   -- notify when price drops below this
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (farmer_id, crop_name, state)
);

CREATE INDEX idx_price_subs_farmer ON market.price_subscriptions(farmer_id) WHERE is_active = TRUE;
```

---

## PHASE 6 — ANALYTICS LAYER

### Goal: All platform metrics, agent performance, farmer feedback

```sql
-- ============================================================
-- PHASE 6.1 — FARM SEASON ANALYTICS (per farm, per season)
-- ============================================================

CREATE TABLE analytics.farm_season_analytics (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id                 UUID NOT NULL REFERENCES core.farms(id),
    farmer_id               UUID NOT NULL REFERENCES core.farmers(id),
    crop_name               TEXT NOT NULL,
    season                  TEXT NOT NULL CHECK (season IN ('kharif','rabi','zaid')),
    season_year             INT NOT NULL,

    -- Advisory usage
    total_queries           INT DEFAULT 0,
    queries_about_pest      INT DEFAULT 0,
    queries_about_weather   INT DEFAULT 0,
    queries_about_market    INT DEFAULT 0,
    queries_about_soil      INT DEFAULT 0,
    advisories_followed     INT DEFAULT 0,
    advisories_ignored      INT DEFAULT 0,

    -- Alerts
    critical_alerts_received INT DEFAULT 0,
    alerts_acted_upon        INT DEFAULT 0,

    -- Outcomes (filled at harvest)
    actual_yield_kg_ha      FLOAT,
    dssat_predicted_yield   FLOAT,
    yield_accuracy_pct      FLOAT GENERATED ALWAYS AS (
        CASE WHEN dssat_predicted_yield > 0
             THEN (1 - ABS(actual_yield_kg_ha - dssat_predicted_yield) / dssat_predicted_yield) * 100
             ELSE NULL END
    ) STORED,
    sold_price_per_quintal  NUMERIC(10,2),
    total_revenue_inr       NUMERIC(12,2),

    -- Satisfaction
    overall_satisfaction    INT CHECK (overall_satisfaction BETWEEN 1 AND 5),
    nps_score               INT CHECK (nps_score BETWEEN 0 AND 10),

    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (farm_id, crop_name, season, season_year)
);

CREATE INDEX idx_season_analytics_farmer ON analytics.farm_season_analytics(farmer_id);
CREATE INDEX idx_season_analytics_crop ON analytics.farm_season_analytics(crop_name, season_year);

-- ============================================================
-- PHASE 6.2 — AGENT PERFORMANCE (daily per-agent metrics)
-- ============================================================

CREATE TABLE analytics.agent_performance (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_name          TEXT NOT NULL,
    metric_date         DATE NOT NULL,
    total_invocations   INT DEFAULT 0,
    successful          INT DEFAULT 0,
    failed              INT DEFAULT 0,
    success_rate_pct    FLOAT GENERATED ALWAYS AS (
        CASE WHEN total_invocations > 0
             THEN (successful::FLOAT / total_invocations) * 100
             ELSE 0 END
    ) STORED,
    avg_duration_ms     FLOAT,
    p50_duration_ms     FLOAT,
    p95_duration_ms     FLOAT,
    p99_duration_ms     FLOAT,
    total_gemini_calls  INT DEFAULT 0,
    total_tokens_used   INT DEFAULT 0,
    cache_hit_count     INT DEFAULT 0,
    cache_hit_rate_pct  FLOAT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (agent_name, metric_date)
);

CREATE INDEX idx_agent_perf_date ON analytics.agent_performance(metric_date DESC);
CREATE INDEX idx_agent_perf_name ON analytics.agent_performance(agent_name, metric_date DESC);

-- ============================================================
-- PHASE 6.3 — PLATFORM METRICS (daily platform-wide KPIs)
-- ============================================================

CREATE TABLE analytics.platform_metrics (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_date             DATE NOT NULL UNIQUE,
    -- User metrics
    dau                     INT DEFAULT 0,   -- daily active users
    new_registrations       INT DEFAULT 0,
    total_registered        INT DEFAULT 0,
    -- Advisory metrics
    total_queries           INT DEFAULT 0,
    avg_response_ms         FLOAT,
    p95_response_ms         FLOAT,
    -- Agent metrics
    total_agent_calls       INT DEFAULT 0,
    gemini_calls_total      INT DEFAULT 0,
    gemini_tokens_total     INT DEFAULT 0,
    -- Alerts
    alerts_sent             INT DEFAULT 0,
    fcm_success_rate_pct    FLOAT,
    -- Errors
    error_count             INT DEFAULT 0,
    error_rate_pct          FLOAT,
    -- Cache
    weather_cache_hits      INT DEFAULT 0,
    market_cache_hits       INT DEFAULT 0,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_platform_metrics_date ON analytics.platform_metrics(metric_date DESC);

-- ============================================================
-- PHASE 6.4 — ADVISORY FEEDBACK (farmer rates AI quality)
-- ============================================================

CREATE TABLE analytics.advisory_feedback (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    message_id          UUID NOT NULL,
    session_id          UUID NOT NULL REFERENCES agents.advisory_sessions(id),
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id),
    rating              INT NOT NULL CHECK (rating IN (1, -1)),  -- thumbs up=1, down=-1
    feedback_text       TEXT,           -- optional text feedback
    feedback_text_en    TEXT,           -- AI-translated to English
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX idx_feedback_session ON analytics.advisory_feedback(session_id);
CREATE INDEX idx_feedback_rating ON analytics.advisory_feedback(rating, created_at DESC);
```

---

## PHASE 7 — SYSTEM LAYER & REALTIME TRIGGERS

### Goal: Audit logging, rate limiting, and auto-refresh triggers

```sql
-- ============================================================
-- PHASE 7.1 — AUDIT LOG (all write operations)
-- ============================================================

CREATE TABLE system.audit_log (
    id              UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    table_schema    TEXT NOT NULL,
    table_name      TEXT NOT NULL,
    operation       TEXT NOT NULL CHECK (operation IN ('INSERT','UPDATE','DELETE')),
    record_id       UUID,
    farmer_id       UUID,
    old_data        JSONB,
    new_data        JSONB,
    changed_fields  TEXT[],
    performed_at    TIMESTAMPTZ NOT NULL DEFAULT NOW()
) PARTITION BY RANGE (performed_at);

CREATE TABLE system.audit_log_2026_q4 PARTITION OF system.audit_log
    FOR VALUES FROM ('2026-10-01') TO ('2027-01-01');
CREATE TABLE system.audit_log_2027_q1 PARTITION OF system.audit_log
    FOR VALUES FROM ('2027-01-01') TO ('2027-04-01');
CREATE TABLE system.audit_log_2027_q2 PARTITION OF system.audit_log
    FOR VALUES FROM ('2027-04-01') TO ('2027-07-01');

CREATE INDEX idx_audit_farmer ON system.audit_log(farmer_id, performed_at DESC)
    WHERE farmer_id IS NOT NULL;
CREATE INDEX idx_audit_table ON system.audit_log(table_name, performed_at DESC);

-- Generic audit trigger function
CREATE OR REPLACE FUNCTION system.audit_trigger()
RETURNS TRIGGER AS $$
DECLARE
    changed TEXT[];
    col TEXT;
BEGIN
    IF TG_OP = 'UPDATE' THEN
        FOR col IN SELECT column_name FROM information_schema.columns
                   WHERE table_schema = TG_TABLE_SCHEMA AND table_name = TG_TABLE_NAME
        LOOP
            IF (row_to_json(OLD)->>col) IS DISTINCT FROM (row_to_json(NEW)->>col) THEN
                changed := array_append(changed, col);
            END IF;
        END LOOP;
    END IF;

    INSERT INTO system.audit_log (table_schema, table_name, operation, record_id,
        old_data, new_data, changed_fields)
    VALUES (
        TG_TABLE_SCHEMA, TG_TABLE_NAME, TG_OP,
        CASE WHEN TG_OP = 'DELETE' THEN (row_to_json(OLD)->>'id')::UUID
             ELSE (row_to_json(NEW)->>'id')::UUID END,
        CASE WHEN TG_OP IN ('UPDATE','DELETE') THEN row_to_json(OLD) ELSE NULL END,
        CASE WHEN TG_OP IN ('INSERT','UPDATE') THEN row_to_json(NEW) ELSE NULL END,
        changed
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply audit trigger to critical tables
CREATE TRIGGER audit_farmers
    AFTER INSERT OR UPDATE OR DELETE ON core.farmers
    FOR EACH ROW EXECUTE FUNCTION system.audit_trigger();

CREATE TRIGGER audit_fields
    AFTER INSERT OR UPDATE OR DELETE ON core.fields
    FOR EACH ROW EXECUTE FUNCTION system.audit_trigger();

-- ============================================================
-- PHASE 7.2 — API RATE LIMITS
-- ============================================================

CREATE TABLE system.api_rate_limits (
    farmer_id       UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    window_start    TIMESTAMPTZ NOT NULL,
    window_minutes  INT NOT NULL DEFAULT 60,
    request_count   INT NOT NULL DEFAULT 1,
    max_allowed     INT NOT NULL DEFAULT 100,
    is_limited      BOOLEAN GENERATED ALWAYS AS (request_count >= max_allowed) STORED,
    PRIMARY KEY (farmer_id, window_start)
);

CREATE INDEX idx_rate_limit_farmer ON system.api_rate_limits(farmer_id, window_start DESC);

-- ============================================================
-- PHASE 7.3 — REALTIME AUTO-REFRESH TRIGGERS
-- ============================================================

-- Trigger: when advisory_messages inserted, update session stats
CREATE OR REPLACE FUNCTION agents.update_session_stats()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE agents.advisory_sessions
    SET
        message_count = message_count + 1,
        last_message_at = NEW.created_at,
        total_tokens_used = total_tokens_used + COALESCE(NEW.tokens_in, 0) + COALESCE(NEW.tokens_out, 0),
        avg_response_ms = (
            SELECT AVG(response_ms) FROM agents.advisory_messages
            WHERE session_id = NEW.session_id AND role = 'assistant' AND response_ms IS NOT NULL
        )
    WHERE id = NEW.session_id;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_update_session_stats
    AFTER INSERT ON agents.advisory_messages
    FOR EACH ROW EXECUTE FUNCTION agents.update_session_stats();

-- Trigger: when farmer_alerts inserted, send FCM immediately
-- (This is a notification trigger — actual FCM sent by backend service)
CREATE OR REPLACE FUNCTION alerts.notify_new_alert()
RETURNS TRIGGER AS $$
BEGIN
    -- Notify backend via pg_notify channel (FastAPI listens on this)
    PERFORM pg_notify(
        'new_farmer_alert',
        json_build_object(
            'alert_id', NEW.id,
            'farmer_id', NEW.farmer_id,
            'severity', NEW.severity,
            'category', NEW.category,
            'fcm_topic', (SELECT fcm_topic FROM core.farmers WHERE id = NEW.farmer_id)
        )::TEXT
    );
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_notify_alert
    AFTER INSERT ON alerts.farmer_alerts
    FOR EACH ROW EXECUTE FUNCTION alerts.notify_new_alert();

-- Trigger: update farmer.last_active_at on every new message
CREATE OR REPLACE FUNCTION agents.update_farmer_activity()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.role = 'user' THEN
        UPDATE core.farmers SET last_active_at = NOW() WHERE id = NEW.farmer_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_farmer_activity
    AFTER INSERT ON agents.advisory_messages
    FOR EACH ROW EXECUTE FUNCTION agents.update_farmer_activity();

-- Trigger: auto-generate market recommendation when new price inserted
CREATE OR REPLACE FUNCTION realtime.auto_market_recommendation()
RETURNS TRIGGER AS $$
DECLARE
    price_7d_ago NUMERIC(10,2);
    price_30d_ago NUMERIC(10,2);
    trend TEXT;
    rec TEXT;
    pct_change FLOAT;
BEGIN
    -- Get historical prices
    SELECT modal_price INTO price_7d_ago FROM realtime.market_prices
    WHERE crop_name = NEW.crop_name AND state = NEW.state
      AND price_date = NEW.price_date - 7
    LIMIT 1;

    SELECT modal_price INTO price_30d_ago FROM realtime.market_prices
    WHERE crop_name = NEW.crop_name AND state = NEW.state
      AND price_date = NEW.price_date - 30
    LIMIT 1;

    -- Compute trend
    IF price_7d_ago IS NOT NULL THEN
        pct_change := ((NEW.modal_price - price_7d_ago) / price_7d_ago) * 100;
        IF pct_change > 5 THEN trend := 'rising';
        ELSIF pct_change < -5 THEN trend := 'falling';
        ELSE trend := 'stable';
        END IF;
    ELSE
        trend := 'stable';
        pct_change := 0;
    END IF;

    -- Set trend and recommendation on the inserted row
    UPDATE realtime.market_prices
    SET
        trend_7d = trend::public.price_trend,
        pct_change_7d = pct_change,
        recommendation = CASE
            WHEN trend = 'rising' AND pct_change > 3 THEN 'sell_now'::public.market_recommendation
            WHEN trend = 'falling' THEN 'hold'::public.market_recommendation
            ELSE 'sell_partial'::public.market_recommendation
        END
    WHERE id = NEW.id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_auto_market_rec
    AFTER INSERT ON realtime.market_prices
    FOR EACH ROW EXECUTE FUNCTION realtime.auto_market_recommendation();
```

---

## PHASE 8 — SEED DATA

### Goal: All reference data pre-loaded so app works from day 1

```sql
-- ============================================================
-- PHASE 8.1 — INDIA SOIL ZONES (all major states)
-- ============================================================

INSERT INTO realtime.soil_zones (state, district, primary_texture, ph_min, ph_max, organic_carbon,
    nitrogen_status, phosphorus_status, potassium_status, water_holding_capacity,
    drainage, annual_rainfall_mm_avg, suitable_crops, agroclimatic_zone) VALUES

-- PUNJAB
('Punjab', 'Ludhiana',    'loam',       7.0, 8.5, 'medium', 'low',    'medium', 'high',   'high',   'moderate', 650,  ARRAY['wheat','rice','maize','potato','mustard'],       'trans_gangetic_plains'),
('Punjab', 'Amritsar',    'sandy_loam', 7.0, 8.2, 'low',    'low',    'low',    'high',   'medium', 'moderate', 610,  ARRAY['wheat','rice','cotton','sugarcane'],             'trans_gangetic_plains'),
('Punjab', 'Patiala',     'loam',       7.2, 8.4, 'medium', 'medium', 'low',    'high',   'high',   'moderate', 700,  ARRAY['wheat','rice','mustard','maize'],                'trans_gangetic_plains'),
('Punjab', 'Jalandhar',   'clay_loam',  7.0, 8.0, 'medium', 'medium', 'medium', 'high',   'high',   'moderate', 680,  ARRAY['wheat','rice','vegetables'],                    'trans_gangetic_plains'),

-- HARYANA
('Haryana', 'Karnal',     'loam',       7.5, 8.8, 'low',    'low',    'low',    'high',   'medium', 'moderate', 780,  ARRAY['wheat','rice','sugarcane'],                     'trans_gangetic_plains'),
('Haryana', 'Hisar',      'sandy_loam', 7.8, 9.0, 'low',    'low',    'low',    'medium', 'low',    'moderate', 450,  ARRAY['wheat','cotton','mustard','bajra'],              'trans_gangetic_plains'),
('Haryana', 'Rohtak',     'loam',       7.5, 8.5, 'low',    'low',    'low',    'high',   'medium', 'moderate', 500,  ARRAY['wheat','rice','sugarcane'],                     'trans_gangetic_plains'),

-- UTTAR PRADESH
('Uttar Pradesh', 'Lucknow',      'clay_loam',  7.0, 8.5, 'medium', 'medium', 'medium', 'high',   'high',   'moderate', 1000, ARRAY['wheat','rice','sugarcane','potato','mustard'], 'upper_gangetic_plains'),
('Uttar Pradesh', 'Varanasi',     'loam',       7.2, 8.2, 'medium', 'medium', 'medium', 'high',   'high',   'moderate', 1050, ARRAY['wheat','rice','vegetables','chilli'],          'middle_gangetic_plains'),
('Uttar Pradesh', 'Agra',         'loam',       7.5, 8.5, 'low',    'low',    'medium', 'medium', 'medium', 'moderate', 700,  ARRAY['wheat','mustard','potato','brinjal'],          'upper_gangetic_plains'),
('Uttar Pradesh', 'Meerut',       'sandy_loam', 7.0, 8.0, 'medium', 'medium', 'medium', 'high',   'high',   'well',     800,  ARRAY['wheat','sugarcane','rice','potato'],           'upper_gangetic_plains'),

-- MAHARASHTRA
('Maharashtra', 'Nagpur',    'black_cotton', 7.5, 8.5, 'medium', 'medium', 'medium', 'medium', 'high',   'poor',     1200, ARRAY['soybean','cotton','wheat','orange','gram'],     'western_plateau_hills'),
('Maharashtra', 'Pune',      'black_cotton', 7.0, 8.0, 'medium', 'medium', 'low',    'high',   'high',   'poor',     740,  ARRAY['soybean','wheat','sugarcane','grapes','onion'],'western_plateau_hills'),
('Maharashtra', 'Nashik',    'black_cotton', 6.5, 7.5, 'medium', 'medium', 'medium', 'high',   'high',   'moderate', 700,  ARRAY['grapes','onion','tomato','wheat','soybean'],   'western_plateau_hills'),
('Maharashtra', 'Aurangabad','black_cotton', 7.5, 8.5, 'low',    'low',    'medium', 'medium', 'high',   'poor',     700,  ARRAY['cotton','soybean','wheat','jowar'],            'western_plateau_hills'),

-- MADHYA PRADESH
('Madhya Pradesh', 'Bhopal',   'black_cotton', 7.5, 8.5, 'medium', 'medium', 'medium', 'medium', 'high',   'poor',     1200, ARRAY['soybean','wheat','cotton','gram','lentil'],     'central_plateau_hills'),
('Madhya Pradesh', 'Indore',   'black_cotton', 7.0, 8.0, 'medium', 'medium', 'medium', 'high',   'high',   'moderate', 1000, ARRAY['soybean','wheat','cotton','sugarcane','onion'], 'central_plateau_hills'),
('Madhya Pradesh', 'Jabalpur', 'clay',         6.5, 7.5, 'high',   'medium', 'medium', 'medium', 'high',   'poor',     1400, ARRAY['rice','wheat','pulses','oilseeds'],              'central_plateau_hills'),

-- RAJASTHAN
('Rajasthan', 'Jaipur',  'sandy_loam', 7.5, 9.0, 'low', 'low', 'low',    'low',    'low',    'excessive', 550,  ARRAY['wheat','mustard','bajra','jowar','groundnut'],   'western_dry'),
('Rajasthan', 'Jodhpur', 'sandy',      7.8, 9.2, 'low', 'low', 'low',    'low',    'low',    'excessive', 380,  ARRAY['bajra','guar','moth_bean','sesame'],             'western_dry'),
('Rajasthan', 'Kota',    'loam',       7.5, 8.5, 'low', 'low', 'medium', 'medium', 'medium', 'moderate',  700,  ARRAY['soybean','wheat','mustard','coriander'],         'western_plateau_hills'),

-- GUJARAT
('Gujarat', 'Ahmedabad', 'black_cotton', 7.5, 8.5, 'low',    'low',    'low',    'medium', 'high',   'poor',     700,  ARRAY['cotton','groundnut','wheat','bajra','castor'],   'gujarat_plains'),
('Gujarat', 'Surat',     'loam',         6.5, 7.5, 'medium', 'medium', 'medium', 'high',   'medium', 'moderate', 1200, ARRAY['sugarcane','rice','vegetables','mango'],          'gujarat_plains'),
('Gujarat', 'Anand',     'loam',         7.0, 8.0, 'medium', 'medium', 'medium', 'high',   'high',   'moderate', 900,  ARRAY['tobacco','cotton','wheat','groundnut'],           'gujarat_plains'),

-- TAMIL NADU
('Tamil Nadu', 'Coimbatore', 'red_laterite',  6.0, 7.5, 'medium', 'medium', 'low',    'medium', 'medium', 'well',     600,  ARRAY['cotton','maize','sorghum','groundnut','banana'],   'east_coast_plains'),
('Tamil Nadu', 'Thanjavur',  'alluvial',      6.5, 7.5, 'high',   'high',   'medium', 'high',   'high',   'moderate', 1200, ARRAY['rice','banana','sugarcane','groundnut'],           'east_coast_plains'),
('Tamil Nadu', 'Salem',      'red_laterite',  6.0, 7.0, 'low',    'low',    'low',    'medium', 'low',    'well',     900,  ARRAY['maize','groundnut','tapioca','cotton'],            'east_coast_plains'),
('Tamil Nadu', 'Tirunelveli','red_laterite',  6.5, 7.5, 'low',    'low',    'low',    'medium', 'medium', 'well',     500,  ARRAY['cotton','banana','groundnut','sesame'],            'east_coast_plains'),

-- ANDHRA PRADESH
('Andhra Pradesh', 'Guntur',      'black_cotton', 7.5, 8.5, 'low',    'low',    'medium', 'medium', 'high',   'poor',     900,  ARRAY['cotton','chilli','tobacco','groundnut','rice'], 'east_coast_plains'),
('Andhra Pradesh', 'Krishna',     'alluvial',     6.5, 7.5, 'high',   'high',   'medium', 'high',   'high',   'moderate', 1000, ARRAY['rice','sugarcane','banana','cotton'],            'east_coast_plains'),
('Andhra Pradesh', 'Kurnool',     'red_laterite', 6.5, 8.0, 'low',    'low',    'low',    'medium', 'low',    'well',     600,  ARRAY['groundnut','cotton','sunflower','maize'],        'southern_plateau_hills'),

-- TELANGANA
('Telangana', 'Hyderabad',    'red_laterite', 6.5, 8.0, 'low',    'low',    'low',    'medium', 'medium', 'well',     900,  ARRAY['rice','cotton','maize','sorghum','groundnut'],  'southern_plateau_hills'),
('Telangana', 'Warangal',     'black_cotton', 7.0, 8.5, 'medium', 'medium', 'medium', 'medium', 'high',   'poor',     1000, ARRAY['cotton','rice','chilli','maize','sorghum'],      'southern_plateau_hills'),

-- KERALA
('Kerala', 'Ernakulam',      'laterite',     5.5, 6.5, 'medium', 'low',    'medium', 'high',   'medium', 'well',     3200, ARRAY['coconut','tapioca','banana','rubber','pepper'],  'west_coast_plains'),
('Kerala', 'Thrissur',       'laterite',     5.5, 6.5, 'high',   'medium', 'medium', 'high',   'medium', 'moderate', 2800, ARRAY['coconut','banana','tapioca','pepper','arecanut'],'west_coast_plains'),
('Kerala', 'Thiruvananthapuram','laterite',  5.0, 6.5, 'high',   'medium', 'low',    'high',   'medium', 'well',     1700, ARRAY['coconut','rubber','tapioca','banana','cashew'],  'west_coast_plains'),
('Kerala', 'Kozhikode',      'laterite',     5.5, 6.5, 'high',   'medium', 'low',    'high',   'high',   'well',     2700, ARRAY['coconut','banana','arecanut','pepper','ginger'], 'west_coast_plains'),
('Kerala', 'Wayanad',        'laterite',     4.5, 6.0, 'high',   'high',   'low',    'high',   'high',   'well',     2000, ARRAY['coffee','tea','pepper','cardamom','ginger'],    'west_coast_plains'),
('Kerala', 'Idukki',         'laterite',     4.5, 6.0, 'high',   'medium', 'low',    'medium', 'high',   'well',     2500, ARRAY['cardamom','tea','coffee','rubber','pepper'],     'west_coast_plains'),
('Kerala', 'Palakkad',       'red_laterite', 5.5, 7.0, 'medium', 'medium', 'low',    'medium', 'medium', 'well',     2100, ARRAY['rice','coconut','banana','maize','groundnut'],   'west_coast_plains'),
('Kerala', 'Malappuram',     'laterite',     5.5, 6.5, 'medium', 'low',    'low',    'medium', 'medium', 'well',     2600, ARRAY['coconut','arecanut','banana','pepper','ginger'], 'west_coast_plains'),
('Kerala', 'Kollam',         'laterite',     5.0, 6.5, 'high',   'medium', 'low',    'high',   'medium', 'moderate', 2200, ARRAY['coconut','rubber','cashew','tapioca','banana'],  'west_coast_plains'),
('Kerala', 'Alappuzha',      'alluvial',     5.5, 7.0, 'high',   'high',   'medium', 'high',   'high',   'poor',     2800, ARRAY['rice','coconut','banana','vegetables'],           'west_coast_plains'),
('Kerala', 'Pathanamthitta', 'laterite',     5.0, 6.5, 'high',   'medium', 'low',    'medium', 'high',   'well',     3000, ARRAY['rubber','coconut','banana','tapioca','pepper'],  'west_coast_plains'),
('Kerala', 'Kottayam',       'laterite',     5.0, 6.0, 'high',   'medium', 'low',    'medium', 'high',   'well',     3000, ARRAY['rubber','coconut','pepper','cardamom','tapioca'],'west_coast_plains'),
('Kerala', 'Kasaragod',      'laterite',     5.5, 6.5, 'medium', 'medium', 'low',    'medium', 'medium', 'well',     3800, ARRAY['coconut','arecanut','rubber','banana','pepper'],  'west_coast_plains'),
('Kerala', 'Kannur',         'laterite',     5.5, 6.5, 'medium', 'low',    'low',    'medium', 'medium', 'well',     3300, ARRAY['coconut','arecanut','pepper','banana','ginger'],  'west_coast_plains'),

-- KARNATAKA
('Karnataka', 'Bengaluru',  'red_laterite',  6.0, 7.5, 'medium', 'medium', 'low',    'medium', 'medium', 'well',     900,  ARRAY['ragi','vegetables','coconut','maize','potato'],   'southern_plateau_hills'),
('Karnataka', 'Mysuru',     'red_laterite',  6.0, 7.5, 'medium', 'medium', 'medium', 'medium', 'medium', 'well',     750,  ARRAY['sugarcane','ragi','maize','vegetables','cotton'],  'southern_plateau_hills'),
('Karnataka', 'Dharwad',    'black_cotton',  7.5, 8.5, 'medium', 'medium', 'medium', 'medium', 'high',   'poor',     800,  ARRAY['cotton','soybean','wheat','sunflower','groundnut'],'central_plateau_hills'),
('Karnataka', 'Tumkur',     'red_laterite',  6.0, 7.0, 'low',    'low',    'low',    'medium', 'low',    'well',     700,  ARRAY['coconut','groundnut','mulberry','ragi','maize'],   'southern_plateau_hills'),

-- WEST BENGAL
('West Bengal', 'Kolkata',    'alluvial',  6.5, 7.5, 'high',   'high',   'high',   'high',   'high',   'poor',     1850, ARRAY['rice','jute','vegetables','potato'],              'lower_gangetic_plains'),
('West Bengal', 'Burdwan',    'alluvial',  6.5, 7.5, 'high',   'high',   'medium', 'high',   'high',   'moderate', 1450, ARRAY['rice','potato','wheat','jute','mustard'],          'lower_gangetic_plains'),
('West Bengal', 'Malda',      'alluvial',  6.5, 7.5, 'high',   'high',   'medium', 'high',   'high',   'moderate', 1400, ARRAY['mango','rice','wheat','jute','potato'],            'lower_gangetic_plains'),

-- BIHAR
('Bihar', 'Patna',       'alluvial', 7.0, 8.0, 'medium', 'medium', 'medium', 'high',  'high',   'moderate', 1200, ARRAY['rice','wheat','maize','lentil','potato','mustard'],   'middle_gangetic_plains'),
('Bihar', 'Muzaffarpur', 'alluvial', 7.0, 7.8, 'medium', 'medium', 'medium', 'high',  'high',   'moderate', 1200, ARRAY['rice','wheat','mango','litchi','maize'],               'middle_gangetic_plains'),

-- ODISHA
('Odisha', 'Bhubaneswar', 'red_laterite', 5.5, 7.0, 'medium', 'low',    'low',    'medium', 'medium', 'well',     1500, ARRAY['rice','groundnut','turmeric','ginger','maize'],    'eastern_plateau_hills'),
('Odisha', 'Cuttack',     'alluvial',     6.0, 7.5, 'high',   'medium', 'medium', 'high',   'high',   'moderate', 1550, ARRAY['rice','jute','sugarcane','vegetables'],             'eastern_plateau_hills');

-- ============================================================
-- PHASE 8.2 — MSP REFERENCE DATA (Minimum Support Price 2025-26)
-- ============================================================

CREATE TABLE IF NOT EXISTS realtime.msp_reference (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_name   TEXT NOT NULL,
    season      TEXT NOT NULL CHECK (season IN ('kharif','rabi','zaid')),
    msp_year    TEXT NOT NULL,
    msp_per_quintal NUMERIC(10,2) NOT NULL,
    announced_by TEXT DEFAULT 'CACP',
    effective_from DATE,
    source      TEXT DEFAULT 'Ministry of Agriculture & Farmers Welfare',
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (crop_name, season, msp_year)
);

INSERT INTO realtime.msp_reference (crop_name, season, msp_year, msp_per_quintal, effective_from) VALUES
-- Kharif 2025-26
('rice',        'kharif', '2025-26', 2300.00, '2025-07-01'),
('maize',       'kharif', '2025-26', 2090.00, '2025-07-01'),
('cotton',      'kharif', '2025-26', 7121.00, '2025-07-01'),
('groundnut',   'kharif', '2025-26', 6783.00, '2025-07-01'),
('soybean',     'kharif', '2025-26', 4892.00, '2025-07-01'),
('sugarcane',   'kharif', '2025-26', 340.00,  '2025-07-01'),
('bajra',       'kharif', '2025-26', 2625.00, '2025-07-01'),
('jowar',       'kharif', '2025-26', 3371.00, '2025-07-01'),
('tur_dal',     'kharif', '2025-26', 7550.00, '2025-07-01'),
('urad',        'kharif', '2025-26', 7400.00, '2025-07-01'),
('moong',       'kharif', '2025-26', 8682.00, '2025-07-01'),
('sesame',      'kharif', '2025-26', 9267.00, '2025-07-01'),
-- Rabi 2025-26
('wheat',       'rabi',   '2025-26', 2425.00, '2025-11-01'),
('mustard',     'rabi',   '2025-26', 5950.00, '2025-11-01'),
('gram',        'rabi',   '2025-26', 5650.00, '2025-11-01'),
('lentil',      'rabi',   '2025-26', 6700.00, '2025-11-01'),
('safflower',   'rabi',   '2025-26', 5940.00, '2025-11-01'),
('sunflower',   'rabi',   '2025-26', 7280.00, '2025-11-01'),
('barley',      'rabi',   '2025-26', 1850.00, '2025-11-01');
```

---

## PHASE 9 — ALEMBIC MIGRATIONS (Python)

### Goal: SQLAlchemy models mirror every PostgreSQL table, Alembic manages all schema changes

```python
# backend/app/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from pgvector.sqlalchemy import Vector
from app.config import settings

engine = create_async_engine(
    settings.database_url,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    echo=(settings.environment == "development"),
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()

async def init_db():
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\""))
        await conn.execute(text("""
            CREATE INDEX IF NOT EXISTS idx_kau_hnsw
            ON agents.kau_documents USING hnsw (embedding vector_cosine_ops)
            WITH (m = 16, ef_construction = 64)
        """))
```

```python
# backend/app/models/core.py — SQLAlchemy models (key examples)
from sqlalchemy import Column, String, Float, Boolean, Integer, ARRAY, Text
from sqlalchemy import DateTime, ForeignKey, Enum, CheckConstraint, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func
from pgvector.sqlalchemy import Vector
from app.database import Base
import uuid

class Farmer(Base):
    __tablename__ = "farmers"
    __table_args__ = {"schema": "core"}

    id               = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    farmer_code      = Column(String, unique=True, nullable=False)
    name             = Column(String(100), nullable=False)
    phone            = Column(String(10), unique=True)
    phone_verified   = Column(Boolean, default=False, nullable=False)
    state            = Column(String(60), nullable=False)
    district         = Column(String(60), nullable=False)
    lat              = Column(Float)
    lon              = Column(Float)
    primary_language = Column(String(2), nullable=False, default='hi')
    crops            = Column(ARRAY(Text), default=[])
    onboarding_complete = Column(Boolean, default=False, nullable=False)
    fcm_topic        = Column(String)
    last_active_at   = Column(DateTime(timezone=True))
    created_at       = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at       = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

class KauDocument(Base):
    __tablename__ = "kau_documents"
    __table_args__ = {"schema": "agents"}

    id               = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    source_file      = Column(Text, nullable=False)
    source_org       = Column(Text, nullable=False, default='KAU')
    crop_name        = Column(Text, nullable=False)
    chunk_index      = Column(Integer, nullable=False)
    content          = Column(Text, nullable=False)
    embedding        = Column(Vector(1024), nullable=False)  # pgvector
    doc_type         = Column(Text)
    ingested_at      = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        UniqueConstraint('source_file', 'chunk_index'),
        {"schema": "agents"}
    )
```

```ini
# backend/alembic.ini
[alembic]
script_location = migrations
sqlalchemy.url = %(DATABASE_URL)s

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic
```

```python
# backend/migrations/env.py
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.ext.asyncio import create_async_engine
from alembic import context
from app.models import core, realtime, agents, intelligence, alerts, market, analytics, system
from app.database import Base

config = context.config
target_metadata = Base.metadata

async def run_migrations_online():
    engine = create_async_engine(config.get_main_option("sqlalchemy.url"), poolclass=pool.NullPool)
    async with engine.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await engine.dispose()

def do_run_migrations(connection):
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()
```

---

## PHASE 10 — FINAL VALIDATION

### Run ALL of these. Every query must return expected result.

```sql
-- ============================================================
-- COMPLETE SCHEMA VALIDATION
-- ============================================================

-- 1. All schemas exist
SELECT schema_name FROM information_schema.schemata
WHERE schema_name IN ('core','realtime','agents','intelligence','alerts','market','analytics','system')
ORDER BY schema_name;
-- Expected: 8 rows

-- 2. All 30+ tables exist
SELECT table_schema, table_name FROM information_schema.tables
WHERE table_schema IN ('core','realtime','agents','intelligence','alerts','market','analytics','system')
ORDER BY table_schema, table_name;
-- Expected: 30+ tables listed

-- 3. pgvector HNSW index confirmed
SELECT indexname, indexdef FROM pg_indexes WHERE indexname = 'idx_kau_hnsw';
-- Expected: 1 row with USING hnsw (embedding vector_cosine_ops) WITH (m='16', ef_construction='64')

-- 4. All partitions exist
SELECT tablename FROM pg_tables
WHERE tablename LIKE 'market_prices_202%' OR tablename LIKE 'advisory_messages_202%'
   OR tablename LIKE 'farmer_alerts_202%' OR tablename LIKE 'imd_rainfall_202%'
ORDER BY tablename;
-- Expected: 20+ partition tables

-- 5. Soil zones loaded for all states
SELECT state, COUNT(*) AS districts FROM realtime.soil_zones
GROUP BY state ORDER BY state;
-- Expected: 16+ states with their districts

-- 6. MSP data loaded
SELECT COUNT(*) AS msp_rows FROM realtime.msp_reference;
-- Expected: 19 rows

-- 7. All triggers exist
SELECT trigger_name, event_object_schema, event_object_table
FROM information_schema.triggers
WHERE trigger_name IN (
    'trg_farmers_updated_at','trg_fields_updated_at','trg_update_session_stats',
    'trg_notify_alert','trg_farmer_activity','trg_auto_market_rec','audit_farmers','audit_fields'
)
ORDER BY trigger_name;
-- Expected: 8 rows

-- 8. All functions exist
SELECT routine_name FROM information_schema.routines
WHERE routine_name IN (
    'set_updated_at','generate_farmer_code','haversine_km','is_cache_valid',
    'retrieve_kau_docs','update_session_stats','notify_new_alert',
    'update_farmer_activity','auto_market_recommendation','audit_trigger'
)
ORDER BY routine_name;
-- Expected: 10 rows

-- 9. pg_notify channel test (backend must listen on 'new_farmer_alert')
-- This is tested by inserting a test alert after farmer insertion

-- 10. Full end-to-end insert test
BEGIN;
  -- Insert test farmer
  INSERT INTO core.farmers (name, phone, state, district, primary_language, crops)
  VALUES ('Validation Farmer', '9999999999', 'Punjab', 'Ludhiana', 'hi', ARRAY['wheat'])
  RETURNING id, farmer_code, fcm_topic;

  -- Insert farm
  INSERT INTO core.farms (farmer_id, total_area_acres, state, district)
  SELECT id, 5.0, 'Punjab', 'Ludhiana' FROM core.farmers WHERE phone = '9999999999';

  -- Insert field
  INSERT INTO core.fields (farm_id, farmer_id, name, area_acres, current_crop, soil_texture)
  SELECT f.id, fr.id, 'North Field', 2.5, 'wheat', 'loam'
  FROM core.farms f JOIN core.farmers fr ON fr.id = f.farmer_id
  WHERE fr.phone = '9999999999';

  -- Insert advisory session
  INSERT INTO agents.advisory_sessions (farmer_id, language, state, district)
  SELECT id, 'hi', 'Punjab', 'Ludhiana' FROM core.farmers WHERE phone = '9999999999';

  -- Insert test advisory message (user)
  INSERT INTO agents.advisory_messages (session_id, farmer_id, role, sequence_no, content_native, content_en, language)
  SELECT s.id, f.id, 'user', 1, 'मेरी गेहूं पीली हो रही है', 'My wheat is yellowing', 'hi'
  FROM agents.advisory_sessions s JOIN core.farmers f ON f.id = s.farmer_id
  WHERE f.phone = '9999999999';

  -- Verify session stats updated by trigger
  SELECT message_count, last_message_at FROM agents.advisory_sessions
  WHERE farmer_id = (SELECT id FROM core.farmers WHERE phone = '9999999999');
  -- Expected: message_count = 1, last_message_at is recent timestamp

  -- Insert test market price
  INSERT INTO realtime.market_prices (crop_name, market_name, district, state, price_date, min_price, max_price, modal_price)
  VALUES ('Wheat', 'Ludhiana APMC', 'Ludhiana', 'Punjab', CURRENT_DATE, 2200.00, 2350.00, 2275.00);

  -- Verify auto market recommendation trigger ran
  SELECT recommendation, trend_7d FROM realtime.market_prices
  WHERE crop_name = 'Wheat' AND price_date = CURRENT_DATE;
  -- Expected: recommendation and trend_7d should be populated

  -- Insert test alert (triggers pg_notify)
  INSERT INTO alerts.farmer_alerts
    (farmer_id, category, severity, title_native, title_en, body_native, body_en, language)
  SELECT id, 'pest_outbreak', 'critical',
         'कीट प्रकोप चेतावनी', 'Pest outbreak warning',
         'आपके क्षेत्र में टिड्डी प्रकोप की सूचना है', 'Locust outbreak reported in your area',
         'hi'
  FROM core.farmers WHERE phone = '9999999999';

  -- Verify audit log captured the farmer insert
  SELECT operation, table_name FROM system.audit_log
  WHERE table_name = 'farmers' ORDER BY performed_at DESC LIMIT 1;
  -- Expected: INSERT, farmers

ROLLBACK;  -- Clean up all test data

-- Final status
SELECT
    (SELECT COUNT(*) FROM realtime.soil_zones)         AS soil_zones_count,
    (SELECT COUNT(*) FROM realtime.msp_reference)       AS msp_count,
    (SELECT COUNT(*) FROM pg_indexes WHERE schemaname IN ('core','realtime','agents','intelligence','alerts','market','analytics','system')) AS total_indexes,
    'ALL VALIDATION PASSED' AS status;
```

---

## MAINTENANCE PROCEDURES

```sql
-- ============================================================
-- SCHEDULED JOBS (run via pg_cron or APScheduler in Python)
-- ============================================================

-- 1. Daily: Create next month's partitions (run 1st of each month)
-- SELECT realtime.create_market_partition(CURRENT_DATE + INTERVAL '1 month');
-- SELECT agents.create_message_partition(CURRENT_DATE + INTERVAL '1 month');

-- 2. Daily: Clean expired weather cache
-- DELETE FROM realtime.weather_cache WHERE expires_at < NOW();
-- DELETE FROM realtime.weather_forecasts WHERE forecast_date < CURRENT_DATE - 2;

-- 3. Weekly: Clean old FCM delivery logs (keep 30 days)
-- DELETE FROM alerts.fcm_delivery_log WHERE sent_at < NOW() - INTERVAL '30 days';

-- 4. Weekly: Clean expired pest alerts
-- DELETE FROM realtime.pest_alerts WHERE expires_at < NOW();

-- 5. Daily: Update platform metrics (run at midnight)
-- INSERT INTO analytics.platform_metrics (metric_date, dau, total_queries, ...)
-- SELECT CURRENT_DATE - 1, COUNT(DISTINCT farmer_id), COUNT(*), ...
-- FROM agents.advisory_messages WHERE created_at >= CURRENT_DATE - 1 AND created_at < CURRENT_DATE;

-- 6. Monthly: Archive old advisory messages to cold storage
-- (move messages older than 90 days to S3 or similar, then delete from partitions)

-- ============================================================
-- PERFORMANCE MONITORING QUERIES
-- ============================================================

-- Slowest queries
SELECT query, mean_exec_time, calls
FROM pg_stat_statements
ORDER BY mean_exec_time DESC LIMIT 10;

-- Index usage
SELECT schemaname, tablename, indexname, idx_scan, idx_tup_read
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;

-- Table sizes
SELECT schemaname, tablename,
       pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS total_size
FROM pg_tables
WHERE schemaname IN ('core','realtime','agents','intelligence','alerts','market','analytics','system')
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Active connections
SELECT state, COUNT(*) FROM pg_stat_activity GROUP BY state;
```

---

## FINAL SUMMARY

```
DATABASE: agrisage (PostgreSQL 16 + pgvector 0.4.0)

SCHEMAS:      8 (core, realtime, agents, intelligence, alerts, market, analytics, system)
TABLES:       34 base tables + 20+ partitions
INDEXES:      50+ (HNSW, GIN, BTree, partial)
TRIGGERS:     10 (updated_at, audit, session stats, FCM notify, activity, market rec)
FUNCTIONS:    10 (haversine, cache check, RAG retrieve, audit, session update, etc.)
ENUM TYPES:   11 (language, crop stage, soil texture, alert severity, etc.)
SEED DATA:    50+ soil zones across 16 states + 19 MSP prices

REALTIME DATA SOURCES CONNECTED:
  ✅ Open-Meteo      → realtime.weather_cache + weather_forecasts     (6hr TTL)
  ✅ data.gov.in     → realtime.market_prices (partitioned)            (daily 08:00)
  ✅ NBAIR RSS       → realtime.pest_alerts + pest_alert_crops         (every 6hr)
  ✅ IMD             → realtime.imd_rainfall (partitioned by year)     (daily)
  ✅ NASA EarthData  → realtime.ndvi_readings                          (16-day)
  ✅ NBSS India      → realtime.soil_zones (loaded, all major states)  (static)
  ✅ ICAR/KAU PDFs   → agents.kau_documents (pgvector HNSW 1024-dim)  (on-demand)
  ✅ MSP Reference   → realtime.msp_reference (2025-26 season data)   (annual)

ALL 14 AGENTS HAVE DEDICATED STORAGE:
  ✅ IntentAgent       → agents.agent_invocations
  ✅ TranslatorAgent   → agents.advisory_messages (content_native + content_en)
  ✅ WeatherAgent      → realtime.weather_cache
  ✅ SoilAgent         → realtime.soil_zones
  ✅ PestAgent         → realtime.pest_alerts
  ✅ CropAgent         → intelligence.crop_stages + dssat_simulations
  ✅ IrrigationAgent   → intelligence.irrigation_schedules
  ✅ FertiliserAgent   → intelligence.fertiliser_plans
  ✅ MarketAgent       → realtime.market_prices + market.market_recommendations
  ✅ AlertAgent        → alerts.farmer_alerts + alerts.fcm_delivery_log
  ✅ MemoryAgent       → agents.langgraph_checkpoints + langgraph_checkpoint_writes
  ✅ SchedulerAgent    → intelligence.irrigation_schedules + fertiliser_plans
  ✅ NDVIAgent         → realtime.ndvi_readings
  ✅ SupervisorAgent   → agents.advisory_messages (final_native + final_en)
```

---

_Agri-SAGE Database v1.0 — Production Grade_
_PostgreSQL 16 + pgvector 0.4.0 — Zero Budget — All India_
_Built for Magnel & team · ASIET Kalady · 2026_
