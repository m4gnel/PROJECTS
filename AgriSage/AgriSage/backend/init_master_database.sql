-- ============================================================
-- 🌾 AGRI-SAGE — MASTER DATABASE INITIALIZATION SCRIPT
-- PostgreSQL 16 + pgvector 0.4.0
-- Complete production database schema, indexes, functions,
-- triggers, partitioning, seed data, and validation suite.
-- ============================================================

-- ============================================================
-- PHASE 1 — EXTENSIONS & DATABASE FOUNDATIONS
-- ============================================================

CREATE EXTENSION IF NOT EXISTS vector;             -- pgvector 0.4.0
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";        -- UUID generation
CREATE EXTENSION IF NOT EXISTS pg_trgm;            -- text search trigrams
CREATE EXTENSION IF NOT EXISTS btree_gin;          -- GIN index on btree types
CREATE EXTENSION IF NOT EXISTS pg_stat_statements; -- query performance monitoring

-- SCHEMAS (namespace separation)
CREATE SCHEMA IF NOT EXISTS core;          -- farmer, farm, field entities
CREATE SCHEMA IF NOT EXISTS realtime;      -- weather, market, pest live data
CREATE SCHEMA IF NOT EXISTS agents;        -- AI agent state, embeddings, sessions
CREATE SCHEMA IF NOT EXISTS intelligence;  -- field observations, DSSAT, plans
CREATE SCHEMA IF NOT EXISTS alerts;        -- farmer notifications
CREATE SCHEMA IF NOT EXISTS market;        -- market intelligence
CREATE SCHEMA IF NOT EXISTS analytics;     -- metrics and performance
CREATE SCHEMA IF NOT EXISTS system;        -- audit, rate limits, migrations

-- ENUM TYPES
DO $$ BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'language_code') THEN
        CREATE TYPE public.language_code AS ENUM ('hi', 'en', 'ta', 'ml', 'te', 'pa');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'agroclimatic_zone') THEN
        CREATE TYPE public.agroclimatic_zone AS ENUM (
            'western_himalayan', 'eastern_himalayan', 'lower_gangetic_plains',
            'middle_gangetic_plains', 'upper_gangetic_plains', 'trans_gangetic_plains',
            'eastern_plateau_hills', 'central_plateau_hills', 'western_plateau_hills',
            'southern_plateau_hills', 'east_coast_plains', 'west_coast_plains',
            'gujarat_plains', 'western_dry', 'island_territories'
        );
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'crop_stage') THEN
        CREATE TYPE public.crop_stage AS ENUM (
            'land_preparation', 'sowing', 'germination', 'seedling', 'vegetative',
            'tillering', 'stem_elongation', 'heading', 'flowering', 'grain_filling',
            'maturity', 'harvest', 'post_harvest', 'fallow'
        );
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'soil_texture') THEN
        CREATE TYPE public.soil_texture AS ENUM (
            'sandy', 'loamy_sand', 'sandy_loam', 'loam', 'silt_loam', 'silt',
            'clay_loam', 'sandy_clay_loam', 'silty_clay_loam', 'sandy_clay',
            'silty_clay', 'clay', 'laterite', 'black_cotton', 'alluvial', 'red_laterite'
        );
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'irrigation_type') THEN
        CREATE TYPE public.irrigation_type AS ENUM (
            'rain_fed', 'canal', 'borewell', 'open_well', 'drip', 'sprinkler',
            'flood', 'tank', 'lift_irrigation'
        );
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'alert_severity') THEN
        CREATE TYPE public.alert_severity AS ENUM ('critical', 'warning', 'info', 'success');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'alert_category') THEN
        CREATE TYPE public.alert_category AS ENUM (
            'pest_outbreak', 'weather_extreme', 'disease_risk', 'irrigation_needed',
            'fertiliser_due', 'harvest_ready', 'market_price', 'crop_stage_update',
            'soil_health', 'government_scheme'
        );
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'message_role') THEN
        CREATE TYPE public.message_role AS ENUM ('user', 'assistant', 'system');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'price_trend') THEN
        CREATE TYPE public.price_trend AS ENUM ('rising', 'falling', 'stable', 'volatile');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'market_recommendation') THEN
        CREATE TYPE public.market_recommendation AS ENUM ('sell_now', 'hold', 'sell_partial', 'buy_input');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'nutrient_status') THEN
        CREATE TYPE public.nutrient_status AS ENUM ('deficient', 'low', 'medium', 'high', 'excessive');
    END IF;
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'field_status') THEN
        CREATE TYPE public.field_status AS ENUM ('active', 'fallow', 'harvesting', 'resting', 'sold');
    END IF;
END $$;

-- UTILITY FUNCTIONS
CREATE OR REPLACE FUNCTION public.set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

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

CREATE OR REPLACE FUNCTION public.is_cache_valid(fetched_at TIMESTAMPTZ, ttl_seconds INT)
RETURNS BOOLEAN AS $$
BEGIN
    RETURN (NOW() - fetched_at) < (ttl_seconds * INTERVAL '1 second');
END;
$$ LANGUAGE plpgsql IMMUTABLE;

CREATE OR REPLACE FUNCTION public.get_partition_name(base TEXT, dt DATE)
RETURNS TEXT AS $$
BEGIN
    RETURN base || '_' || TO_CHAR(dt, 'YYYY_MM');
END;
$$ LANGUAGE plpgsql IMMUTABLE;


-- ============================================================
-- PHASE 2 — CORE LAYER: FARMERS, FARMS, FIELDS
-- ============================================================

