# AGRI-SAGE — DATA MODEL

## PostgreSQL 16 + pgvector 0.4.0

## Extensions (run first)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS postgis;

## Migration Order
001_extensions→002_users→003_farms→004_crop_cycles→005_observations
→006_weather→007_diagnoses→008_advisories→009_interventions→010_simulation
→011_knowledge→012_schemes→013_market→014_notifications→015_expert→016_audit→017_rls

## Key Tables

### users
id UUID PK | phone VARCHAR(15) UNIQUE NOT NULL | name VARCHAR(100)
language VARCHAR(10) DEFAULT 'ml' | subscription_tier VARCHAR(20) DEFAULT 'free'
subscription_expires TIMESTAMPTZ | advisories_this_month INT DEFAULT 0
is_active BOOLEAN DEFAULT true | created_at TIMESTAMPTZ DEFAULT NOW()

### farms
id UUID PK | user_id UUID FK→users CASCADE | name VARCHAR(200) NOT NULL
location GEOMETRY(POINT,4326) | district VARCHAR(100) | state VARCHAR(100)
area_ha DECIMAL(8,2) | INDEX idx_farms_user ON farms(user_id)

### crop_cycles
id UUID PK | field_id UUID FK→fields CASCADE | crop VARCHAR(50) NOT NULL
cultivar VARCHAR(100) | planting_date DATE NOT NULL
status VARCHAR(20) DEFAULT 'active' CHECK IN('active','harvested','abandoned')

### observations
id UUID PK | crop_cycle_id UUID FK→crop_cycles CASCADE
problem_description TEXT | voice_note_key VARCHAR(500)
observed_growth_stage VARCHAR(50) | observed_at TIMESTAMPTZ DEFAULT NOW()

### images
id UUID PK | observation_id UUID FK→observations CASCADE
r2_key VARCHAR(500) UNIQUE | mime_type VARCHAR(50)
quality_score DECIMAL(4,2) CHECK BETWEEN 0 AND 1 | blur_score DECIMAL(8,2)

### advisories
id UUID PK | observation_id UUID FK→observations CASCADE
confidence_state VARCHAR(30) NOT NULL | recommended_scenario VARCHAR(5)
scenarios_json JSONB NOT NULL | evidence_bundle_json JSONB NOT NULL
recommended_action_json JSONB NOT NULL | safe_to_act BOOLEAN DEFAULT true
sources_json JSONB | generation_ms INTEGER

### knowledge_chunks
id UUID PK | document_id UUID FK→knowledge_documents CASCADE
chunk_index INTEGER | content TEXT | embedding vector(1024) | metadata JSONB
UNIQUE(document_id, chunk_index)
-- HNSW index (pgvector 0.4.0):
CREATE INDEX idx_chunks_embedding ON knowledge_chunks
    USING hnsw (embedding vector_cosine_ops) WITH (m=16, ef_construction=64);

### schemes
id UUID PK | name VARCHAR(300) | authority VARCHAR(200)
crops_applicable JSONB | eligibility_rules JSONB NOT NULL
valid_until DATE NOT NULL | status VARCHAR(20) DEFAULT 'active'

## RLS (migration 017 — runs LAST)
ALTER TABLE farms ENABLE ROW LEVEL SECURITY;
CREATE POLICY farms_owner ON farms
    USING (user_id = current_setting('app.current_user_id')::UUID);
-- Apply same pattern to: fields, crop_cycles, observations, images, advisories, notifications

## Android Room Entities
FarmerEntity | FarmEntity | FieldEntity | CropCycleEntity
ObservationEntity | ImageEntity | CachedAdvisoryEntity
WeatherCacheEntity | SyncQueueEntity(priority INT, retryCount INT)