CREATE TABLE IF NOT EXISTS core.farmers (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_code         TEXT UNIQUE NOT NULL DEFAULT public.generate_farmer_code(),

    -- Identity
    name                TEXT NOT NULL CHECK (length(name) BETWEEN 2 AND 100),
    phone               TEXT UNIQUE CHECK (phone ~ '^[6-9][0-9]{9}$'),
    phone_verified      BOOLEAN NOT NULL DEFAULT FALSE,

    -- Location (India-specific)
    country             TEXT NOT NULL DEFAULT 'India',
    state               TEXT NOT NULL CHECK (length(state) BETWEEN 2 AND 60),
    district            TEXT NOT NULL CHECK (length(district) BETWEEN 2 AND 60),
    taluk               TEXT,
    village             TEXT,
    pincode             TEXT CHECK (pincode ~ '^[1-9][0-9]{5}$'),
    lat                 FLOAT CHECK (lat BETWEEN 6.0 AND 38.0),
    lon                 FLOAT CHECK (lon BETWEEN 68.0 AND 97.5),
    location_accuracy_m FLOAT,

    -- Preferences
    primary_language    public.language_code NOT NULL DEFAULT 'hi',
    secondary_language  public.language_code,
    crops               TEXT[] NOT NULL DEFAULT '{}',
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
    deleted_at          TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_farmers_phone ON core.farmers(phone) WHERE phone IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_farmers_state_district ON core.farmers(state, district);
CREATE INDEX IF NOT EXISTS idx_farmers_crops ON core.farmers USING GIN(crops);
CREATE INDEX IF NOT EXISTS idx_farmers_location ON core.farmers(lat, lon) WHERE lat IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_farmers_active ON core.farmers(last_active_at DESC) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_farmers_fcm_topic ON core.farmers(fcm_topic);

CREATE OR REPLACE TRIGGER trg_farmers_updated_at
    BEFORE UPDATE ON core.farmers
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TABLE IF NOT EXISTS core.fcm_tokens (
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

CREATE INDEX IF NOT EXISTS idx_fcm_tokens_farmer ON core.fcm_tokens(farmer_id) WHERE is_active = TRUE;

CREATE TABLE IF NOT EXISTS core.farms (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    name                TEXT NOT NULL DEFAULT 'My Farm',
    total_area_acres    FLOAT NOT NULL CHECK (total_area_acres > 0 AND total_area_acres < 10000),
    ownership_type      TEXT CHECK (ownership_type IN ('owned','leased','sharecrop','inherited')),
    land_record_number  TEXT,

    -- Location
    state               TEXT NOT NULL,
    district            TEXT NOT NULL,
    taluk               TEXT,
    village             TEXT,
    lat                 FLOAT CHECK (lat BETWEEN 6.0 AND 38.0),
    lon                 FLOAT CHECK (lon BETWEEN 68.0 AND 97.5),

    -- Soil summary
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

CREATE INDEX IF NOT EXISTS idx_farms_farmer_id ON core.farms(farmer_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_farms_state_district ON core.farms(state, district);

CREATE OR REPLACE TRIGGER trg_farms_updated_at
    BEFORE UPDATE ON core.farms
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TABLE IF NOT EXISTS core.fields (
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

    -- Soil
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
    boundary_geojson    JSONB,

    -- Metadata
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    deleted_at          TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_fields_farm_id ON core.fields(farm_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_fields_farmer_id ON core.fields(farmer_id) WHERE deleted_at IS NULL;
CREATE INDEX IF NOT EXISTS idx_fields_crop ON core.fields(current_crop) WHERE current_crop IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_fields_status ON core.fields(status);
CREATE INDEX IF NOT EXISTS idx_fields_location ON core.fields(lat, lon) WHERE lat IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_fields_harvest ON core.fields(expected_harvest) WHERE status = 'active';

CREATE OR REPLACE TRIGGER trg_fields_updated_at
    BEFORE UPDATE ON core.fields
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();


-- ============================================================
-- PHASE 3 — REALTIME DATA LAYER
-- ============================================================

CREATE TABLE IF NOT EXISTS realtime.weather_cache (
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
    weather_code        INT,
    weather_description TEXT,

    -- Agri advisory flags
    advice_flag         TEXT CHECK (advice_flag IN (
                            'NORMAL','SPRAY_RISK','IRRIGATION_NEEDED',
                            'FLOOD_RISK','FROST_RISK','HEAT_STRESS',
                            'STRONG_WIND','HAILSTORM_RISK'
                        )) DEFAULT 'NORMAL',
    spray_window_open   BOOLEAN DEFAULT TRUE,
    field_work_suitable BOOLEAN DEFAULT TRUE,

    -- Cache metadata
    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at          TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '6 hours'),
    source              TEXT NOT NULL DEFAULT 'open-meteo',
    UNIQUE (state, district)
);

CREATE INDEX IF NOT EXISTS idx_weather_district ON realtime.weather_cache(state, district);
CREATE INDEX IF NOT EXISTS idx_weather_expires ON realtime.weather_cache(expires_at);
CREATE INDEX IF NOT EXISTS idx_weather_fetched ON realtime.weather_cache(fetched_at DESC);

CREATE TABLE IF NOT EXISTS realtime.weather_forecasts (
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

    spray_suitable      BOOLEAN,
    irrigation_needed   BOOLEAN,
    field_work_suitable BOOLEAN,

    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at          TIMESTAMPTZ NOT NULL DEFAULT (NOW() + INTERVAL '12 hours'),
    UNIQUE (state, district, forecast_date)
);

CREATE INDEX IF NOT EXISTS idx_forecasts_location_date ON realtime.weather_forecasts(state, district, forecast_date);
CREATE INDEX IF NOT EXISTS idx_forecasts_expires ON realtime.weather_forecasts(expires_at);

CREATE TABLE IF NOT EXISTS realtime.market_prices (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_name           TEXT NOT NULL,
    crop_variety        TEXT,
    market_name         TEXT NOT NULL,
    district            TEXT NOT NULL,
    state               TEXT NOT NULL,
    price_date          DATE NOT NULL,

    min_price           NUMERIC(10,2) CHECK (min_price >= 0),
    max_price           NUMERIC(10,2) CHECK (max_price >= 0),
    modal_price         NUMERIC(10,2) CHECK (modal_price >= 0),

    msp_price           NUMERIC(10,2),
    above_msp           BOOLEAN GENERATED ALWAYS AS (modal_price > msp_price) STORED,

    trend_7d            public.price_trend,
    trend_30d           public.price_trend,
    pct_change_7d       FLOAT,
    recommendation      public.market_recommendation,

    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    source              TEXT NOT NULL DEFAULT 'data.gov.in',
    UNIQUE (crop_name, market_name, district, state, price_date)
) PARTITION BY RANGE (price_date);

-- Partition creation for market_prices
CREATE TABLE IF NOT EXISTS realtime.market_prices_2026_07 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
CREATE TABLE IF NOT EXISTS realtime.market_prices_2026_08 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
CREATE TABLE IF NOT EXISTS realtime.market_prices_2026_09 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
CREATE TABLE IF NOT EXISTS realtime.market_prices_2026_10 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
CREATE TABLE IF NOT EXISTS realtime.market_prices_2026_11 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');
CREATE TABLE IF NOT EXISTS realtime.market_prices_2026_12 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2026-12-01') TO ('2027-01-01');
CREATE TABLE IF NOT EXISTS realtime.market_prices_2027_01 PARTITION OF realtime.market_prices
    FOR VALUES FROM ('2027-01-01') TO ('2027-02-01');

CREATE INDEX IF NOT EXISTS idx_market_crop_state_date ON realtime.market_prices(crop_name, state, price_date DESC);
CREATE INDEX IF NOT EXISTS idx_market_district ON realtime.market_prices(district, state, price_date DESC);
CREATE INDEX IF NOT EXISTS idx_market_above_msp ON realtime.market_prices(crop_name) WHERE above_msp = TRUE;

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

CREATE TABLE IF NOT EXISTS realtime.pest_alerts (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    external_id         TEXT UNIQUE,
    title               TEXT NOT NULL,
    description         TEXT,
    full_content        TEXT,
    severity            public.alert_severity NOT NULL DEFAULT 'warning',

    affected_states     TEXT[] DEFAULT '{}',
    affected_districts  TEXT[] DEFAULT '{}',
    is_national         BOOLEAN DEFAULT FALSE,

    pest_name           TEXT,
    pest_scientific     TEXT,
    damage_type         TEXT,

    source_url          TEXT,
    source_org          TEXT DEFAULT 'NBAIR',
    published_at        TIMESTAMPTZ,
    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at          TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '7 days')
);

CREATE TABLE IF NOT EXISTS realtime.pest_alert_crops (
    alert_id            UUID NOT NULL REFERENCES realtime.pest_alerts(id) ON DELETE CASCADE,
    crop_name           TEXT NOT NULL,
    affinity_score      FLOAT CHECK (affinity_score BETWEEN 0 AND 1),
    PRIMARY KEY (alert_id, crop_name)
);

CREATE INDEX IF NOT EXISTS idx_pest_severity ON realtime.pest_alerts(severity, fetched_at DESC);
CREATE INDEX IF NOT EXISTS idx_pest_states ON realtime.pest_alerts USING GIN(affected_states);
CREATE INDEX IF NOT EXISTS idx_pest_districts ON realtime.pest_alerts USING GIN(affected_districts);
CREATE INDEX IF NOT EXISTS idx_pest_expires ON realtime.pest_alerts(expires_at);
CREATE INDEX IF NOT EXISTS idx_pest_alert_crops_crop ON realtime.pest_alert_crops(crop_name);

CREATE TABLE IF NOT EXISTS realtime.soil_zones (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    state               TEXT NOT NULL,
    district            TEXT NOT NULL,
    agroclimatic_zone   public.agroclimatic_zone,

    primary_texture     public.soil_texture NOT NULL,
    secondary_texture   public.soil_texture,
    ph_min              FLOAT NOT NULL CHECK (ph_min BETWEEN 3.0 AND 10.0),
    ph_max              FLOAT NOT NULL CHECK (ph_max BETWEEN 3.0 AND 10.0),
    ph_optimal          FLOAT GENERATED ALWAYS AS ((ph_min + ph_max) / 2) STORED,
    organic_carbon      public.nutrient_status NOT NULL DEFAULT 'medium',
    cec_meq             FLOAT,

    nitrogen_status     public.nutrient_status NOT NULL DEFAULT 'medium',
    phosphorus_status   public.nutrient_status NOT NULL DEFAULT 'medium',
    potassium_status    public.nutrient_status NOT NULL DEFAULT 'high',

    zinc_deficient      BOOLEAN DEFAULT FALSE,
    boron_deficient     BOOLEAN DEFAULT FALSE,
    sulphur_deficient   BOOLEAN DEFAULT FALSE,
    iron_deficient      BOOLEAN DEFAULT FALSE,

    water_holding_capacity TEXT CHECK (water_holding_capacity IN ('low','medium','high')),
    drainage             TEXT CHECK (drainage IN ('poor','moderate','well','excessive')),
    annual_rainfall_mm_avg FLOAT,

    suitable_crops       TEXT[] NOT NULL DEFAULT '{}',
    unsuitable_crops     TEXT[] DEFAULT '{}',
    special_notes        TEXT,

    data_source          TEXT DEFAULT 'NBSS&LUP',
    data_year            INT DEFAULT 2024,
    created_at           TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (state, district)
);

CREATE INDEX IF NOT EXISTS idx_soil_state_district ON realtime.soil_zones(state, district);
CREATE INDEX IF NOT EXISTS idx_soil_suitable_crops ON realtime.soil_zones USING GIN(suitable_crops);
CREATE INDEX IF NOT EXISTS idx_soil_zone ON realtime.soil_zones(agroclimatic_zone);

CREATE TABLE IF NOT EXISTS realtime.imd_rainfall (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    state               TEXT NOT NULL,
    district            TEXT NOT NULL,
    reading_date        DATE NOT NULL,
    rainfall_mm         FLOAT NOT NULL DEFAULT 0 CHECK (rainfall_mm >= 0),
    normal_rainfall_mm  FLOAT,
    departure_pct       FLOAT,
    is_deficient        BOOLEAN,
    is_excess           BOOLEAN,
    season              TEXT CHECK (season IN ('kharif','rabi','zaid','annual')),
    cumulative_mm       FLOAT,
    source              TEXT DEFAULT 'IMD',
    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (state, district, reading_date)
) PARTITION BY RANGE (reading_date);

CREATE TABLE IF NOT EXISTS realtime.imd_rainfall_2026 PARTITION OF realtime.imd_rainfall
    FOR VALUES FROM ('2026-01-01') TO ('2027-01-01');
CREATE TABLE IF NOT EXISTS realtime.imd_rainfall_2027 PARTITION OF realtime.imd_rainfall
    FOR VALUES FROM ('2027-01-01') TO ('2028-01-01');

CREATE INDEX IF NOT EXISTS idx_rainfall_location_date ON realtime.imd_rainfall(state, district, reading_date DESC);

CREATE TABLE IF NOT EXISTS realtime.ndvi_readings (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id            UUID REFERENCES core.fields(id) ON DELETE CASCADE,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    lat                 FLOAT NOT NULL,
    lon                 FLOAT NOT NULL,
    reading_date        DATE NOT NULL,

    ndvi                FLOAT CHECK (ndvi BETWEEN -1.0 AND 1.0),
    evi                 FLOAT,
    pixel_reliability   INT CHECK (pixel_reliability BETWEEN 0 AND 3),
    is_cloud_affected   BOOLEAN DEFAULT FALSE,

    health_category     TEXT CHECK (health_category IN (
                            'bare_soil','sparse_vegetation','moderate',
                            'good','excellent','stress_detected'
                        )),
    health_score        INT CHECK (health_score BETWEEN 0 AND 100),
    stress_type         TEXT,

    satellite_product   TEXT DEFAULT 'MOD13Q1',
    spatial_resolution_m INT DEFAULT 250,
    source              TEXT DEFAULT 'NASA-EOSDIS',
    fetched_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (field_id, reading_date)
);

CREATE INDEX IF NOT EXISTS idx_ndvi_field_date ON realtime.ndvi_readings(field_id, reading_date DESC)
    WHERE field_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_ndvi_farmer_date ON realtime.ndvi_readings(farmer_id, reading_date DESC);
CREATE INDEX IF NOT EXISTS idx_ndvi_health ON realtime.ndvi_readings(health_category) WHERE is_cloud_affected = FALSE;


-- ============================================================
-- PHASE 4 — AGENT & AI LAYER
-- ============================================================

CREATE TABLE IF NOT EXISTS agents.advisory_sessions (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    session_token       TEXT UNIQUE NOT NULL DEFAULT gen_random_uuid()::TEXT,

    language            public.language_code NOT NULL DEFAULT 'hi',
    state               TEXT NOT NULL,
    district            TEXT NOT NULL,
    primary_crop        TEXT,
    active_field_id     UUID REFERENCES core.fields(id),

    is_active           BOOLEAN NOT NULL DEFAULT TRUE,
    message_count       INT NOT NULL DEFAULT 0,
    total_tokens_used   INT DEFAULT 0,
    total_cost_usd      FLOAT DEFAULT 0,

    avg_response_ms     FLOAT,
    farmer_satisfaction INT CHECK (farmer_satisfaction BETWEEN 1 AND 5),

    started_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_message_at     TIMESTAMPTZ,
    ended_at            TIMESTAMPTZ,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_sessions_farmer ON agents.advisory_sessions(farmer_id, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_sessions_active ON agents.advisory_sessions(farmer_id) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_sessions_token ON agents.advisory_sessions(session_token);

CREATE TABLE IF NOT EXISTS agents.advisory_messages (
    id                  UUID NOT NULL DEFAULT uuid_generate_v4(),
    session_id          UUID NOT NULL REFERENCES agents.advisory_sessions(id) ON DELETE CASCADE,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    role                public.message_role NOT NULL,
    sequence_no         INT NOT NULL,

    content_native      TEXT NOT NULL,
    content_en          TEXT,
    language            public.language_code NOT NULL,

    agents_used         TEXT[] DEFAULT '{}',
    intent_detected     TEXT[] DEFAULT '{}',
    confidence_score    FLOAT CHECK (confidence_score BETWEEN 0 AND 1),
    response_ms         INT,
    model_used          TEXT DEFAULT 'gemini-1.5-flash',
    tokens_in           INT,
    tokens_out          INT,

    used_weather_data   BOOLEAN DEFAULT FALSE,
    used_soil_data      BOOLEAN DEFAULT FALSE,
    used_pest_data      BOOLEAN DEFAULT FALSE,
    used_market_data    BOOLEAN DEFAULT FALSE,
    used_rag_docs       BOOLEAN DEFAULT FALSE,
    used_dssat          BOOLEAN DEFAULT FALSE,
    used_ndvi           BOOLEAN DEFAULT FALSE,

    was_helpful         BOOLEAN,
    was_acted_upon      BOOLEAN,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (id, created_at)
) PARTITION BY RANGE (created_at);

CREATE TABLE IF NOT EXISTS agents.advisory_messages_2026_07 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2026-07-01') TO ('2026-08-01');
CREATE TABLE IF NOT EXISTS agents.advisory_messages_2026_08 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2026-08-01') TO ('2026-09-01');
CREATE TABLE IF NOT EXISTS agents.advisory_messages_2026_09 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2026-09-01') TO ('2026-10-01');
CREATE TABLE IF NOT EXISTS agents.advisory_messages_2026_10 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2026-10-01') TO ('2026-11-01');
CREATE TABLE IF NOT EXISTS agents.advisory_messages_2026_11 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2026-11-01') TO ('2026-12-01');
CREATE TABLE IF NOT EXISTS agents.advisory_messages_2026_12 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2026-12-01') TO ('2027-01-01');
CREATE TABLE IF NOT EXISTS agents.advisory_messages_2027_01 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2027-01-01') TO ('2027-02-01');
CREATE TABLE IF NOT EXISTS agents.advisory_messages_2027_02 PARTITION OF agents.advisory_messages
    FOR VALUES FROM ('2027-02-01') TO ('2027-03-01');

CREATE INDEX IF NOT EXISTS idx_messages_session ON agents.advisory_messages(session_id, sequence_no);
CREATE INDEX IF NOT EXISTS idx_messages_farmer ON agents.advisory_messages(farmer_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_messages_role ON agents.advisory_messages(role, created_at DESC);

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

CREATE TABLE IF NOT EXISTS agents.agent_invocations (
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
    input_summary       JSONB,
    output_summary      JSONB,
    gemini_calls        INT DEFAULT 0,
    gemini_tokens       INT DEFAULT 0,
    cache_hit           BOOLEAN DEFAULT FALSE
);

CREATE INDEX IF NOT EXISTS idx_invocations_session ON agents.agent_invocations(session_id);
CREATE INDEX IF NOT EXISTS idx_invocations_agent ON agents.agent_invocations(agent_name, started_at DESC);
CREATE INDEX IF NOT EXISTS idx_invocations_errors ON agents.agent_invocations(agent_name) WHERE succeeded = FALSE;
CREATE INDEX IF NOT EXISTS idx_invocations_slow ON agents.agent_invocations(duration_ms DESC) WHERE duration_ms > 3000;

CREATE TABLE IF NOT EXISTS agents.kau_documents (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_file         TEXT NOT NULL,
    source_org          TEXT NOT NULL DEFAULT 'KAU',
    crop_name           TEXT NOT NULL,
    state_relevance     TEXT[] DEFAULT '{}',
    chunk_index         INT NOT NULL,
    total_chunks        INT,
    content             TEXT NOT NULL,
    content_length      INT GENERATED ALWAYS AS (length(content)) STORED,

    embedding           vector(1024) NOT NULL,

    doc_type            TEXT CHECK (doc_type IN (
                            'package_of_practices','pest_management',
                            'soil_management','irrigation_guide',
                            'post_harvest','market_linkage',
                            'government_scheme','variety_guide'
                        )),
    crop_stage_relevance TEXT[],
    season_relevance     TEXT[],

    ingested_at         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_retrieved_at   TIMESTAMPTZ,
    retrieval_count     INT DEFAULT 0,
    avg_similarity_score FLOAT,

    UNIQUE (source_file, chunk_index)
);

CREATE INDEX IF NOT EXISTS idx_kau_hnsw ON agents.kau_documents
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

CREATE INDEX IF NOT EXISTS idx_kau_crop ON agents.kau_documents(crop_name);
CREATE INDEX IF NOT EXISTS idx_kau_org ON agents.kau_documents(source_org);
CREATE INDEX IF NOT EXISTS idx_kau_state ON agents.kau_documents USING GIN(state_relevance);
CREATE INDEX IF NOT EXISTS idx_kau_stage ON agents.kau_documents USING GIN(crop_stage_relevance);
CREATE INDEX IF NOT EXISTS idx_kau_type ON agents.kau_documents(doc_type);

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
    WITH matches AS (
        SELECT
            kd.id AS m_id,
            kd.content AS m_content,
            kd.source_file AS m_source_file,
            kd.crop_name AS m_crop_name,
            (1 - (kd.embedding <=> query_embedding))::FLOAT AS m_similarity
        FROM agents.kau_documents kd
        WHERE
            (filter_crop IS NULL OR kd.crop_name = filter_crop)
            AND (filter_org IS NULL OR kd.source_org = filter_org)
            AND (1 - (kd.embedding <=> query_embedding)) >= similarity_threshold
        ORDER BY kd.embedding <=> query_embedding
        LIMIT top_k
    ),
    upd AS (
        UPDATE agents.kau_documents kd
        SET last_retrieved_at = NOW(), retrieval_count = COALESCE(kd.retrieval_count, 0) + 1
        FROM matches
        WHERE kd.id = matches.m_id
    )
    SELECT m_id, m_content, m_source_file, m_crop_name, m_similarity FROM matches;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS agents.langgraph_checkpoints (
    thread_id           TEXT NOT NULL,
    checkpoint_id       TEXT NOT NULL,
    checkpoint_ns       TEXT NOT NULL DEFAULT '',
    checkpoint          JSONB NOT NULL,
    metadata            JSONB NOT NULL DEFAULT '{}',
    parent_checkpoint_id TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    PRIMARY KEY (thread_id, checkpoint_ns, checkpoint_id)
);

CREATE TABLE IF NOT EXISTS agents.langgraph_checkpoint_writes (
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

CREATE INDEX IF NOT EXISTS idx_lg_checkpoints_thread ON agents.langgraph_checkpoints(thread_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_lg_writes_thread ON agents.langgraph_checkpoint_writes(thread_id, checkpoint_id);


-- ============================================================
-- PHASE 5 — FIELD INTELLIGENCE, ALERTS & MARKET LAYERS
-- ============================================================

CREATE TABLE IF NOT EXISTS intelligence.field_observations (
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
    description_native  TEXT NOT NULL,
    description_en      TEXT,
    severity_estimate   public.alert_severity DEFAULT 'info',
    area_affected_pct   FLOAT CHECK (area_affected_pct BETWEEN 0 AND 100),

    photo_url           TEXT,
    photo_analysis      JSONB,
    detected_disease    TEXT,
    detected_pest       TEXT,
    confidence_pct      FLOAT CHECK (confidence_pct BETWEEN 0 AND 100),

    triggered_advisory  UUID,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_observations_field ON intelligence.field_observations(field_id, observed_at DESC);
CREATE INDEX IF NOT EXISTS idx_observations_type ON intelligence.field_observations(observation_type, observed_at DESC);
CREATE INDEX IF NOT EXISTS idx_observations_severity ON intelligence.field_observations(severity_estimate);

CREATE TABLE IF NOT EXISTS intelligence.crop_stages (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id            UUID NOT NULL REFERENCES core.fields(id) ON DELETE CASCADE,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id),
    crop_name           TEXT NOT NULL,
    crop_variety        TEXT,
    season              TEXT CHECK (season IN ('kharif','rabi','zaid')),
    season_year         INT NOT NULL,

    current_stage       public.crop_stage NOT NULL,
    stage_started_at    DATE,
    next_stage          public.crop_stage,
    next_stage_eta_days INT,
    days_since_sowing   INT,

    predicted_yield_kg_ha    FLOAT,
    predicted_harvest_date   DATE,
    yield_confidence_pct     FLOAT CHECK (yield_confidence_pct BETWEEN 0 AND 100),
    simulated_at             TIMESTAMPTZ,
    dssat_scenario           JSONB,

    cumulative_et_mm    FLOAT,
    water_stress_index  FLOAT CHECK (water_stress_index BETWEEN 0 AND 1),
    heat_stress_index   FLOAT CHECK (heat_stress_index BETWEEN 0 AND 1),

    updated_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (field_id, crop_name, season_year)
);

CREATE INDEX IF NOT EXISTS idx_crop_stages_field ON intelligence.crop_stages(field_id);
CREATE INDEX IF NOT EXISTS idx_crop_stages_harvest ON intelligence.crop_stages(predicted_harvest_date)
    WHERE current_stage NOT IN ('harvest','post_harvest','fallow');

CREATE OR REPLACE TRIGGER trg_crop_stages_updated_at
    BEFORE UPDATE ON intelligence.crop_stages
    FOR EACH ROW EXECUTE FUNCTION public.set_updated_at();

CREATE TABLE IF NOT EXISTS intelligence.irrigation_schedules (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id            UUID NOT NULL REFERENCES core.fields(id) ON DELETE CASCADE,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id),
    generated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valid_for_date      DATE NOT NULL,

    should_irrigate     BOOLEAN NOT NULL,
    reason              TEXT NOT NULL,
    reason_native       TEXT,
    next_irrigation_date DATE,
    irrigation_amount_mm FLOAT CHECK (irrigation_amount_mm >= 0),
    irrigation_duration_hours FLOAT,

    et0_mm              FLOAT,
    kc_factor           FLOAT,
    etc_mm              FLOAT,
    soil_moisture_pct   FLOAT CHECK (soil_moisture_pct BETWEEN 0 AND 100),
    field_capacity_pct  FLOAT,
    wilting_point_pct   FLOAT,
    rain_forecast_mm    FLOAT DEFAULT 0,

    was_followed        BOOLEAN,
    farmer_notes        TEXT,
    UNIQUE (field_id, valid_for_date)
);

CREATE INDEX IF NOT EXISTS idx_irrigation_field_date ON intelligence.irrigation_schedules(field_id, valid_for_date DESC);
CREATE INDEX IF NOT EXISTS idx_irrigation_due ON intelligence.irrigation_schedules(valid_for_date)
    WHERE should_irrigate = TRUE AND was_followed IS NULL;

CREATE TABLE IF NOT EXISTS intelligence.fertiliser_plans (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id            UUID NOT NULL REFERENCES core.fields(id) ON DELETE CASCADE,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id),
    crop_name           TEXT NOT NULL,
    crop_stage          public.crop_stage NOT NULL,
    generated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    application_date    DATE NOT NULL,

    nitrogen_kg_acre    FLOAT CHECK (nitrogen_kg_acre >= 0),
    phosphorus_kg_acre  FLOAT CHECK (phosphorus_kg_acre >= 0),
    potassium_kg_acre   FLOAT CHECK (potassium_kg_acre >= 0),

    primary_fertiliser  TEXT,
    primary_dose_kg_acre FLOAT,
    secondary_fertiliser TEXT,
    secondary_dose_kg_acre FLOAT,
    micronutrient_needed TEXT,

    application_method  TEXT CHECK (application_method IN (
                            'broadcast','band_placement','fertigation',
                            'foliar_spray','top_dressing','basal'
                        )),
    best_time_of_day    TEXT,
    avoid_if_rain       BOOLEAN DEFAULT FALSE,

    rationale           TEXT NOT NULL,
    rationale_native    TEXT,
    source_doc          TEXT,

    was_followed        BOOLEAN,
    UNIQUE (field_id, crop_stage, application_date)
);

CREATE INDEX IF NOT EXISTS idx_fertiliser_field ON intelligence.fertiliser_plans(field_id, application_date DESC);
CREATE INDEX IF NOT EXISTS idx_fertiliser_due ON intelligence.fertiliser_plans(application_date)
    WHERE was_followed IS NULL;

CREATE TABLE IF NOT EXISTS alerts.farmer_alerts (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    field_id            UUID REFERENCES core.fields(id),

    category            public.alert_category NOT NULL,
    severity            public.alert_severity NOT NULL,
    title_native        TEXT NOT NULL,
    title_en            TEXT NOT NULL,
    body_native         TEXT NOT NULL,
    body_en             TEXT NOT NULL,
    language            public.language_code NOT NULL,

    source_agent        TEXT,
    source_data_type    TEXT,
    source_data_id      UUID,

    action_type         TEXT CHECK (action_type IN (
                            'ask_advisor','scan_crop','check_field',
                            'visit_market','apply_fertiliser','irrigate',
                            'harvest_now','none'
                        )),
    action_deep_link    TEXT,

    fcm_sent            BOOLEAN DEFAULT FALSE,
    fcm_sent_at         TIMESTAMPTZ,
    fcm_message_id      TEXT,

    is_read             BOOLEAN DEFAULT FALSE,
    read_at             TIMESTAMPTZ,
    is_dismissed        BOOLEAN DEFAULT FALSE,
    dismissed_at        TIMESTAMPTZ,
    was_acted_upon      BOOLEAN,
    acted_at            TIMESTAMPTZ,

    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    expires_at          TIMESTAMPTZ DEFAULT (NOW() + INTERVAL '7 days')
) PARTITION BY RANGE (created_at);

CREATE TABLE IF NOT EXISTS alerts.farmer_alerts_2026_q3 PARTITION OF alerts.farmer_alerts
    FOR VALUES FROM ('2026-07-01') TO ('2026-10-01');
CREATE TABLE IF NOT EXISTS alerts.farmer_alerts_2026_q4 PARTITION OF alerts.farmer_alerts
    FOR VALUES FROM ('2026-10-01') TO ('2027-01-01');
CREATE TABLE IF NOT EXISTS alerts.farmer_alerts_2027_q1 PARTITION OF alerts.farmer_alerts
    FOR VALUES FROM ('2027-01-01') TO ('2027-04-01');
CREATE TABLE IF NOT EXISTS alerts.farmer_alerts_2027_q2 PARTITION OF alerts.farmer_alerts
    FOR VALUES FROM ('2027-04-01') TO ('2027-07-01');

CREATE INDEX IF NOT EXISTS idx_farmer_alerts_farmer ON alerts.farmer_alerts(farmer_id, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_farmer_alerts_unread ON alerts.farmer_alerts(farmer_id)
    WHERE is_read = FALSE AND is_dismissed = FALSE;
CREATE INDEX IF NOT EXISTS idx_farmer_alerts_severity ON alerts.farmer_alerts(severity, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_farmer_alerts_expires ON alerts.farmer_alerts(expires_at);

CREATE TABLE IF NOT EXISTS alerts.fcm_delivery_log (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_id            UUID NOT NULL,
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id),
    fcm_token           TEXT NOT NULL,
    fcm_message_id      TEXT,
    topic               TEXT,
    status              TEXT NOT NULL CHECK (status IN (
                            'sent','delivered','failed','invalid_token','not_registered'
                        )),
    error_code          TEXT,
    error_message       TEXT,
    sent_at             TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    delivered_at        TIMESTAMPTZ
);

CREATE INDEX IF NOT EXISTS idx_fcm_log_farmer ON alerts.fcm_delivery_log(farmer_id, sent_at DESC);
CREATE INDEX IF NOT EXISTS idx_fcm_log_status ON alerts.fcm_delivery_log(status) WHERE status != 'delivered';

CREATE TABLE IF NOT EXISTS market.market_recommendations (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    crop_name           TEXT NOT NULL,
    state               TEXT NOT NULL,
    district            TEXT NOT NULL,
    generated_at        TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    current_modal_price NUMERIC(10,2),
    nearest_market      TEXT,
    price_date          DATE,

    recommendation      public.market_recommendation NOT NULL,
    rationale           TEXT NOT NULL,
    rationale_native    TEXT,
    target_price        NUMERIC(10,2),
    hold_until_estimate DATE,

    price_trend_7d      public.price_trend,
    price_trend_30d     public.price_trend,
    pct_above_msp       FLOAT,
    seasonal_factor     TEXT,

    valid_until         DATE DEFAULT (CURRENT_DATE + 3),
    was_helpful         BOOLEAN
);

CREATE INDEX IF NOT EXISTS idx_market_rec_farmer ON market.market_recommendations(farmer_id, generated_at DESC);
CREATE INDEX IF NOT EXISTS idx_market_rec_crop ON market.market_recommendations(crop_name, state, generated_at DESC);

CREATE TABLE IF NOT EXISTS market.price_subscriptions (
    id          UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farmer_id   UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    crop_name   TEXT NOT NULL,
    state       TEXT NOT NULL,
    alert_above NUMERIC(10,2),
    alert_below NUMERIC(10,2),
    is_active   BOOLEAN DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (farmer_id, crop_name, state)
);

CREATE INDEX IF NOT EXISTS idx_price_subs_farmer ON market.price_subscriptions(farmer_id) WHERE is_active = TRUE;


-- ============================================================
-- PHASE 6 — ANALYTICS LAYER
-- ============================================================

CREATE TABLE IF NOT EXISTS analytics.farm_season_analytics (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id                 UUID NOT NULL REFERENCES core.farms(id),
    farmer_id               UUID NOT NULL REFERENCES core.farmers(id),
    crop_name               TEXT NOT NULL,
    season                  TEXT NOT NULL CHECK (season IN ('kharif','rabi','zaid')),
    season_year             INT NOT NULL,

    total_queries           INT DEFAULT 0,
    queries_about_pest      INT DEFAULT 0,
    queries_about_weather   INT DEFAULT 0,
    queries_about_market    INT DEFAULT 0,
    queries_about_soil      INT DEFAULT 0,
    advisories_followed     INT DEFAULT 0,
    advisories_ignored      INT DEFAULT 0,

    critical_alerts_received INT DEFAULT 0,
    alerts_acted_upon        INT DEFAULT 0,

    actual_yield_kg_ha      FLOAT,
    dssat_predicted_yield   FLOAT,
    yield_accuracy_pct      FLOAT GENERATED ALWAYS AS (
        CASE WHEN dssat_predicted_yield > 0
             THEN (1 - ABS(actual_yield_kg_ha - dssat_predicted_yield) / dssat_predicted_yield) * 100
             ELSE NULL END
    ) STORED,
    sold_price_per_quintal  NUMERIC(10,2),
    total_revenue_inr       NUMERIC(12,2),

    overall_satisfaction    INT CHECK (overall_satisfaction BETWEEN 1 AND 5),
    nps_score               INT CHECK (nps_score BETWEEN 0 AND 10),

    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at              TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (farm_id, crop_name, season, season_year)
);

CREATE INDEX IF NOT EXISTS idx_season_analytics_farmer ON analytics.farm_season_analytics(farmer_id);
CREATE INDEX IF NOT EXISTS idx_season_analytics_crop ON analytics.farm_season_analytics(crop_name, season_year);

CREATE TABLE IF NOT EXISTS analytics.agent_performance (
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

CREATE INDEX IF NOT EXISTS idx_agent_perf_date ON analytics.agent_performance(metric_date DESC);
CREATE INDEX IF NOT EXISTS idx_agent_perf_name ON analytics.agent_performance(agent_name, metric_date DESC);

CREATE TABLE IF NOT EXISTS analytics.platform_metrics (
    id                      UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    metric_date             DATE NOT NULL UNIQUE,
    dau                     INT DEFAULT 0,
    new_registrations       INT DEFAULT 0,
    total_registered        INT DEFAULT 0,
    total_queries           INT DEFAULT 0,
    avg_response_ms         FLOAT,
    p95_response_ms         FLOAT,
    total_agent_calls       INT DEFAULT 0,
    gemini_calls_total      INT DEFAULT 0,
    gemini_tokens_total     INT DEFAULT 0,
    alerts_sent             INT DEFAULT 0,
    fcm_success_rate_pct    FLOAT,
    error_count             INT DEFAULT 0,
    error_rate_pct          FLOAT,
    weather_cache_hits      INT DEFAULT 0,
    market_cache_hits       INT DEFAULT 0,
    created_at              TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_platform_metrics_date ON analytics.platform_metrics(metric_date DESC);

CREATE TABLE IF NOT EXISTS analytics.advisory_feedback (
    id                  UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    message_id          UUID NOT NULL,
    session_id          UUID NOT NULL REFERENCES agents.advisory_sessions(id),
    farmer_id           UUID NOT NULL REFERENCES core.farmers(id),
    rating              INT NOT NULL CHECK (rating IN (1, -1)),
    feedback_text       TEXT,
    feedback_text_en    TEXT,
    created_at          TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_feedback_session ON analytics.advisory_feedback(session_id);
CREATE INDEX IF NOT EXISTS idx_feedback_rating ON analytics.advisory_feedback(rating, created_at DESC);


-- ============================================================
-- PHASE 7 — SYSTEM LAYER & REALTIME TRIGGERS
-- ============================================================

CREATE TABLE IF NOT EXISTS system.audit_log (
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

CREATE TABLE IF NOT EXISTS system.audit_log_2026_q4 PARTITION OF system.audit_log
    FOR VALUES FROM ('2026-10-01') TO ('2027-01-01');
CREATE TABLE IF NOT EXISTS system.audit_log_2027_q1 PARTITION OF system.audit_log
    FOR VALUES FROM ('2027-01-01') TO ('2027-04-01');
CREATE TABLE IF NOT EXISTS system.audit_log_2027_q2 PARTITION OF system.audit_log
    FOR VALUES FROM ('2027-04-01') TO ('2027-07-01');

CREATE INDEX IF NOT EXISTS idx_audit_farmer ON system.audit_log(farmer_id, performed_at DESC)
    WHERE farmer_id IS NOT NULL;
CREATE INDEX IF NOT EXISTS idx_audit_table ON system.audit_log(table_name, performed_at DESC);

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

CREATE OR REPLACE TRIGGER audit_farmers
    AFTER INSERT OR UPDATE OR DELETE ON core.farmers
    FOR EACH ROW EXECUTE FUNCTION system.audit_trigger();

CREATE OR REPLACE TRIGGER audit_fields
    AFTER INSERT OR UPDATE OR DELETE ON core.fields
    FOR EACH ROW EXECUTE FUNCTION system.audit_trigger();

CREATE TABLE IF NOT EXISTS system.api_rate_limits (
    farmer_id       UUID NOT NULL REFERENCES core.farmers(id) ON DELETE CASCADE,
    window_start    TIMESTAMPTZ NOT NULL,
    window_minutes  INT NOT NULL DEFAULT 60,
    request_count   INT NOT NULL DEFAULT 1,
    max_allowed     INT NOT NULL DEFAULT 100,
    is_limited      BOOLEAN GENERATED ALWAYS AS (request_count >= max_allowed) STORED,
    PRIMARY KEY (farmer_id, window_start)
);

CREATE INDEX IF NOT EXISTS idx_rate_limit_farmer ON system.api_rate_limits(farmer_id, window_start DESC);

-- REALTIME AUTOMATION TRIGGERS
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

CREATE OR REPLACE TRIGGER trg_update_session_stats
    AFTER INSERT ON agents.advisory_messages
    FOR EACH ROW EXECUTE FUNCTION agents.update_session_stats();

CREATE OR REPLACE FUNCTION alerts.notify_new_alert()
RETURNS TRIGGER AS $$
BEGIN
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

CREATE OR REPLACE TRIGGER trg_notify_alert
    AFTER INSERT ON alerts.farmer_alerts
    FOR EACH ROW EXECUTE FUNCTION alerts.notify_new_alert();

CREATE OR REPLACE FUNCTION agents.update_farmer_activity()
RETURNS TRIGGER AS $$
BEGIN
    IF NEW.role = 'user' THEN
        UPDATE core.farmers SET last_active_at = NOW() WHERE id = NEW.farmer_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER trg_farmer_activity
    AFTER INSERT ON agents.advisory_messages
    FOR EACH ROW EXECUTE FUNCTION agents.update_farmer_activity();

CREATE OR REPLACE FUNCTION realtime.auto_market_recommendation()
RETURNS TRIGGER AS $$
DECLARE
    price_7d_ago NUMERIC(10,2);
    price_30d_ago NUMERIC(10,2);
    trend TEXT;
    pct_change FLOAT;
BEGIN
    SELECT modal_price INTO price_7d_ago FROM realtime.market_prices
    WHERE crop_name = NEW.crop_name AND state = NEW.state
      AND price_date = NEW.price_date - 7
    LIMIT 1;

    SELECT modal_price INTO price_30d_ago FROM realtime.market_prices
    WHERE crop_name = NEW.crop_name AND state = NEW.state
      AND price_date = NEW.price_date - 30
    LIMIT 1;

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

CREATE OR REPLACE TRIGGER trg_auto_market_rec
    AFTER INSERT ON realtime.market_prices
    FOR EACH ROW EXECUTE FUNCTION realtime.auto_market_recommendation();


-- ============================================================
-- PHASE 8 — SEED DATA
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
('Odisha', 'Cuttack',     'alluvial',     6.0, 7.5, 'high',   'medium', 'medium', 'high',   'high',   'moderate', 1550, ARRAY['rice','jute','sugarcane','vegetables'],             'eastern_plateau_hills')
ON CONFLICT (state, district) DO UPDATE SET
    primary_texture = EXCLUDED.primary_texture,
    ph_min = EXCLUDED.ph_min,
    ph_max = EXCLUDED.ph_max,
    suitable_crops = EXCLUDED.suitable_crops;

-- MSP REFERENCE DATA
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
('wheat',       'rabi',   '2025-26', 2425.00, '2025-11-01'),
('mustard',     'rabi',   '2025-26', 5950.00, '2025-11-01'),
('gram',        'rabi',   '2025-26', 5650.00, '2025-11-01'),
('lentil',      'rabi',   '2025-26', 6700.00, '2025-11-01'),
('safflower',   'rabi',   '2025-26', 5940.00, '2025-11-01'),
('sunflower',   'rabi',   '2025-26', 7280.00, '2025-11-01'),
('barley',      'rabi',   '2025-26', 1850.00, '2025-11-01')
ON CONFLICT (crop_name, season, msp_year) DO UPDATE SET
    msp_per_quintal = EXCLUDED.msp_per_quintal;


-- ============================================================
-- MASTER ADVANCED ENHANCEMENTS (ARCHITECTURAL INNOVATIONS)
-- ============================================================

-- 1. Hybrid Search Function (pgvector + pg_trgm BM25-style keyword weighting)
CREATE OR REPLACE FUNCTION agents.retrieve_kau_docs_hybrid(
    query_text          TEXT,
    query_embedding     vector(1024),
    filter_crop         TEXT DEFAULT NULL,
    filter_org          TEXT DEFAULT NULL,
    top_k               INT DEFAULT 5,
    vector_weight       FLOAT DEFAULT 0.7,
    text_weight         FLOAT DEFAULT 0.3
) RETURNS TABLE (
    id                  UUID,
    content             TEXT,
    source_file         TEXT,
    crop_name           TEXT,
    vector_similarity   FLOAT,
    text_similarity     FLOAT,
    combined_score      FLOAT
) AS $$
BEGIN
    RETURN QUERY
    SELECT
        kd.id,
        kd.content,
        kd.source_file,
        kd.crop_name,
        (1 - (kd.embedding <=> query_embedding))::FLOAT AS vector_similarity,
        similarity(kd.content, query_text)::FLOAT AS text_similarity,
        (
            (vector_weight * (1 - (kd.embedding <=> query_embedding))) +
            (text_weight * similarity(kd.content, query_text))
        )::FLOAT AS combined_score
    FROM agents.kau_documents kd
    WHERE
        (filter_crop IS NULL OR kd.crop_name = filter_crop)
        AND (filter_org IS NULL OR kd.source_org = filter_org)
    ORDER BY combined_score DESC
    LIMIT top_k;
END;
$$ LANGUAGE plpgsql;

-- 2. Automated Monthly Partition Maintenance
CREATE OR REPLACE FUNCTION system.maintain_monthly_partitions()
RETURNS VOID AS $$
DECLARE
    next_month DATE := DATE_TRUNC('month', NOW() + INTERVAL '1 month');
BEGIN
    PERFORM realtime.create_market_partition(next_month);
    PERFORM agents.create_message_partition(next_month);
END;
$$ LANGUAGE plpgsql;

-- GIN Trigram Indexes for Fast Full-Text & Vernacular Querying
CREATE INDEX IF NOT EXISTS idx_kau_content_trgm ON agents.kau_documents USING GIN(content gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_farmers_name_trgm ON core.farmers USING GIN(name gin_trgm_ops);
CREATE INDEX IF NOT EXISTS idx_observations_native_trgm ON intelligence.field_observations USING GIN(description_native gin_trgm_ops);

-- ============================================================
-- END OF INITIALIZATION SCRIPT
-- ============================================================
