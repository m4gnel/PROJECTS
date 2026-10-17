# AGRI-SAGE — MASTER BUILD PROMPTS
## Step-by-Step AI Prompts for Gemini / Cline / Cursor
### World-Class Agricultural AI Platform — Complete Build Guide

---

> **HOW TO USE THIS FILE**
> - Give ONE prompt at a time to the AI
> - Wait for it to finish completely before giving the next prompt
> - Verify each prompt's output works before moving on
> - Never skip a prompt — each one depends on the previous
> - These prompts are ordered: Foundation → Backend → Agents → Android → Data → QA → Launch

---

## CONTEXT BLOCK — PASTE THIS AT THE TOP OF EVERY SINGLE PROMPT SESSION

```
AGRI-SAGE PROJECT CONTEXT (read before executing any task):

Project: Agri-SAGE (Scalable Agricultural Guidance Engine)
Purpose: Professional agricultural AI decision platform for India's 146 million smallholder farmers
Stack: FastAPI + PostgreSQL + pgvector + LangGraph + Android Kotlin + Jetpack Compose
Cost: 100% free — no paid APIs, no paid tools, no exceptions
Demo Deadline: October 1, 2026 — 50% implementation required

EXACT PACKAGE VERSIONS — USE THESE, NO OTHERS:
Backend: fastapi==0.115.0 | uvicorn[standard]==0.34.0 | sqlalchemy[asyncio]==2.0.36
         asyncpg==0.30.0 | alembic==1.14.0 | pgvector==0.4.0
         pydantic==2.11.0 | pydantic-settings==2.7.0 | httpx==0.28.0
         python-jose[cryptography]==3.3.0 | passlib[bcrypt]==1.7.4
         python-multipart==0.0.18 | structlog==24.4.0
         sentence-transformers==3.3.0 | onnxruntime==1.20.0
         torch==2.5.1 | torchvision==0.20.1 | langgraph==1.0.8
         PyMuPDF==1.24.0 | beautifulsoup4==4.12.3 | Pillow==11.0.0
         python-magic==0.4.27 | boto3==1.35.0 | firebase-admin==6.6.0
         apscheduler==3.10.4 | razorpay==1.4.2
         pytest==8.3.0 | pytest-asyncio==0.24.0

Android: kotlin=2.0.21 | ksp=2.0.21-1.0.28 | compose-bom=2024.12.01
         navigation-compose=2.8.5 | room=2.7.0 (KSP not kapt)
         hilt=2.53 | camerax=1.4.0 | onnxruntime-android=1.20.0
         work-runtime-ktx=2.10.0 | retrofit=2.11.0 | coil-compose=2.7.0

CRITICAL API RULES:
- LangGraph 1.0.8: from langgraph.graph import StateGraph, START, END
  from langgraph.checkpoint.memory import MemorySaver
  builder.compile(checkpointer=MemorySaver())
- FastAPI 0.115.0: use @asynccontextmanager lifespan — NOT on_startup/on_shutdown
- sentence-transformers 3.3.0: encode(f'query: {text}', normalize_embeddings=True, convert_to_numpy=True)
- pgvector 0.4.0: USING hnsw WITH (m=16, ef_construction=64) — NOT IVFFlat
- Pillow 11.0.0: Image.Resampling.LANCZOS — NOT Image.LANCZOS
- Room 2.7.0: ksp("androidx.room:room-compiler:2.7.0") — NOT kapt

SAFETY RULES (never violate):
1. Never invent pesticide or chemical product names
2. Never recommend treatment when confidence is UNCERTAIN/INSUFFICIENT_DATA/CONFLICTING_EVIDENCE
3. All simulation output must carry label "modelled estimate"
4. Never say farmer IS eligible for scheme — say "appears to meet listed criteria"
5. All LLM output validated against Pydantic schema before reaching farmer
6. All 500 errors return only: {"detail": "Internal server error"}
```

---

# PHASE 0 — FOUNDATION

---

## PROMPT P0-01: Project Structure

```
You are building Agri-SAGE, a world-class agricultural AI platform for India's smallholder farmers.

TASK: Create the complete project directory structure and all configuration files.

Create exactly this folder structure (use mkdir -p for all paths):
agrisage/
├── backend/
│   ├── api/v1/
│   ├── agents/
│   ├── models/db/
│   ├── models/schemas/
│   ├── services/
│   ├── simulation/
│   ├── knowledge/
│   ├── ml/vision/
│   ├── safety/
│   └── data/
├── mobile/android/
├── tests/
│   ├── unit/
│   ├── integration/
│   ├── safety/
│   ├── performance/
│   └── golden/
├── scripts/
├── alembic/
├── brain/
├── docs/
├── apps/web-expert/
└── .github/workflows/

CREATE FILE: .gitignore
Content:
node_modules/
.next/
out/
.env
.env.local
.DS_Store
*.log
__pycache__/
*.pyc
*.pyo
*.onnx
*.pt
.vercel/
venv/
.venv/
*.egg-info/
dist/
build/
*.so
.pytest_cache/
htmlcov/
.coverage

CREATE FILE: .env.example
Content (all values empty — developer fills these in):
DATABASE_URL=
SECRET_KEY=
ENVIRONMENT=development
CORS_ORIGINS=["http://localhost:3000"]
R2_BUCKET=
R2_ACCESS_KEY=
R2_SECRET_KEY=
R2_ACCOUNT_ID=
FCM_KEY=
BHASHINI_API_KEY=
OTP_PROVIDER_KEY=
WEATHER_PROVIDER=open_meteo
GEMINI_API_KEY=
OLLAMA_URL=http://localhost:11434
MAX_IMAGE_SIZE_MB=5
MODEL_VERSION=v1.0.0
KNOWLEDGE_VERSION=2026-09-01
LOG_LEVEL=INFO
DSSAT_BIN_PATH=/usr/local/bin/dscsm048

CREATE FILE: README.md
Content:
# Agri-SAGE — Scalable Agricultural Guidance Engine
Agricultural AI decision platform for India's 146 million smallholder farmers.
14 AI agents. Real-time disease diagnosis. Malayalam. Works offline.

## Team
- Member 1: Team Lead & Backend (dev/m1-backend)
- Member 2: AI Agent Developer (dev/m2-agents)
- Member 3: Android Developer (dev/m3-android)
- Member 4: Data & Knowledge (dev/m4-data)
- Member 5: QA & DevOps (dev/m5-tests)

## Quick Start
cp .env.example .env
docker compose up -d
alembic upgrade head
uvicorn backend.main:app --reload

CREATE FILE: LICENSE_REGISTRY.md
Content:
# Agri-SAGE — Dependency License Registry
| Package | License | Commercial Use | Notes |
|---------|---------|---------------|-------|
| FastAPI | MIT | YES | |
| PostgreSQL | PostgreSQL License | YES | |
| pgvector | MIT | YES | |
| LangGraph | MIT | YES | |
| PyTorch | BSD-3-Clause | YES | |
| ONNX Runtime | MIT | YES | |
| DSSAT | BSD-3-Clause | YES | Free for all use |
| Open-Meteo | CC BY 4.0 | NON-COMMERCIAL ONLY | Switch to IMD before monetization |
| APSIM | APSIM Non-Commercial | NON-COMMERCIAL ONLY | Do NOT use — use DSSAT instead |
| multilingual-e5-large | MIT | YES | |
| Cloudflare R2 | Commercial SaaS | YES | Free tier: 10GB |
| Firebase FCM | Google Terms | YES | Free tier available |

AFTER CREATING ALL FILES:
Show me the directory tree.
Confirm .gitignore includes .env.
Confirm LICENSE_REGISTRY.md warns about Open-Meteo commercial restriction.
```

---

## PROMPT P0-02: Docker and Requirements

```
Agri-SAGE project. Foundation phase.

TASK: Create Docker environment and Python requirements.

CREATE FILE: docker-compose.yml
Content:
version: '3.9'
services:
  db:
    image: pgvector/pgvector:pg16
    environment:
      POSTGRES_DB: agrisage_dev
      POSTGRES_USER: agrisage
      POSTGRES_PASSWORD: ${DB_PASSWORD:-devpassword}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U agrisage"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build: .
    ports:
      - "8000:8000"
    env_file: .env
    depends_on:
      db:
        condition: service_healthy
    volumes:
      - .:/app
    command: uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload

volumes:
  postgres_data:

CREATE FILE: Dockerfile
Content:
FROM python:3.11-slim
RUN apt-get update && apt-get install -y \
    build-essential libpq-dev libmagic1 libgdal-dev \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]

CREATE FILE: backend/requirements.txt
Content — use EXACT versions, no changes:
fastapi==0.115.0
uvicorn[standard]==0.34.0
sqlalchemy[asyncio]==2.0.36
asyncpg==0.30.0
alembic==1.14.0
pgvector==0.4.0
pydantic==2.11.0
pydantic-settings==2.7.0
httpx==0.28.0
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.18
structlog==24.4.0
sentence-transformers==3.3.0
onnxruntime==1.20.0
torch==2.5.1
torchvision==0.20.1
langgraph==1.0.8
PyMuPDF==1.24.0
beautifulsoup4==4.12.3
Pillow==11.0.0
python-magic==0.4.27
boto3==1.35.0
firebase-admin==6.6.0
apscheduler==3.10.4
razorpay==1.4.2
pytest==8.3.0
pytest-asyncio==0.24.0
bandit==1.8.0
pip-audit==2.8.0
cross-encoder==0.1.0

VERIFY: Show docker-compose.yml and requirements.txt in full.
```

---

## PROMPT P0-03: FastAPI App Core

```
Agri-SAGE project. Foundation phase.

TASK: Create the FastAPI application core — config, database, and main app.

CREATE FILE: backend/config.py
Use pydantic-settings 2.7.0 with SettingsConfigDict. Include ALL fields from .env.example.
CORS_ORIGINS must be List[str].
Export: settings = Settings()
Use model_config = SettingsConfigDict(env_file='.env', case_sensitive=False, extra='ignore')

CREATE FILE: backend/database.py
- Async SQLAlchemy engine from settings.DATABASE_URL
- AsyncSessionLocal sessionmaker
- Base = declarative_base()
- async get_db() dependency — yields AsyncSession, closes after use
- async check_db_connection() — runs SELECT 1, returns bool

CREATE FILE: backend/main.py
Rules:
- Use @asynccontextmanager lifespan (NOT on_startup) — FastAPI 0.115.0 requirement
- Lifespan startup: log app start, check DB connection
- Lifespan shutdown: dispose engine
- Add CORSMiddleware with origins=settings.CORS_ORIGINS, allow_credentials=True, allow_methods=["*"], allow_headers=["*"]
- Add structlog middleware: log every request with method, path, status_code, process_time_ms — NEVER log Authorization header values or passwords
- GET /health endpoint: returns {"status": "ok", "version": settings.MODEL_VERSION, "environment": settings.ENVIRONMENT, "db_connected": bool}
- Global exception handler for all unhandled exceptions: return JSONResponse(status_code=500, content={"detail": "Internal server error"}) — NEVER expose stack traces or error details
- Include all routers with prefix /api/v1 (create empty placeholder routers for now: auth, farms, observations, diagnose, weather, risk, schemes, markets, simulate, notifications, sync)

CREATE FILE: backend/dependencies.py
- require_auth async dependency:
  - Extract Bearer token from Authorization header
  - Decode JWT with python-jose, algorithm HS256, settings.SECRET_KEY
  - Validate exp claim — raise HTTPException(401) if expired
  - Extract user_id from sub claim
  - Run: await db.execute(text(f"SET LOCAL app.current_user_id = '{user_id}'"))
  - Return decoded payload dict
  - On ANY failure: raise HTTPException(status_code=401, detail="Invalid or expired token")

VERIFY: Show backend/main.py in full. Confirm lifespan pattern is used, not on_startup.
```

---

## PROMPT P0-04: Database Migrations

```
Agri-SAGE project. Foundation phase.

TASK: Set up Alembic and create all 17 database migrations.

STEP 1: Run alembic init alembic in project root.

STEP 2: Configure alembic/env.py:
- Import settings from backend.config
- Import Base from backend.database
- Set target_metadata = Base.metadata
- Use async engine pattern with run_sync

STEP 3: Create these 17 migration files in alembic/versions/ in this exact order:

001_extensions.py — Execute raw SQL:
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS postgis;

002_users.py — Create users table:
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    phone VARCHAR(15) UNIQUE NOT NULL,
    name VARCHAR(100),
    language VARCHAR(10) NOT NULL DEFAULT 'ml',
    location_lat DECIMAL(9,6), location_lon DECIMAL(9,6),
    district VARCHAR(100), state VARCHAR(100) DEFAULT 'Kerala',
    subscription_tier VARCHAR(20) NOT NULL DEFAULT 'free',
    subscription_expires TIMESTAMPTZ,
    trial_started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    advisories_this_month INT NOT NULL DEFAULT 0,
    advisories_reset_at DATE NOT NULL DEFAULT CURRENT_DATE,
    is_active BOOLEAN NOT NULL DEFAULT true,
    fcm_token VARCHAR(500),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    last_active_at TIMESTAMPTZ
);
CREATE INDEX idx_users_phone ON users(phone);

003_farms.py — Create farms and fields tables:
CREATE TABLE farms (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    name VARCHAR(200) NOT NULL,
    location_lat DECIMAL(9,6), location_lon DECIMAL(9,6),
    district VARCHAR(100), state VARCHAR(100),
    area_ha DECIMAL(8,2),
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_farms_user ON farms(user_id);

CREATE TABLE fields (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    farm_id UUID NOT NULL REFERENCES farms(id) ON DELETE CASCADE,
    name VARCHAR(100),
    area_ha DECIMAL(8,2), slope VARCHAR(20),
    irrigation VARCHAR(30), soil_type VARCHAR(50),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_fields_farm ON fields(farm_id);

004_crop_cycles.py:
CREATE TABLE crop_cycles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    field_id UUID NOT NULL REFERENCES fields(id) ON DELETE CASCADE,
    crop VARCHAR(50) NOT NULL CHECK (crop IN ('rice','banana','coconut','tomato','maize')),
    cultivar VARCHAR(100), season VARCHAR(20),
    planting_date DATE NOT NULL,
    expected_harvest DATE, actual_harvest DATE,
    status VARCHAR(20) NOT NULL DEFAULT 'active'
        CHECK (status IN ('active','harvested','abandoned')),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_cycles_field ON crop_cycles(field_id);

005_observations.py:
CREATE TABLE observations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_cycle_id UUID NOT NULL REFERENCES crop_cycles(id) ON DELETE CASCADE,
    location_lat DECIMAL(9,6), location_lon DECIMAL(9,6),
    problem_description TEXT,
    voice_note_key VARCHAR(500),
    irrigation_status VARCHAR(20),
    fertilizer_recent BOOLEAN, pesticide_recent BOOLEAN,
    observed_growth_stage VARCHAR(50),
    observed_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_obs_cycle ON observations(crop_cycle_id);

CREATE TABLE images (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    observation_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
    r2_key VARCHAR(500) NOT NULL UNIQUE,
    mime_type VARCHAR(50) NOT NULL,
    file_size_bytes INTEGER, width_px INTEGER, height_px INTEGER,
    quality_score DECIMAL(4,2) CHECK (quality_score BETWEEN 0 AND 1),
    blur_score DECIMAL(8,2),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_images_obs ON images(observation_id);

006_weather.py:
CREATE TABLE weather_cache (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    location_key VARCHAR(20) NOT NULL UNIQUE,
    data_json JSONB NOT NULL,
    cached_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

007_diagnoses.py:
CREATE TABLE diagnoses (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    observation_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
    pipeline_trace_id VARCHAR(100),
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    generation_ms INTEGER,
    model_version VARCHAR(50),
    status VARCHAR(20) DEFAULT 'pending'
);

008_advisories.py:
CREATE TABLE advisories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    observation_id UUID NOT NULL REFERENCES observations(id) ON DELETE CASCADE,
    confidence_state VARCHAR(30) NOT NULL
        CHECK (confidence_state IN ('CONFIRMED','LIKELY','POSSIBLE','UNCERTAIN',
               'INSUFFICIENT_DATA','CONFLICTING_EVIDENCE','OUT_OF_SCOPE')),
    confidence_score DECIMAL(4,2),
    recommended_scenario VARCHAR(5),
    scenarios_json JSONB NOT NULL,
    evidence_bundle_json JSONB NOT NULL,
    recommended_action_json JSONB NOT NULL,
    what_would_change_json JSONB,
    safe_to_act BOOLEAN NOT NULL DEFAULT true,
    sources_json JSONB,
    scheme_matches_json JSONB,
    model_version VARCHAR(50),
    knowledge_version VARCHAR(50),
    generation_ms INTEGER,
    farmer_feedback VARCHAR(20),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_adv_obs ON advisories(observation_id);
CREATE INDEX idx_adv_created ON advisories(created_at DESC);

009_interventions.py:
CREATE TABLE interventions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop_cycle_id UUID NOT NULL REFERENCES crop_cycles(id),
    advisory_id UUID REFERENCES advisories(id),
    intervention_type VARCHAR(50) NOT NULL,
    product_name VARCHAR(200), dosage VARCHAR(100),
    cost_inr DECIMAL(10,2), applied_at DATE,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE outcomes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    intervention_id UUID NOT NULL REFERENCES interventions(id),
    observed_at DATE NOT NULL,
    effectiveness VARCHAR(20),
    yield_actual_kgha DECIMAL(10,2),
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

010_simulation.py:
CREATE TABLE simulation_results (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    advisory_id UUID NOT NULL REFERENCES advisories(id),
    engine VARCHAR(20) DEFAULT 'dssat',
    scenario_id VARCHAR(5),
    params_json JSONB, results_json JSONB,
    yield_kgha DECIMAL(10,2), net_return_inr DECIMAL(12,2),
    is_modelled_estimate BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

011_knowledge.py:
CREATE TABLE knowledge_documents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(500), crop VARCHAR(50), state VARCHAR(100),
    topic VARCHAR(100), growth_stage VARCHAR(50),
    source_tier INTEGER NOT NULL CHECK (source_tier BETWEEN 1 AND 6),
    source_authority VARCHAR(200), source_url VARCHAR(1000),
    language VARCHAR(10) NOT NULL DEFAULT 'en',
    published_at DATE, valid_until DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'PUBLISHED'
        CHECK (status IN ('DISCOVERED','PARSED','VALIDATED','APPROVED',
               'PUBLISHED','SUPERSEDED','ARCHIVED')),
    content_hash CHAR(64), version INTEGER NOT NULL DEFAULT 1,
    license VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE knowledge_chunks (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    document_id UUID NOT NULL REFERENCES knowledge_documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(1024),
    metadata JSONB,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE(document_id, chunk_index)
);
-- HNSW index — pgvector 0.4.0 — NOT IVFFlat
CREATE INDEX idx_chunks_embedding ON knowledge_chunks
    USING hnsw (embedding vector_cosine_ops)
    WITH (m=16, ef_construction=64);

012_schemes.py:
CREATE TABLE schemes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(300) NOT NULL, short_name VARCHAR(50),
    authority VARCHAR(200), authority_level VARCHAR(20),
    state VARCHAR(100), crops_applicable JSONB,
    eligibility_rules JSONB NOT NULL, benefits_json JSONB,
    enrollment_url VARCHAR(500), helpline VARCHAR(50),
    valid_from DATE, valid_until DATE NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

013_market.py:
CREATE TABLE market_prices (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    crop VARCHAR(50) NOT NULL, variety VARCHAR(100),
    market_name VARCHAR(200), district VARCHAR(100), state VARCHAR(100),
    price_min_inr DECIMAL(10,2), price_max_inr DECIMAL(10,2),
    price_modal_inr DECIMAL(10,2),
    recorded_date DATE NOT NULL,
    source VARCHAR(100) DEFAULT 'enam',
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_market_crop_date ON market_prices(crop, recorded_date DESC);

014_notifications.py:
CREATE TABLE notifications (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL,
    title VARCHAR(300), body TEXT,
    data_json JSONB, is_read BOOLEAN DEFAULT false,
    sent_at TIMESTAMPTZ, read_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_notif_user ON notifications(user_id, created_at DESC);

015_expert.py:
CREATE TABLE expert_reviews (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    advisory_id UUID NOT NULL REFERENCES advisories(id),
    expert_id UUID NOT NULL REFERENCES users(id),
    verdict VARCHAR(20) CHECK (verdict IN ('correct','partially_correct','incorrect','insufficient_data')),
    notes TEXT, corrected_diagnosis VARCHAR(100),
    reviewed_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

016_audit.py:
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id),
    event_type VARCHAR(100) NOT NULL,
    event_data JSONB,
    ip_address INET,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
CREATE INDEX idx_audit_type_date ON audit_logs(event_type, created_at DESC);

017_rls.py — Row Level Security (MUST run last):
ALTER TABLE farms ENABLE ROW LEVEL SECURITY;
ALTER TABLE fields ENABLE ROW LEVEL SECURITY;
ALTER TABLE crop_cycles ENABLE ROW LEVEL SECURITY;
ALTER TABLE observations ENABLE ROW LEVEL SECURITY;
ALTER TABLE images ENABLE ROW LEVEL SECURITY;
ALTER TABLE advisories ENABLE ROW LEVEL SECURITY;
ALTER TABLE notifications ENABLE ROW LEVEL SECURITY;

CREATE POLICY farms_owner ON farms
    USING (user_id = current_setting('app.current_user_id')::UUID);
CREATE POLICY fields_owner ON fields
    USING (farm_id IN (SELECT id FROM farms WHERE user_id = current_setting('app.current_user_id')::UUID));
CREATE POLICY cycles_owner ON crop_cycles
    USING (field_id IN (SELECT f.id FROM fields f JOIN farms fa ON f.farm_id=fa.id WHERE fa.user_id = current_setting('app.current_user_id')::UUID));
CREATE POLICY obs_owner ON observations
    USING (crop_cycle_id IN (SELECT cc.id FROM crop_cycles cc JOIN fields f ON cc.field_id=f.id JOIN farms fa ON f.farm_id=fa.id WHERE fa.user_id = current_setting('app.current_user_id')::UUID));
CREATE POLICY adv_owner ON advisories
    USING (observation_id IN (SELECT o.id FROM observations o JOIN crop_cycles cc ON o.crop_cycle_id=cc.id JOIN fields f ON cc.field_id=f.id JOIN farms fa ON f.farm_id=fa.id WHERE fa.user_id = current_setting('app.current_user_id')::UUID));
CREATE POLICY notif_owner ON notifications
    USING (user_id = current_setting('app.current_user_id')::UUID);

VERIFY: List all 17 migration files. Run alembic upgrade head on test DB. Confirm all tables created.
```

---

## PROMPT P0-05: Auth Endpoints

```
Agri-SAGE project. Foundation phase.

TASK: Implement complete authentication system.

CREATE FILE: backend/services/jwt_service.py
- create_access_token(user_id: str, subscription_tier: str) → str
  Algorithm: HS256, expiry: 15 minutes, include: sub, tier, exp, iat, jti=uuid4()
- create_refresh_token(user_id: str) → tuple[str, str]
  Returns (raw_token, hashed_token). Hash with SHA-256. Expiry: 7 days.
- verify_access_token(token: str) → dict — decode and return payload

CREATE FILE: backend/api/v1/auth.py
Four endpoints:

POST /api/v1/auth/send-otp
Input: {phone: str} — validate E.164 format (+91XXXXXXXXXX or country code)
Logic:
  1. Check rate limit: max 5 OTP requests per phone per 10 minutes (query otp_sessions table)
  2. If over limit: raise HTTPException(429, "Too many OTP requests")
  3. Generate OTP: str(secrets.randbelow(1000000)).zfill(6)
  4. Hash OTP: passlib bcrypt, rounds=10
  5. Delete any existing unexpired OTP for this phone
  6. Insert into otp_sessions: {phone, otp_hash, expires_at=now+300s, attempts=0, used=false}
  7. In DEVELOPMENT environment (settings.ENVIRONMENT == 'development'): print OTP to console
  8. In PRODUCTION: call MSG91 API (if OTP_PROVIDER_KEY set) else log warning
  9. Return: {"message": "OTP sent", "expires_in": 300}

POST /api/v1/auth/verify-otp
Input: {phone: str, otp: str}
Logic:
  1. Find most recent unused unexpired otp_session for phone
  2. If not found: raise HTTPException(401, "Invalid or expired OTP")
  3. If session.attempts >= 5: raise HTTPException(401, "Too many failed attempts")
  4. Increment attempts
  5. Verify bcrypt hash — if mismatch: save incremented attempts, raise HTTPException(401, "Invalid OTP")
  6. Mark session used=true
  7. Get or create user by phone (upsert)
  8. Generate access token + refresh token pair
  9. Store refresh token hash in refresh_tokens table with expires_at=now+7days
  10. Return: {"access_token": str, "refresh_token": str, "user": {id, phone, name, language, subscription_tier}}

POST /api/v1/auth/refresh
Input: {refresh_token: str}
Logic:
  1. Hash incoming token with SHA-256
  2. Find in refresh_tokens: must exist, NOT revoked, expires_at > NOW()
  3. If not found: raise HTTPException(401, "Invalid refresh token")
  4. Mark old token revoked=true BEFORE issuing new one
  5. Generate new access + refresh token pair
  6. Store new refresh token hash
  7. Return new token pair

POST /api/v1/auth/logout
Input: {refresh_token: str}
Logic:
  1. Hash token
  2. Find in refresh_tokens and mark revoked=true
  3. Return: {"message": "Logged out"}

Add otp_sessions and refresh_tokens tables to migration 002 or create a new 002b migration.

VERIFY: Test POST /auth/send-otp in development mode — OTP must print to console. Test verify-otp returns JWT.
```

---

## PROMPT P0-06: Farm CRUD and Image Upload

```
Agri-SAGE project. Backend phase.

TASK: Implement Farm, Field, CropCycle CRUD and secure image upload.

CREATE FILE: backend/models/db/farms.py
SQLAlchemy ORM models matching migration tables exactly:
- UserModel, FarmModel, FieldModel, CropCycleModel
- Use relationship() for associations
- All column types must match migration SQL exactly

CREATE FILE: backend/models/schemas/farms.py
Pydantic v2 schemas with field_validator for string sanitization:
- FarmCreate, FarmResponse, FieldCreate, FieldResponse
- CropCycleCreate, CropCycleResponse
- String sanitizer: strip HTML tags with re.sub(r'<[^>]+>','',v)
  and control chars with re.sub(r'[\x00-\x1f\x7f]','',v)

CREATE FILE: backend/services/image_security.py
process_uploaded_image(file_bytes: bytes) -> bytes:
  1. Check size: if len(file_bytes) > 5*1024*1024: raise ValueError("Too large")
  2. Check MIME from CONTENT (not filename): use python-magic
     Allowed: image/jpeg, image/png, image/webp only
     If not allowed: raise ValueError(f"Not allowed: {mime}")
  3. Open with Pillow and verify (detects corrupt images)
  4. Strip ALL EXIF metadata by recreating image:
     clean = Image.new(img.mode, img.size)
     clean.putdata(list(img.getdata()))
  5. Resize if > 1200px: clean.thumbnail((1200,1200), Image.Resampling.LANCZOS)
  6. Save as JPEG quality=85, optimize=True
  7. Return output bytes

CREATE FILE: backend/services/storage.py
R2StorageService using boto3:
- endpoint_url = f"https://{settings.R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
- async upload_image(file_bytes: bytes, object_key: str) -> str (returns public URL)
- async delete_image(object_key: str)
- async generate_signed_url(object_key: str, expires_seconds=3600) -> str

CREATE FILE: backend/api/v1/farms.py
All endpoints require require_auth dependency.
Before EVERY DB query: await db.execute(text(f"SET LOCAL app.current_user_id = '{user_id}'"))
Return 404 for not-found OR not-owned (RLS makes them both return empty — treat identically).

Endpoints:
POST /api/v1/farms — create farm
GET /api/v1/farms — list user's farms
GET /api/v1/farms/{id} — get farm (404 if not owned)
PUT /api/v1/farms/{id} — update farm
DELETE /api/v1/farms/{id} — soft delete (set is_active=False)
POST /api/v1/farms/{id}/fields — add field
POST /api/v1/crop-cycles — start crop cycle

CREATE FILE: backend/api/v1/observations.py
POST /api/v1/observations — multipart form:
  Fields: crop_cycle_id (str), description (str, optional, max 2000 chars)
  Files: images (List[UploadFile], max 5 files)
  Logic:
    1. Validate crop_cycle ownership via RLS
    2. For each image: call process_uploaded_image() then upload to R2
    3. Generate UUID key: f"observations/{user_id}/{observation_id}/{image_uuid}.jpg"
    4. Create observation record
    5. Create image records with r2_key
    6. Return {observation_id, image_ids: []}

VERIFY: POST /farms creates farm. GET /farms returns it.
Test RLS: GET /farms/{other_user_farm_id} must return 404.
```

---

## PROMPT P0-07: GitHub Actions CI/CD

```
Agri-SAGE project. Foundation phase.

TASK: Create complete GitHub Actions CI/CD pipeline.

CREATE FILE: .github/workflows/ci.yml
Content:
name: CI Pipeline

on:
  push:
    branches: [main, dev/*]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      db:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_DB: agrisage_test
          POSTGRES_USER: agrisage
          POSTGRES_PASSWORD: testpassword
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
        ports:
          - 5432:5432

    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r backend/requirements.txt
      - name: Run migrations
        env:
          DATABASE_URL: postgresql+asyncpg://agrisage:testpassword@localhost/agrisage_test
          SECRET_KEY: test-secret-key-ci-only
          ENVIRONMENT: test
        run: alembic upgrade head
      - name: Run tests
        env:
          DATABASE_URL: postgresql+asyncpg://agrisage:testpassword@localhost/agrisage_test
          SECRET_KEY: test-secret-key-ci-only
          ENVIRONMENT: test
        run: pytest tests/ -v --tb=short --asyncio-mode=auto

  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install black ruff
      - run: black --check backend/
      - run: ruff check backend/

  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Check hardcoded secrets
        run: |
          if grep -rn --include="*.py" --include="*.kt" \
             -E '(SECRET_KEY|API_KEY|PASSWORD)\s*=\s*"[a-zA-Z0-9+/]{20,}"' .; then
            echo "FAIL: Hardcoded secret found"
            exit 1
          fi
      - name: Verify .env not committed
        run: |
          if git ls-files --error-unmatch .env 2>/dev/null; then
            echo "FAIL: .env is tracked by git"
            exit 1
          fi
      - name: Dependency vulnerability scan
        run: |
          pip install pip-audit
          pip-audit -r backend/requirements.txt --fail-on CRITICAL
      - name: SAST scan
        run: |
          pip install bandit
          bandit -r backend/ -lll

VERIFY: Show complete ci.yml. Confirm all 3 jobs exist: test, lint, security.
```

---

# PHASE 1 — AI AGENTS

---

## PROMPT P1-01: LangGraph Orchestrator

```
Agri-SAGE project. Agent phase.

TASK: Create the LangGraph 1.0.8 orchestration system and all 14 agent stubs.

CRITICAL: Use LangGraph 1.0.8 API exactly:
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
Use builder.add_edge(START, 'node_name') — not graph.set_entry_point()
Use builder.compile(checkpointer=MemorySaver())

CREATE FILE: backend/agents/state.py
Define AgriSAGEState as TypedDict with Annotated fields:

from typing import TypedDict, Optional, Annotated
import operator

class AgriSAGEState(TypedDict):
    # Input
    observation_id: str
    user_id: str
    images: list
    farm_state: Optional[dict]
    # Agent results
    vision_result: Optional[dict]
    weather_result: Optional[dict]
    crop_stage_result: Optional[dict]
    knowledge_result: Optional[dict]
    critic_result: Optional[dict]
    scheme_result: Optional[dict]
    simulation_result: Optional[dict]
    decision_result: Optional[dict]
    advisory: Optional[dict]
    # Control
    run_simulation: bool
    confidence_state: Optional[str]
    # Accumulate warnings and errors across all agents
    warnings: Annotated[list, operator.add]
    errors: Annotated[list, operator.add]
    # Metadata
    pipeline_start_ms: Optional[int]
    generation_ms: Optional[int]
    language: str
    crop: Optional[str]

CREATE FILE: backend/agents/orchestrator.py
Build advisory graph with this EXACT pipeline:
START → intake
intake → vision (parallel)
intake → weather (parallel)
intake → crop_stage (parallel)
intake → knowledge (parallel)
[vision, weather, crop_stage, knowledge] → critic
critic → scheme (always)
critic → simulation (conditional: only if state['run_simulation'] == True)
          OR directly to decision (if run_simulation == False)
[simulation, scheme] → decision
decision → explanation
explanation → END

Add 10-second timeout wrapper around full graph execution.
Store pipeline_start_ms at graph entry.
On completion: calculate generation_ms.

CREATE STUB FILES for all 14 agents (each with class + async run(state) returning state unchanged):
backend/agents/intake.py
backend/agents/vision.py
backend/agents/weather.py
backend/agents/crop_stage.py
backend/agents/knowledge.py
backend/agents/critic.py
backend/agents/scheme.py
backend/agents/soil.py
backend/agents/decision.py
backend/agents/explanation.py
backend/agents/simulation.py
backend/agents/market.py
backend/agents/economics.py
backend/agents/monitoring.py

CREATE FILE: backend/services/llm_service.py
LLMService class:
- If settings.GEMINI_API_KEY is set: use Gemini 1.5 Pro API
  URL: https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-pro:generateContent
  Headers: ?key={GEMINI_API_KEY}
  Payload: {system_instruction: {parts:[{text:system_prompt}]}, contents:[{parts:[{text:user_prompt}]}], generationConfig:{temperature, maxOutputTokens}}
- Else: use Ollama at settings.OLLAMA_URL/api/chat
- Retry logic: on invalid JSON, append "Output ONLY valid JSON. No other text." and retry once
- After 2 failures: return None (caller uses fallback)
- Never raise exception to caller — always return dict or None
- Timeout: 25 seconds per call

VERIFY: Show orchestrator.py in full. Confirm START/END imports are from langgraph.graph.
Confirm MemorySaver is from langgraph.checkpoint.memory.
```

---

## PROMPT P1-02: Vision, Intake, Critic Agents

```
Agri-SAGE project. Agent phase.

TASK: Implement Intake, Vision, and Critic agents. No LLM calls in any of these.

FIRST: Create backend/data/disease_classes.json with this EXACT content:
[
  {"index":0,"class_name":"rice_blast","common_name":"Rice Blast","ml_name":"നെൽ ബ്ലാസ്റ്റ് രോഗം","crop":"rice"},
  {"index":1,"class_name":"rice_brown_spot","common_name":"Brown Spot","ml_name":"തവിട്ട് പുള്ളി രോഗം","crop":"rice"},
  {"index":2,"class_name":"rice_bacterial_blight","common_name":"Bacterial Blight","ml_name":"ബാക്ടീരിയൽ ഇല കരിച്ചിൽ","crop":"rice"},
  {"index":3,"class_name":"rice_sheath_blight","common_name":"Sheath Blight","ml_name":"കതിർ ആവരണ ജീർണ്ണം","crop":"rice"},
  {"index":4,"class_name":"rice_leaf_folder","common_name":"Leaf Folder","ml_name":"ഇല ചുരുട്ടി പുഴു","crop":"rice"},
  {"index":5,"class_name":"rice_healthy","common_name":"Healthy Rice","ml_name":"ആരോഗ്യകരമായ നെൽ","crop":"rice"},
  {"index":6,"class_name":"banana_fusarium","common_name":"Fusarium Wilt","ml_name":"ഫ്യൂസേറിയം വിൽറ്റ്","crop":"banana"},
  {"index":7,"class_name":"banana_sigatoka","common_name":"Sigatoka Leaf Spot","ml_name":"സിഗറ്റോക്ക ഇലപ്പുള്ളി","crop":"banana"},
  {"index":8,"class_name":"banana_bbtv","common_name":"Banana Bunchy Top Virus","ml_name":"വാഴ ബഞ്ചി ടോപ്പ് വൈറസ്","crop":"banana"},
  {"index":9,"class_name":"banana_healthy","common_name":"Healthy Banana","ml_name":"ആരോഗ്യകരമായ വാഴ","crop":"banana"},
  {"index":10,"class_name":"coconut_wclwd","common_name":"Kerala Wilt WCLWD","ml_name":"തെങ്ങ് മഞ്ഞൾ ഇല കൊഴിച്ചിൽ","crop":"coconut"},
  {"index":11,"class_name":"coconut_bud_rot","common_name":"Bud Rot","ml_name":"ഓലച്ചീർ","crop":"coconut"},
  {"index":12,"class_name":"coconut_healthy","common_name":"Healthy Coconut","ml_name":"ആരോഗ്യകരമായ തെങ്ങ്","crop":"coconut"},
  {"index":13,"class_name":"tomato_early_blight","common_name":"Early Blight","ml_name":"തക്കാളി ആദ്യ ദ്രവം","crop":"tomato"},
  {"index":14,"class_name":"tomato_late_blight","common_name":"Late Blight","ml_name":"തക്കാളി അന്ത്യ ദ്രവം","crop":"tomato"},
  {"index":15,"class_name":"tomato_leaf_curl","common_name":"Leaf Curl Virus","ml_name":"തക്കാളി ഇല ചുരുളൽ","crop":"tomato"},
  {"index":16,"class_name":"tomato_healthy","common_name":"Healthy Tomato","ml_name":"ആരോഗ്യകരമായ തക്കാളി","crop":"tomato"},
  {"index":17,"class_name":"maize_northern_blight","common_name":"Northern Leaf Blight","ml_name":"ചോളം ഇല ദ്രവം","crop":"maize"},
  {"index":18,"class_name":"maize_common_rust","common_name":"Common Rust","ml_name":"ചോളം തുരുമ്പ്","crop":"maize"},
  {"index":19,"class_name":"maize_grey_leaf_spot","common_name":"Grey Leaf Spot","ml_name":"ചോളം ചാര പുള്ളി","crop":"maize"},
  {"index":20,"class_name":"maize_healthy","common_name":"Healthy Maize","ml_name":"ആരോഗ്യകരമായ ചോളം","crop":"maize"},
  {"index":21,"class_name":"out_of_distribution","common_name":"Not a crop image","ml_name":"തിരിച്ചറിയാൻ കഴിഞ്ഞില്ല","crop":"none"}
]

IMPLEMENT backend/agents/intake.py:
- Merge raw observation data with stored farm profile from DB
- Compute: days_after_sowing = (date.today() - planting_date).days
- Normalize crop name to one of: rice, banana, coconut, tomato, maize
  If crop not recognized: set state.warnings += ["crop not normalized"]
- Flag any null required fields in state.warnings
- Return updated state with complete farm_state dict
- NO LLM call

IMPLEMENT backend/agents/vision.py:
- Load ONNX session as CLASS-LEVEL SINGLETON (load once, reuse every request)
  model_path = "backend/ml/vision_int8.onnx"
  session = ort.InferenceSession(model_path, providers=['CPUExecutionProvider'])
- Load class names from backend/data/disease_classes.json at module load
- For each image in state.images:
  Image quality checks (reject with INSUFFICIENT_DATA if fails):
    blur: compute Laplacian variance — if < 100: reject, message "Image too blurry"
    brightness: compute mean pixel value — if < 40: "Too dark", if > 220: "Too bright"
    coverage: estimate crop region coverage — if < 30%: "Move closer to the crop"
  If quality passes:
    Preprocess: resize to 300x300, normalize with ImageNet stats
    Run inference: session.run(['output'], {'input': img_array})
    Apply softmax to logits
    Get top-5 predictions with class names and scores
- Return VisionResult with: label, confidence_score, severity, affected_area_pct, top_predictions, quality_score, out_of_distribution
- NO LLM call

IMPLEMENT backend/agents/critic.py:
Assign confidence_state using these EXACT rules:
  vision.confidence > 0.80 AND dfi supports AND stage matches AND Tier1 chunk found → CONFIRMED
  vision.confidence 0.60-0.80 AND most evidence supports → LIKELY
  vision.confidence 0.40-0.60 OR minor conflict exists → POSSIBLE
  vision.confidence < 0.40 OR multiple conflicts → UNCERTAIN
  vision.out_of_distribution == True OR critical data missing → INSUFFICIENT_DATA
  Vision says disease_X AND weather DFI < 0.25 AND wet_days < 2 → CONFLICTING_EVIDENCE
  crop not in [rice,banana,coconut,tomato,maize] → OUT_OF_SCOPE

Safety blocks — if ANY block triggers, hold advisory:
  1. Product name in LLM output not found verbatim in knowledge_chunks
  2. Product not in CIB&RC database (check backend/data/chemical_labels.json if it exists, else skip)
  3. Stage mismatch: vision_label not in expected diseases for crop stage
  4. Scheme valid_until < today
  5. Image quality_score < 0.3 AND confidence > 0.85 (suspicious mismatch)

set run_simulation = True only if:
  confidence_score > 0.65 AND len(conflicts) == 0 AND confidence_state in ['CONFIRMED','LIKELY']

set safe_to_act = False if confidence_state in ['UNCERTAIN','INSUFFICIENT_DATA','CONFLICTING_EVIDENCE']
NO LLM call in critic.

VERIFY: Show critic.py in full. Confirm zero LLM calls. Show confidence_state assignment logic.
```

---

## PROMPT P1-03: Weather, CropStage, Knowledge Agents

```
Agri-SAGE project. Agent phase.

TASK: Implement Weather, CropStage, and Knowledge agents. No LLM calls.

FIRST: Create backend/data/gdd_thresholds.json with EXACT content:
{
  "base_temperatures": {"rice":10,"maize":10,"tomato":10,"banana":15,"coconut":20},
  "thresholds": {
    "rice": {
      "germination":{"gdd_from":0,"gdd_to":50,"vulnerability":"low","diseases_expected":[]},
      "seedling":{"gdd_from":50,"gdd_to":200,"vulnerability":"low","diseases_expected":["rice_leaf_folder"]},
      "tillering":{"gdd_from":200,"gdd_to":400,"vulnerability":"high","diseases_expected":["rice_blast","rice_brown_spot","rice_leaf_folder"]},
      "panicle_initiation":{"gdd_from":400,"gdd_to":600,"vulnerability":"high","diseases_expected":["rice_blast","rice_sheath_blight"]},
      "flowering":{"gdd_from":600,"gdd_to":750,"vulnerability":"critical","diseases_expected":["rice_blast","rice_bacterial_blight"]},
      "grain_fill":{"gdd_from":750,"gdd_to":900,"vulnerability":"medium","diseases_expected":["rice_sheath_blight","rice_brown_spot"]},
      "maturity":{"gdd_from":900,"gdd_to":1100,"vulnerability":"low","diseases_expected":[]}
    },
    "banana": {
      "establishment":{"gdd_from":0,"gdd_to":300,"vulnerability":"low","diseases_expected":[]},
      "vegetative":{"gdd_from":300,"gdd_to":800,"vulnerability":"medium","diseases_expected":["banana_sigatoka"]},
      "shooting":{"gdd_from":800,"gdd_to":1200,"vulnerability":"high","diseases_expected":["banana_fusarium","banana_sigatoka"]},
      "flowering":{"gdd_from":1200,"gdd_to":1600,"vulnerability":"high","diseases_expected":["banana_fusarium","banana_bbtv"]},
      "maturity":{"gdd_from":1600,"gdd_to":2000,"vulnerability":"medium","diseases_expected":[]}
    },
    "tomato": {
      "seedling":{"gdd_from":0,"gdd_to":150,"vulnerability":"low","diseases_expected":[]},
      "vegetative":{"gdd_from":150,"gdd_to":400,"vulnerability":"medium","diseases_expected":["tomato_early_blight"]},
      "flowering":{"gdd_from":400,"gdd_to":600,"vulnerability":"high","diseases_expected":["tomato_late_blight","tomato_leaf_curl"]},
      "fruit_set":{"gdd_from":600,"gdd_to":800,"vulnerability":"high","diseases_expected":["tomato_late_blight"]},
      "maturity":{"gdd_from":800,"gdd_to":1000,"vulnerability":"medium","diseases_expected":[]}
    },
    "maize": {
      "germination":{"gdd_from":0,"gdd_to":60,"vulnerability":"low","diseases_expected":[]},
      "vegetative":{"gdd_from":60,"gdd_to":400,"vulnerability":"medium","diseases_expected":["maize_northern_blight"]},
      "tasseling":{"gdd_from":400,"gdd_to":600,"vulnerability":"high","diseases_expected":["maize_northern_blight","maize_common_rust"]},
      "grain_fill":{"gdd_from":600,"gdd_to":1000,"vulnerability":"medium","diseases_expected":["maize_grey_leaf_spot"]},
      "maturity":{"gdd_from":1000,"gdd_to":1200,"vulnerability":"low","diseases_expected":[]}
    }
  }
}

IMPLEMENT backend/agents/weather.py:
- Call Open-Meteo API (development only — non-commercial):
  URL: https://api.open-meteo.com/v1/forecast
  Params: latitude, longitude, hourly=[temperature_2m,relativehumidity_2m,precipitation_probability,windspeed_10m], daily=[precipitation_sum,temperature_2m_max,temperature_2m_min], forecast_days=7
- Cache 30 minutes in class-level dict keyed by (round(lat,2), round(lon,2))
- Compute DFI (Disease Favorability Index):
  dfi = ((humidity_pct > 80) * 0.4 + (20 <= temperature_c <= 30) * 0.3 + (consecutive_wet_days / 7) * 0.3)
  dfi = max(0.0, min(1.0, dfi))
- Compute spray_window: rain_probability < 20% AND wind_speed < 15 km/h for any 4-hour block today
- Compute consecutive_wet_days: count consecutive days with precipitation_sum > 1mm going backwards from today
- Return WeatherResult with all indicators
- NO LLM call

IMPLEMENT backend/agents/crop_stage.py:
- Load backend/data/gdd_thresholds.json at module load
- Get weather history from DB (last 30 days daily tmax/tmin for this farm location)
- Compute cumulative GDD from planting_date:
  for each day: gdd_daily = max(0, ((tmax + tmin) / 2) - base_temp[crop])
  cumulative_gdd = sum of all gdd_daily values
- Match cumulative_gdd to stage threshold range in JSON
- Return CropStageResult with: stage_code, stage_name, vulnerability, days_after_sowing,
  cumulative_gdd, diseases_expected, upcoming_vulnerable_stage (next stage if current is low risk)
- NO LLM call

IMPLEMENT backend/agents/knowledge.py:
HYBRID RETRIEVAL:
1. Build query text: f"{crop} {vision_label} {stage_name} {district} {problem_description or ''}"

2. DENSE search using pgvector:
   embedding = embed_service.embed_query(query_text)
   # MUST use 'query: ' prefix via embedding service
   SQL: SELECT *, (embedding <=> :query_embedding) as distance
        FROM knowledge_chunks kc
        JOIN knowledge_documents kd ON kc.document_id = kd.id
        WHERE kd.valid_until > CURRENT_DATE AND kd.status = 'PUBLISHED'
        AND (kd.crop = :crop OR kd.crop IS NULL)
        ORDER BY embedding <=> :query_embedding
        LIMIT 20

3. SPARSE search using PostgreSQL FTS:
   SQL: SELECT *, ts_rank(to_tsvector('english', content), plainto_tsquery(:keywords)) as rank
        FROM knowledge_chunks WHERE to_tsvector('english', content) @@ plainto_tsquery(:keywords)
        AND valid_until > CURRENT_DATE LIMIT 20

4. Merge with RRF (Reciprocal Rank Fusion, k=60):
   score = sum(1 / (k + rank)) for each result from each source

5. Authority boost: multiply score by 1.3 for source_tier = 1 documents

6. Return top 5 chunks as KnowledgeResult
- NO LLM call

CREATE FILE: backend/services/embedding_service.py
EmbeddingService class using sentence-transformers 3.3.0:
- Singleton instance: SentenceTransformer('intfloat/multilingual-e5-large', device='cpu')
- embed_query(text: str) -> list[float]:
  return model.encode(f'query: {text}', normalize_embeddings=True, convert_to_numpy=True).tolist()
- embed_passage(text: str) -> list[float]:
  return model.encode(f'passage: {text}', normalize_embeddings=True, convert_to_numpy=True).tolist()
- Always use 'query: ' prefix for queries and 'passage: ' prefix for documents

VERIFY: Show weather.py DFI formula. Show crop_stage.py GDD formula.
Confirm embedding service uses normalize_embeddings=True.
```

---

## PROMPT P1-04: Decision and Explanation Agents

```
Agri-SAGE project. Agent phase.

TASK: Implement Decision and Explanation agents. Explanation uses LLM.

IMPLEMENT backend/agents/decision.py:
Scoring formula for each scenario A/B/C:
  score = (
    normalize(expected_yield_kgha, min_yield, max_yield)
    + normalize(expected_net_return_inr, min_return, max_return)
    - risk_penalty(scenario.risk_level)
    - uncertainty_penalty
  )
  risk_penalty: critical=-3, high=-2, medium=-1, low=0
  uncertainty_penalty = (1 - confidence_score) * 2

If farmer_budget_inr is set:
  Flag scenarios where expected_cost_inr > farmer_budget_inr as BUDGET_EXCEEDED

All scenario yield/return values must have modelled_estimate=True in output.
Return DecisionResult with: recommended_scenario, scored_scenarios, reasoning
NO LLM call.

IMPLEMENT backend/agents/explanation.py:
This agent calls the LLM. Use llm_service.generate() from backend/services/llm_service.py.

SYSTEM PROMPT — copy this VERBATIM, do not paraphrase:
"""
You are Agri-SAGE Advisory Engine, an agricultural decision support system.

YOUR ROLE:
Convert the structured evidence bundle below into a clear, actionable advisory
for a smallholder farmer. You are a translator of evidence — not a source of knowledge.

ABSOLUTE CONSTRAINTS:
1. Use ONLY facts from the evidence_bundle and knowledge_chunks provided below.
   Do not add any agricultural knowledge from your training data.
2. If evidence_bundle.confidence_state is UNCERTAIN, INSUFFICIENT_DATA, or
   CONFLICTING_EVIDENCE: do NOT recommend any treatment. Request more information.
3. Chemical product names: only use names that appear verbatim in the
   knowledge_chunks or cibrc_data provided. Never invent product names.
4. All yield/profit numbers come from simulation_result only.
   Always label them: "modelled estimate — actual results vary by field conditions".
5. Government schemes: always include: "Final eligibility determined by the
   concerned authority — please verify before applying."
6. Language: Generate advisory in {language_code} ({language_name}).
   Use simple, everyday vocabulary. Avoid technical jargon.
7. Output ONLY valid JSON matching the schema below. No markdown. No explanation.

OUTPUT JSON:
{
  "diagnosis_summary": "<2 sentences max>",
  "confidence_explanation": "<1 sentence>",
  "risk_explanation": "<1-2 sentences>",
  "recommended_action": {
    "what": "<specific action>",
    "when": "<specific timing>",
    "how": "<method>",
    "cost_note": "<cost range>",
    "spray_window": "<time or null>"
  },
  "evidence_summary": ["<point 1>", "<point 2>"],
  "what_would_change_this": ["<factor 1>"],
  "safe_to_act": true,
  "insufficient_data_message": null,
  "modelled_estimate_label": "modelled estimate — actual results vary by field conditions"
}
"""

USER PROMPT TEMPLATE:
"""
EVIDENCE BUNDLE:
confidence_state: {confidence_state}
confidence_score: {confidence_score}
VISION: label={vision_label} severity={vision_severity} affected_area_pct={affected_area_pct}
WEATHER: dfi={dfi} spray_window={spray_window} wet_days={wet_days} temp={temperature} humidity={humidity}
CROP STAGE: stage={stage_name} vulnerability={vulnerability} das={das}
KNOWLEDGE CHUNKS: {knowledge_chunks_json}
SIMULATION: {simulation_result_json}
CONFLICTS: {conflicts_json}
MISSING: {missing_data_json}
CONTEXT: crop={crop} location={district},{state} language={language_name}
Generate advisory JSON now. Output JSON only.
"""

Logic:
1. If confidence_state in ['UNCERTAIN','INSUFFICIENT_DATA','CONFLICTING_EVIDENCE']:
   Override: do not pass any chemical recommendation to LLM
   Add to prompt: "safe_to_act must be false. Do not recommend any treatment."

2. Call LLMService.generate(system_prompt, user_prompt, temperature=0.2, max_tokens=1500)

3. If LLM returns None (failed after 2 retries): use SAFE_FALLBACK:
   SAFE_FALLBACK = {
     "diagnosis_summary": "We analyzed your crop photo and farm conditions.",
     "confidence_explanation": "Our confidence is limited — please see evidence details.",
     "risk_explanation": "Please inspect your field and consult a local agronomist.",
     "recommended_action": {
       "what": "Inspect 10 plants in different parts of the field",
       "when": "Today",
       "how": "Look for spread of symptoms since photo was taken",
       "cost_note": "No cost — visual inspection only",
       "spray_window": None
     },
     "evidence_summary": ["Photo analyzed", "Weather checked", "Crop stage estimated"],
     "what_would_change_this": ["A clearer photo", "A soil test result"],
     "safe_to_act": False,
     "insufficient_data_message": "Advisory generation encountered a technical issue.",
     "modelled_estimate_label": "modelled estimate — actual results vary by field conditions"
   }

4. Validate LLM output against Pydantic schema — if schema invalid: use SAFE_FALLBACK

5. Check for invented product names:
   Any product name in recommended_action.what must appear verbatim in knowledge_chunks content
   If not found: log warning, replace recommendation with request-more-info message

VERIFY: Show explanation.py. Confirm system prompt is copied exactly. Confirm SAFE_FALLBACK exists.
```

---

## PROMPT P1-05: Diagnose Endpoint and Full Pipeline

```
Agri-SAGE project. Agent phase.

TASK: Wire all agents into the diagnose endpoint and test end-to-end.

CREATE FILE: backend/api/v1/diagnose.py
POST /api/v1/diagnose
Input: {"observation_id": "uuid-string"}
Auth: require_auth dependency

Logic:
1. Verify observation exists and is owned by current user (RLS handles this)
2. Load observation + images from DB
3. Build initial AgriSAGEState with observation data
4. Start timer: pipeline_start_ms = int(time.time() * 1000)
5. Run advisory_graph with 10-second timeout:
   config = {"configurable": {"thread_id": str(observation_id)}}
   result = await asyncio.wait_for(advisory_graph.ainvoke(state, config=config), timeout=10.0)
6. On timeout: return safe fallback advisory with generation_ms=-1 and note in evidence
7. Calculate generation_ms
8. Save complete advisory to advisories table
9. Log audit event: advisory_generated with user_id, advisory_id, generation_ms, confidence_state
10. Return full AdvisoryResponse

AdvisoryResponse schema (return all these fields):
{
  advisory_id: str,
  observation_id: str,
  confidence_state: str,  # one of 7 valid states
  confidence_score: float,
  diagnosis: {label, common_name: {ml, en}, confidence_score, severity, affected_area_pct},
  risk: {level, horizon_days, factors},
  scenarios: [{id, label, action, expected_yield_kgha, modelled_estimate: true,
               expected_cost_inr, expected_net_return_inr, risk_level}],
  recommended_scenario: str,
  recommended_action: {what, when, how, spray_window, cost_estimate_inr: {min, max}},
  evidence: {items, contradictions, missing_data},
  what_would_change_this: [str],
  safe_to_act: bool,
  scheme_matches: [],
  sources: [{title, authority, tier}],
  model_version: str,
  generation_ms: int,
  created_at: str
}

IMPORTANT: Every scenario with yield/return numbers must have modelled_estimate: true

CREATE FILE: tests/integration/test_full_pipeline.py
Test the full advisory pipeline:
1. Create test farm, field, crop cycle, observation with test image
2. POST /api/v1/diagnose with observation_id
3. Assert response.status_code == 200
4. Assert all required AdvisoryResponse fields present
5. Assert confidence_state is one of 7 valid states
6. Assert safe_to_act is boolean
7. Assert all scenarios have modelled_estimate == True
8. Assert generation_ms < 15000 (15 seconds max in test)
9. If confidence_state in ['UNCERTAIN','INSUFFICIENT_DATA','CONFLICTING_EVIDENCE']:
   Assert recommended_action does not contain any chemical product name

VERIFY: Run the integration test. Show test output. Fix any failures.
```

---

## PROMPT P1-06: Scheme and Monitoring Agents

```
Agri-SAGE project. Agent phase.

TASK: Implement Scheme and Monitoring agents.

IMPLEMENT backend/agents/scheme.py:
1. Query schemes table: valid_until > NOW() AND status='active' AND (:crop = ANY(crops_applicable) OR crops_applicable IS NULL)
2. For each scheme: score eligibility from eligibility_rules JSONB against farmer profile
3. For complex eligibility: call LLM with this system prompt VERBATIM:

SYSTEM PROMPT:
"""
You are Agri-SAGE Scheme Eligibility Assessor.

YOUR ROLE: Assess whether a farmer appears to meet government scheme criteria.

ABSOLUTE CONSTRAINTS:
1. NEVER state 'you are eligible'. Always: 'You appear to meet the criteria listed below.'
2. ALWAYS end every assessment with: 'Final eligibility is determined by the concerned authority. Please verify before applying.'
3. Only assess schemes from scheme_data provided. Never mention other schemes.
4. If valid_until passed, do not include the scheme.

OUTPUT: Valid JSON only.
{
  "matches": [{
    "scheme_name": "<exact name from data>",
    "eligibility_assessment": "likely_meets|partially_meets|cannot_determine",
    "matching_criteria": ["<criterion>"],
    "missing_criteria": ["<what we cannot verify>"],
    "key_benefit": "<main benefit>",
    "enrollment_steps": ["<step>"],
    "deadline": "<date or null>",
    "mandatory_caveat": "Final eligibility determined by the concerned authority. Please verify before applying."
  }],
  "no_matches_reason": null
}
"""
Temperature: 0.1
Return top 3 scheme matches maximum.
The mandatory_caveat field must ALWAYS be present in every match.

IMPLEMENT backend/agents/monitoring.py:
Morning briefing generator:
1. Runs via APScheduler at 05:30 UTC daily
2. Query all active users with active crop cycles
3. For each user: load farm + crop + latest weather + latest risk scores
4. Call LLM with this system prompt VERBATIM:

SYSTEM PROMPT:
"""
You are Agri-SAGE Morning Briefing Generator.

RULES:
1. Maximum 4 items — one per category.
2. Simple language — farmer acts on this immediately.
3. Specific: 'Check lower leaves' not 'Monitor crop health'.
4. If no significant risk: say 'All clear today'.
5. One recommended action only — most important for today.
6. Language: {language_name}.

OUTPUT: Valid JSON only.
{"stage_summary":"<crop+stage+days>","top_risk":{"risk_type":"disease|pest|water|heat|none",
"level":"high|medium|low|none","description":"<1 sentence>","is_urgent":false},
"weather_today":"<2 words>","recommended_action":"<one action>",
"market_note":null,"all_clear":false}
"""
Temperature: 0.3

5. Store briefing in notifications table (type='morning_briefing')
6. Send via FCM using firebase-admin SDK

CREATE FILE: backend/services/notifications.py
FCMNotificationService:
- Initialize firebase-admin with credentials from settings.FCM_KEY
- send(user_id: str, title: str, body: str, data: dict) -> bool:
  Look up user.fcm_token from DB
  Call messaging.send(Message(notification=Notification(title,body), data=data, token=fcm_token))
  Return True on success, False on failure (log error, never raise)

VERIFY: Show scheme.py. Confirm mandatory_caveat is always present in every scheme match.
```

---

# PHASE 2 — DATA AND KNOWLEDGE

---

## PROMPT P2-01: All Required Data Files

```
Agri-SAGE project. Data phase.

TASK: Create ALL required JSON data files. These files are loaded by agents at startup.

CREATE FILE: backend/data/offline_templates_ml.json
Content:
{
  "disease_detected": {
    "text": "നിങ്ങളുടെ {crop} വിളയിൽ {disease} ന്റെ ലക്ഷണങ്ങൾ കാണുന്നു. ആത്മവിശ്വാസം: {confidence}. ഇന്ന് {action} ചെയ്യുക.",
    "slots": ["crop", "disease", "confidence", "action"]
  },
  "insufficient_data": {
    "text": "ഫോട്ടോ കൂടുതൽ വ്യക്തമല്ല. ഇലയുടെ അടുത്ത് നിന്ന് നല്ല വെളിച്ചത്തിൽ ഫോട്ടോ എടുക്കുക.",
    "slots": []
  },
  "conflicting_evidence": {
    "text": "ഫോട്ടോയും കാലാവസ്ഥ ഡേറ്റയും വ്യത്യസ്ത ഫലങ്ങൾ കാണിക്കുന്നു. ഒരു കൃഷി വിദഗ്ദ്ധനെ സമീപിക്കുക.",
    "slots": []
  },
  "all_clear": {
    "text": "ഇന്ന് നിങ്ങളുടെ {crop} ആരോഗ്യകരമായി കാണുന്നു. കാലാവസ്ഥ: {weather}.",
    "slots": ["crop", "weather"]
  },
  "offline_notice": {
    "text": "ഇന്റർനെറ്റ് ഇല്ല — ഇത് ഒരു ഓഫ്‌ലൈൻ വിശകലനമാണ്. ഇന്റർനെറ്റ് ലഭ്യമാകുമ്പോൾ കൂടുതൽ കൃത്യമായ ഉത്തരം ലഭിക്കും.",
    "slots": []
  },
  "spray_window": {
    "text": "ഇന്ന് {time} മുതൽ {time_end} വരെ കൃഷിമരുന്ന് തളിക്കാൻ അനുയോജ്യമായ സമയമാണ്.",
    "slots": ["time", "time_end"]
  },
  "high_risk_alert": {
    "text": "⚠ {crop} വിളയ്ക്ക് ഇന്ന് {risk_type} അപകടം കൂടുതലാണ്. {action} ചെയ്യുക.",
    "slots": ["crop", "risk_type", "action"]
  }
}

CREATE FILE: backend/data/intent_keywords_ml.json
Content:
{
  "നെൽ": {"field": "crop", "value": "rice"},
  "നെല്ല്": {"field": "crop", "value": "rice"},
  "വാഴ": {"field": "crop", "value": "banana"},
  "തക്കാളി": {"field": "crop", "value": "tomato"},
  "ചോളം": {"field": "crop", "value": "maize"},
  "തെങ്ങ്": {"field": "crop", "value": "coconut"},
  "ബ്ലാസ്റ്റ്": {"field": "problem", "value": "blast"},
  "പുള്ളി": {"field": "symptom", "value": "spots"},
  "ഇല": {"field": "body_part", "value": "leaf"},
  "ചുരുളൽ": {"field": "symptom", "value": "curling"},
  "മഞ്ഞ": {"field": "symptom", "value": "yellowing"},
  "കരിച്ചിൽ": {"field": "symptom", "value": "burning"},
  "ദ്രവം": {"field": "symptom", "value": "rot"},
  "നനഞ്ഞ": {"field": "irrigation_status", "value": "irrigated"},
  "വരൾ": {"field": "irrigation_status", "value": "dry"},
  "ഗോതമ്പ്": {"field": "crop", "value": "wheat"},
  "കൃഷി": {"field": "domain", "value": "agriculture"}
}

CREATE FILE: backend/data/stage_disease_map.json
Content:
{
  "rice_germination": {"expected": [], "unlikely": ["rice_blast", "rice_brown_spot"]},
  "rice_seedling": {"expected": ["rice_leaf_folder"], "unlikely": ["rice_bacterial_blight"]},
  "rice_tillering": {"expected": ["rice_blast", "rice_brown_spot", "rice_leaf_folder"], "unlikely": []},
  "rice_panicle_initiation": {"expected": ["rice_blast", "rice_sheath_blight"], "unlikely": []},
  "rice_flowering": {"expected": ["rice_blast", "rice_bacterial_blight"], "unlikely": ["rice_leaf_folder"]},
  "rice_grain_fill": {"expected": ["rice_sheath_blight", "rice_brown_spot"], "unlikely": ["rice_blast"]},
  "rice_maturity": {"expected": [], "unlikely": ["rice_blast"]},
  "banana_vegetative": {"expected": ["banana_sigatoka"], "unlikely": ["banana_fusarium"]},
  "banana_shooting": {"expected": ["banana_fusarium", "banana_sigatoka"], "unlikely": []},
  "banana_flowering": {"expected": ["banana_fusarium", "banana_bbtv"], "unlikely": []},
  "tomato_vegetative": {"expected": ["tomato_early_blight"], "unlikely": ["tomato_late_blight"]},
  "tomato_flowering": {"expected": ["tomato_late_blight", "tomato_leaf_curl"], "unlikely": []},
  "tomato_fruit_set": {"expected": ["tomato_late_blight"], "unlikely": []},
  "maize_vegetative": {"expected": ["maize_northern_blight"], "unlikely": ["maize_common_rust"]},
  "maize_tasseling": {"expected": ["maize_northern_blight", "maize_common_rust"], "unlikely": []}
}

CREATE FILE: scripts/seed_schemes.py
Seed the schemes table with these real government schemes:
1. PMFBY (Pradhan Mantri Fasal Bima Yojana):
   name="Pradhan Mantri Fasal Bima Yojana", short_name="PMFBY",
   authority="Ministry of Agriculture", authority_level="central",
   state=None (all India), crops_applicable=["rice","maize","tomato","banana"],
   eligibility_rules={"land_ownership":["owner","tenant"],"aadhaar_required":true,"enrollment_window_days_after_sowing":30},
   benefits_json={"premium_kharif_pct":2.0,"premium_rabi_pct":1.5,"coverage":"yield loss"},
   enrollment_url="https://pmfby.gov.in", valid_until="2027-03-31"

2. PM-KISAN:
   name="Pradhan Mantri Kisan Samman Nidhi", short_name="PM-KISAN",
   authority="Ministry of Agriculture", authority_level="central",
   state=None, crops_applicable=None (all crops),
   eligibility_rules={"land_ha_max":2,"not_income_taxpayer":true,"not_government_employee":true},
   benefits_json={"annual_amount_inr":6000,"installments":3},
   valid_until="2028-03-31"

3. Kerala Karshaka Kshemanidhi (Kerala farmers welfare fund):
   authority="Kerala Agriculture Department", authority_level="state", state="Kerala",
   crops_applicable=["rice","banana","coconut","tomato","maize"],
   eligibility_rules={"state":"Kerala","registered_farmer":true},
   valid_until="2027-03-31"

VERIFY: Show all 4 JSON files. Confirm disease_classes.json has exactly 22 entries (index 0-21).
Confirm gdd_thresholds.json has base_temperatures for all 5 crops.
```

---

## PROMPT P2-02: Knowledge Ingestion Pipeline

```
Agri-SAGE project. Data phase.

TASK: Create the complete knowledge ingestion and retrieval system.

CREATE FILE: backend/knowledge/ingestion.py
DocumentIngestionPipeline class:

async fetch_document(url: str) -> bytes:
  Use httpx AsyncClient with timeout=30s. Return raw bytes.

def parse_pdf(content: bytes) -> str:
  Use PyMuPDF (import fitz):
  doc = fitz.open(stream=content, filetype="pdf")
  Extract text from all pages preserving paragraph structure.
  Tables: extract as tab-separated rows.
  Return full text string.

def parse_html(content: bytes) -> str:
  Use BeautifulSoup:
  Remove all script, style, nav, footer, header tags.
  Extract text with double newline between blocks.
  Return clean text string.

def extract_metadata(text: str, url: str, manual_meta: dict = None) -> dict:
  Detect crop mentions (rice/banana/coconut/tomato/maize) — return first found or None
  Detect state names (Kerala/Tamil Nadu/Karnataka/Andhra Pradesh/Maharashtra) — return first found
  Detect date patterns for published_at
  Return: {crop, state, topic, source_tier, source_authority, published_at, valid_until, language}
  Default valid_until: 2 years from today if not found in text

def extract_chunks(text: str, metadata: dict) -> list[dict]:
  Split at heading boundaries first (## patterns, ALL CAPS lines, lines ending with :)
  Then split at paragraph boundaries (double newline)
  Rules:
    max chunk: 512 tokens (~2000 characters)
    min chunk: 100 characters — discard shorter
    Never split mid-sentence — split at sentence boundary
    Never split mid-table — keep table rows together
  Return list of {content, metadata, chunk_index}

async embed_and_store(document_id: str, chunks: list[dict]):
  Use EmbeddingService.embed_passage() for each chunk (MUST use 'passage: ' prefix)
  Batch size: 32 chunks per batch
  Bulk INSERT into knowledge_chunks with ON CONFLICT DO NOTHING

CREATE FILE: backend/knowledge/retrieval.py
HybridRetriever class (implementation from knowledge agent but as standalone service):
  retrieve(query: str, crop: str, state: str, top_k: int = 5) -> list[dict]
  All logic from knowledge agent — dense + sparse + RRF + authority boost

CREATE FILE: scripts/seed_knowledge.py
Create scripts/seed_urls.json with these real agricultural document URLs:
[
  {"url": "https://www.icar.org.in/content/improved-management-practices-rice", "crop": "rice", "source_tier": 1, "source_authority": "ICAR"},
  {"url": "https://www.kau.in/sites/default/files/documents/package-practices-rice.pdf", "crop": "rice", "source_tier": 1, "source_authority": "KAU"},
  {"url": "https://www.icar.org.in/content/banana-cultivation", "crop": "banana", "source_tier": 1, "source_authority": "ICAR"},
  {"url": "https://www.kau.in/sites/default/files/documents/package-practices-banana.pdf", "crop": "banana", "source_tier": 1, "source_authority": "KAU"},
  {"url": "https://www.icar.org.in/content/coconut-diseases", "crop": "coconut", "source_tier": 1, "source_authority": "ICAR"}
]

seed_knowledge.py reads seed_urls.json, calls pipeline.ingest(url, metadata) for each, prints progress.

VERIFY: Show ingestion.py extract_chunks function. Confirm chunks are 100-2000 chars.
Confirm embed_passage uses 'passage: ' prefix.
```

---

## PROMPT P2-03: Vision Model Training

```
Agri-SAGE project. Data phase.

TASK: Create the complete vision model training pipeline.

CREATE FILE: backend/ml/vision/train.py

Model architecture:
  import torchvision.models as models
  model = models.efficientnet_b3(weights=models.EfficientNet_B3_Weights.IMAGENET1K_V1)
  model.classifier = nn.Sequential(nn.Dropout(0.3), nn.Linear(1536, 22))
  # 22 classes matching disease_classes.json index order

Dataset split — FARMER-LEVEL split (not random split):
  Group images by top-level farmer subdirectory
  Split at farmer level: 70% train / 15% val / 15% test
  This prevents data leakage from same-farmer near-duplicate images

Data augmentation (training only):
  transforms.RandomResizedCrop(300, scale=(0.7, 1.0))
  transforms.RandomHorizontalFlip()
  transforms.RandomVerticalFlip(p=0.2)
  transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.2)
  transforms.GaussianBlur(kernel_size=5, p=0.2)
  transforms.ToTensor()
  transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])

Validation/test transforms:
  transforms.Resize(320)
  transforms.CenterCrop(300)
  transforms.ToTensor()
  transforms.Normalize(same as above)

Training configuration:
  optimizer = Adam(lr=1e-4, weight_decay=1e-5)
  scheduler = CosineAnnealingLR(T_max=50)
  class_weights computed from training set class frequencies (inverse frequency)
  criterion = CrossEntropyLoss(weight=class_weights)
  max_epochs = 50
  early_stopping patience = 7 on val macro_f1
  batch_size = 16 (suitable for low-RAM training)

Temperature scaling calibration (post-training):
  On validation set, fit a temperature parameter T
  Calibrated logits = logits / T
  Optimize T to minimize ECE (Expected Calibration Error)
  Target ECE < 0.12

Evaluation metrics:
  macro_f1 = f1_score(y_true, y_pred, average='macro')
  per_class_f1 = f1_score(y_true, y_pred, average=None)
  ece = compute_ece(y_prob, y_true, n_bins=10)
  confusion_matrix

After training:
  ASSERT macro_f1 >= 0.82 — print "PASS: F1={macro_f1:.3f}" or "FAIL: F1={macro_f1:.3f} below threshold"
  ASSERT ece <= 0.12 — print "PASS: ECE={ece:.3f}" or "FAIL: ECE={ece:.3f} above threshold"
  Save checkpoints/best_model.pt and checkpoints/calibrated_model.pt
  Save checkpoints/training_metrics.json with all metrics

CREATE FILE: backend/ml/vision/export.py

def export_to_onnx(model_path: str, output_path: str, opset: int = 17):
  Load calibrated_model.pt
  Create dummy input: torch.randn(1, 3, 300, 300)
  torch.onnx.export(model, dummy, output_path, opset_version=opset,
    input_names=['image'], output_names=['logits'],
    dynamic_axes={'image': {0: 'batch_size'}, 'logits': {0: 'batch_size'}})
  Verify export: run inference on dummy, compare output shape

def quantize_int8(onnx_path: str, quantized_path: str):
  from onnxruntime.quantization import quantize_dynamic, QuantType
  quantize_dynamic(onnx_path, quantized_path, weight_type=QuantType.QInt8)

def verify_accuracy_loss(fp32_path: str, int8_path: str, test_loader) -> float:
  Run both models on test set
  Compute macro_f1 for each
  accuracy_loss = fp32_f1 - int8_f1
  ASSERT accuracy_loss < 0.02 — print result
  Return accuracy_loss

VERIFY: Show train.py training loop. Confirm FARMER-LEVEL split.
Confirm temperature scaling calibration is implemented.
Confirm accuracy assertion: macro_f1 >= 0.82.
```

---

# PHASE 3 — ANDROID APP

---

## PROMPT P3-01: Android Project Setup

```
Agri-SAGE Android app. Setup phase.

TASK: Create Android project with all dependencies and design system.

Create Android project in mobile/android/ with:
  Package: com.agrisage.app
  MinSdk: 26 (Android 8.0)
  TargetSdk: 35
  Language: Kotlin 2.0.21

CREATE FILE: mobile/android/app/build.gradle.kts
Use KSP (NOT kapt) for Room and Hilt. Include ALL these dependencies:

plugins {
  id("com.android.application")
  id("org.jetbrains.kotlin.android")
  id("org.jetbrains.kotlin.plugin.compose")
  id("com.google.devtools.ksp")
  id("com.google.dagger.hilt.android")
  id("org.jetbrains.kotlin.plugin.serialization")
}

dependencies {
  val composeBom = platform("androidx.compose:compose-bom:2024.12.01")
  implementation(composeBom)
  implementation("androidx.compose.ui:ui")
  implementation("androidx.compose.material3:material3")
  implementation("androidx.compose.ui:ui-tooling-preview")
  implementation("androidx.activity:activity-compose:1.9.3")
  implementation("androidx.navigation:navigation-compose:2.8.5")
  implementation("org.jetbrains.kotlinx:kotlinx-serialization-json:1.7.3")
  implementation("androidx.room:room-runtime:2.7.0")
  implementation("androidx.room:room-ktx:2.7.0")
  ksp("androidx.room:room-compiler:2.7.0")
  implementation("com.squareup.retrofit2:retrofit:2.11.0")
  implementation("com.squareup.retrofit2:converter-gson:2.11.0")
  implementation("com.squareup.okhttp3:okhttp:4.12.0")
  implementation("com.squareup.okhttp3:logging-interceptor:4.12.0")
  implementation("com.google.dagger:hilt-android:2.53")
  ksp("com.google.dagger:hilt-compiler:2.53")
  implementation("androidx.hilt:hilt-navigation-compose:1.2.0")
  implementation("androidx.camera:camera-core:1.4.0")
  implementation("androidx.camera:camera-camera2:1.4.0")
  implementation("androidx.camera:camera-lifecycle:1.4.0")
  implementation("androidx.camera:camera-view:1.4.0")
  implementation("com.microsoft.onnxruntime:onnxruntime-android:1.20.0")
  implementation("androidx.work:work-runtime-ktx:2.10.0")
  implementation("com.google.firebase:firebase-messaging-ktx:24.1.0")
  implementation("io.coil-kt:coil-compose:2.7.0")
  implementation("androidx.lifecycle:lifecycle-viewmodel-compose:2.8.7")
  implementation("androidx.lifecycle:lifecycle-runtime-compose:2.8.7")
  implementation("androidx.security:security-crypto:1.1.0-alpha06")
  debugImplementation("androidx.compose.ui:ui-tooling")
}

CREATE FILE: mobile/android/app/src/main/java/com/agrisage/app/ui/theme/Color.kt
ALL 30 color tokens with EXACT hex values:
val ColorPrimary = Color(0xFF2D7D2D)
val ColorPrimaryDark = Color(0xFF1A5C1A)
val ColorPrimaryLight = Color(0xFFE8F5E8)
val ColorPrimaryContainer = Color(0xFFC8E6C9)
val ColorSecondary = Color(0xFF558B2F)
val ColorSecondaryLight = Color(0xFFF1F8E9)
val ColorRiskCritical = Color(0xFFC62828)
val ColorRiskHigh = Color(0xFFE65100)
val ColorRiskMedium = Color(0xFFF57F17)
val ColorRiskLow = Color(0xFF2E7D32)
val ColorConfidenceConfirmed = Color(0xFF1B5E20)
val ColorConfidenceLikely = Color(0xFF2E7D32)
val ColorConfidencePossible = Color(0xFFF57F17)
val ColorConfidenceUncertain = Color(0xFFBF360C)
val ColorConfidenceInsufficient = Color(0xFF757575)
val ColorSurface = Color(0xFFFAFAFA)
val ColorSurfaceVariant = Color(0xFFF5F5F5)
val ColorOnSurface = Color(0xFF212121)
val ColorOnSurfaceSecondary = Color(0xFF616161)
val ColorOnSurfaceTertiary = Color(0xFF9E9E9E)
val ColorOutline = Color(0xFFBDBDBD)
val ColorWarningBg = Color(0xFFFFF9C4)
val ColorWarningText = Color(0xFFF57F17)
val ColorInfoBg = Color(0xFFE3F2FD)
val ColorOfflineBanner = Color(0xFFFFF3E0)
val ColorOfflineText = Color(0xFFE65100)
val ColorCachedLabel = Color(0xFFFF8F00)
val ColorSchemeBg = Color(0xFFEDE7F6)
val ColorSchemeText = Color(0xFF4527A0)
val ColorOnPrimary = Color(0xFFFFFFFF)

CREATE FILE: ui/theme/Type.kt
Noto Sans font family, all 10 text styles with exact sp values:
headlineLarge: Bold 24sp/32sp
headlineMedium: SemiBold 20sp/28sp
headlineSmall: SemiBold 18sp/24sp
bodyLarge: Normal 16sp/24sp
bodyMedium: Normal 14sp/20sp
bodySmall: Normal 12sp/16sp
labelLarge: Medium 14sp/20sp
labelMedium: Medium 12sp/16sp
labelSmall: Medium 10sp/14sp

CREATE FILE: ui/theme/Theme.kt
AgriSAGETheme composable using MaterialTheme with our ColorScheme, Typography, Shapes.
Support both light and dark color schemes.

CREATE FILE: res/xml/network_security_config.xml
<network-security-config>
    <base-config cleartextTrafficPermitted="false"/>
</network-security-config>

Add to AndroidManifest.xml: android:networkSecurityConfig="@xml/network_security_config"

VERIFY: Show Color.kt — confirm exactly 30 tokens. Show build.gradle.kts — confirm ksp not kapt.
```

---

## PROMPT P3-02: Room Database and Navigation

```
Agri-SAGE Android. Database phase.

TASK: Create all Room entities, DAOs, database class, and type-safe navigation.

CREATE all Room entities in data/local/entities/:

FarmerEntity.kt:
@Entity(tableName = "farmers")
data class FarmerEntity(
    @PrimaryKey val id: String,
    val phone: String, val name: String?,
    val language: String = "ml",
    val subscriptionTier: String = "free",
    val subscriptionExpires: Long? = null,
    val updatedAt: Long
)

FarmEntity.kt:
@Entity(tableName = "farms")
data class FarmEntity(
    @PrimaryKey val id: String,
    val userId: String, val name: String,
    val locationLat: Double?, val locationLon: Double?,
    val district: String?, val state: String?,
    val areaHa: Double?,
    val isSynced: Boolean = false,
    val createdAt: Long
)

FieldEntity, CropCycleEntity, ObservationEntity, ImageEntity — create matching backend schema

CachedAdvisoryEntity.kt:
@Entity(tableName = "cached_advisories")
data class CachedAdvisoryEntity(
    @PrimaryKey val id: String,
    val observationId: String,
    val advisoryJson: String,
    val type: String = "advisory",
    val isOffline: Boolean = false,
    val createdAt: Long
)

WeatherCacheEntity.kt:
@Entity(tableName = "weather_cache")
data class WeatherCacheEntity(
    @PrimaryKey val locationKey: String,
    val dataJson: String,
    val cachedAt: Long
)

SyncQueueEntity.kt:
@Entity(tableName = "sync_queue")
data class SyncQueueEntity(
    @PrimaryKey(autoGenerate = true) val id: Int = 0,
    val entityType: String,
    val entityId: String,
    val action: String,
    val payloadJson: String,
    val priority: Int = 5,
    val retryCount: Int = 0,
    val createdAt: Long
)

Create DAO for each entity with standard CRUD operations plus:
- FarmDao: getFarmsByUserId, getFarmById, updateSyncStatus
- SyncQueueDao: getUnsyncedByPriority, incrementRetryCount, deleteById
- CachedAdvisoryDao: getByObservationId, getMorningBriefing, deleteOlderThan

CREATE AgriSAGEDatabase.kt:
@Database(
    entities = [FarmerEntity::class, FarmEntity::class, FieldEntity::class,
                CropCycleEntity::class, ObservationEntity::class, ImageEntity::class,
                CachedAdvisoryEntity::class, WeatherCacheEntity::class, SyncQueueEntity::class],
    version = 1
)
abstract class AgriSAGEDatabase : RoomDatabase() { ... }

Create Hilt DatabaseModule providing database and all DAOs.

CREATE NavGraph.kt with type-safe @Serializable routes:
@Serializable object HomeRoute
@Serializable object CameraRoute
@Serializable data class AdvisoryRoute(val advisoryId: String)
@Serializable data class ContextFormRoute(val imagePath: String)
@Serializable object FarmRoute
@Serializable object AlertsRoute
@Serializable object ProfileRoute
@Serializable object OnboardingRoute
@Serializable object LanguageSelectionRoute
@Serializable object OtpRoute
@Serializable object FarmSetupRoute
@Serializable object SchemeRoute

NavHost(navController, startDestination = OnboardingRoute) with all routes defined.

VERIFY: Show AgriSAGEDatabase.kt entity list. Show NavGraph.kt routes.
Confirm @Serializable annotation on all route classes.
```

---

## PROMPT P3-03: Camera Screen

```
Agri-SAGE Android. Screen phase.

TASK: Create the Camera screen with real-time quality indicator.

CREATE FILE: ui/screens/CameraScreen.kt

Complete implementation:

1. Full-screen CameraX preview:
   Use PreviewView inside AndroidView composable
   Use ImageAnalysis use case running on background dispatcher every 500ms

2. Quality detection (ImageAnalysis callback):
   Blur detection: compute Laplacian variance on Y channel of YUV image
     Convert to grayscale, apply Laplacian kernel [-1,-1,-1,-1,8,-1,-1,-1,-1]
     Compute variance of result
     threshold: < 100 = POOR blur
   Brightness: compute mean of Y channel
     < 40 = POOR (too dark), > 220 = POOR (overexposed)
   Coverage: estimate if crop fills > 30% of center region
   
   QualityLevel enum: GOOD / OKAY / POOR
   GOOD = blur OK AND brightness OK AND coverage OK
   OKAY = blur OK AND brightness OK (coverage uncertain)
   POOR = any check fails

3. QualityIndicatorBar composable:
   Full-width Box, height 8.dp
   animateColorAsState with 200ms animation:
     GOOD → Color(0xFF4CAF50)
     OKAY → Color(0xFFFF9800)
     POOR → Color(0xFFF44336)

4. Quality message Text below bar (changes per quality level):
   GOOD: "Good — tap to capture"
   OKAY: "Hold steady for better results"
   POOR (blur): "ഫോട്ടോ മങ്ങിയിരിക്കുന്നു — ഉറച്ചു പിടിക്കുക"
   POOR (dark): "ഇരുട്ടാണ് — തണൽ ഇടത്ത് നിൽക്കുക"
   POOR (coverage): "നടുഭാഗത്ത് ഇല കൊണ്ടുവരൂ"

5. Capture Button:
   80.dp circular, white fill, ColorPrimary 4.dp border
   Positioned: Alignment.BottomCenter, padding bottom 48.dp
   hapticFeedback.performHapticFeedback(HapticFeedbackType.LongPress) on click
   On tap: take photo using ImageCapture use case

6. On capture:
   If quality POOR: show AlertDialog with specific rejection message + "Try Again" button
   If GOOD or OKAY: save to app cache directory, navigate to ContextFormRoute(imagePath)

7. CropChip: top-right corner, shows current crop from ViewModel
   Tappable → show ModalBottomSheet with crop picker (rice/banana/coconut/tomato/maize)

8. Close button: top-left, 48.dp, X icon, navigates back

CREATE FILE: ui/screens/CameraViewModel.kt
- currentCrop: StateFlow<String>
- qualityLevel: StateFlow<QualityLevel>
- capturedImagePath: StateFlow<String?>
- Functions: onCropSelected, onCaptureComplete

VERIFY: Show CameraScreen.kt. Confirm Laplacian variance blur detection.
Confirm haptic feedback on capture. Confirm POOR quality shows AlertDialog.
```

---

## PROMPT P3-04: Advisory Result Screen

```
Agri-SAGE Android. Screen phase.

TASK: Create the Advisory Result screen with all required composables.

CREATE all composables in ui/components/:

ConfidenceBadge.kt:
@Composable
fun ConfidenceBadge(state: String) — pill Row 32.dp height corner 16.dp
Colors:
  "CONFIRMED" → ColorConfidenceConfirmed background
  "LIKELY" → ColorConfidenceLikely background
  "POSSIBLE" → Color(0xFFF57F17) background
  "UNCERTAIN" → ColorConfidenceUncertain background
  "INSUFFICIENT_DATA" → ColorConfidenceInsufficient background
  "CONFLICTING_EVIDENCE" → ColorConfidenceUncertain background
  "OUT_OF_SCOPE" → ColorConfidenceInsufficient background
Text: white on all, labelMedium style

RiskLevelBadge.kt:
@Composable fun RiskLevelBadge(level: String)
CRITICAL → ColorRiskCritical, HIGH → ColorRiskHigh
MEDIUM → ColorRiskMedium, LOW → ColorRiskLow

EvidenceCard.kt:
@Composable fun EvidenceCard(items: List<EvidenceItem>, expanded: Boolean = true)
Background: ColorInfoBg
Corner: 12.dp
Left border: 2.dp ColorPrimary (use Box with start padding and background)
Expandable — expanded by default
Each item: Row with icon (16.dp) + bodyMedium text

ActionCard.kt:
@Composable fun ActionCard(action: RecommendedAction)
Background: ColorPrimaryLight
Corner: 16.dp
2.dp border: ColorPrimary
Fields shown with icons:
  WHAT: agriculture icon
  WHEN: schedule icon — bold text if is_urgent
  HOW: construction icon
  SPRAY_WINDOW: wb_sunny icon — only shown if not null
  COST: payments icon

ModelledEstimateLabel.kt:
@Composable fun ModelledEstimateLabel()
MANDATORY composable — place under every yield/return figure
Text: "* Modelled estimate — actual results vary by field conditions"
Style: bodySmall, italic, ColorOnSurfaceTertiary (0xFF9E9E9E)

ScenarioCard.kt:
@Composable fun ScenarioCard(scenario: Scenario, isRecommended: Boolean)
Corner: 12.dp
Border: 2.dp ColorPrimary if recommended else ColorOutline
Show: label, action, yield with ModelledEstimateLabel, cost, risk badge
Tappable to expand details

FeedbackRow.kt:
@Composable fun FeedbackRow(onThumbsUp: () -> Unit, onThumbsDown: () -> Unit)
"Was this helpful?" text + 👍 48.dp + 👎 48.dp

CREATE FILE: ui/screens/AdvisoryResultScreen.kt
LazyColumn with all composables in this order:
1. TopAppBar: "Advisory" title + back button + share icon
2. ConfidenceBadge + RiskLevelBadge side by side
3. DiagnosisSummary text (headlineSmall)
4. EvidenceCard (expandable, default expanded)
5. ScenarioCards (A/B/C) — recommended one highlighted
6. ActionCard for recommended action
7. WhatWouldChangeSection (expandable, lightbulb icon, ColorWarningBg)
8. SchemeMatchCards if any scheme_matches present
9. FeedbackRow
10. SourcesSection showing knowledge document titles

IMPORTANT: Every yield and return number MUST have ModelledEstimateLabel directly below it.
The absence of ModelledEstimateLabel next to any number is a critical safety failure.

CREATE FILE: ui/screens/AdvisoryResultViewModel.kt
- advisory: StateFlow<AdvisoryResponse?>
- isLoading: StateFlow<Boolean>
- error: StateFlow<String?>
- Load from cache first, then API
- onFeedback(positive: Boolean) — POST to /api/v1/advisories/{id}/feedback

VERIFY: Show AdvisoryResultScreen.kt. Confirm ModelledEstimateLabel appears after each yield/return number.
```

---

## PROMPT P3-05: Home Screen and Offline Mode

```
Agri-SAGE Android. Screen phase.

TASK: Create Home screen, offline mode, and WorkManager sync.

CREATE FILE: ui/screens/HomeScreen.kt
Complete implementation matching spec:

TopAppBar:
  Background: ColorPrimaryDark
  Left: farm name in headlineSmall white
  Right: sync AnimatedIcon (spins when syncing), notification bell with unread badge

AlertBanner (show ONLY when not CONNECTED):
  OFFLINE: cloud_off icon + "ഇന്റർനെറ്റ് ഇല്ല — സേവ് ചെയ്ത ഡേറ്റ" on ColorOfflineBanner
  LIMITED: warning icon + "Limited connection" on ColorWarningBg

MorningBriefingCard:
  Background: ColorPrimaryLight, corner 16.dp, padding 16.dp
  Row 1: crop icon + stage + days label (headlineSmall) + speaker IconButton (48.dp)
  Row 2: risk level indicator + risk description
  Row 3: weather_cloudy icon + 2-word weather summary
  Row 4: actions icon + recommended action text (bodyLarge bold)
  Speaker button: trigger TTS reading of briefing text

2x2 ActionTile Grid:
  LazyVerticalGrid 2 columns, spacing 12.dp, horizontal padding 16.dp
  Each tile: min 100.dp height, corner 12.dp, white bg, elevation 2.dp
  Tiles:
    "Check Crop" (photo_camera icon, ColorPrimary) → navigate to CameraRoute
    "Farm Weather" (partly_cloudy_day icon, ColorSecondary) → navigate to WeatherRoute
    "View Risks" (warning icon, ColorRiskMedium) → navigate to RiskRoute
    "My Schemes" (account_balance icon, ColorSchemeText) → navigate to SchemeRoute

BottomNavBar:
  5 items: Home | Farm | Diagnose | Alerts | Profile
  Diagnose center item: elevated circular ColorPrimary background
  Selected indicator: ColorPrimary underline

CREATE FILE: ui/screens/HomeViewModel.kt
- activeFarm: StateFlow<FarmEntity?>
- activecrCycle: StateFlow<CropCycleEntity?>
- morningBriefing: StateFlow<CachedAdvisoryEntity?>
- connectivityStatus: StateFlow<ConnectivityStatus> (ONLINE/LIMITED/OFFLINE)
- syncStatus: StateFlow<SyncStatus>
Connectivity via ConnectivityManager network callback.
Morning briefing: load from Room where type='morning_briefing', refresh if > 12 hours old AND connected.

CREATE FILE: data/sync/SyncWorker.kt
CoroutineWorker implementation:

doWork():
1. Check connectivity — if not connected: return Result.retry()
2. Query sync_queue ordered by priority ASC, retryCount ASC
3. For each item:
   Call matching API endpoint based on entityType (farm/field/observation/image)
   On HTTP 200: delete from sync_queue
   On failure: increment retryCount
   If retryCount > 5: skip item (log warning), do not retry
4. After queue empty:
   GET /api/v1/sync/delta?last_sync={last_sync_timestamp}
   Apply delta updates to Room
5. Check knowledge cache version from server — if different, download new knowledge cache
6. Return Result.success()

Schedule in Application class:
PeriodicWorkRequest every 15 minutes, constraint NETWORK_CONNECTED, EXPONENTIAL backoff

CREATE FILE: ml/OfflineAdvisoryEngine.kt
fun generateOfflineAdvisory(imagePath: String, crop: String): CachedAdvisoryEntity
1. Run ONNX vision inference (singleton session)
2. Load offline_templates_ml.json from assets/
3. Fill template slots: {crop, disease, confidence, action}
4. Return CachedAdvisoryEntity with isOffline=true
5. Always include banner: "ഇന്റർനെറ്റ് ഇല്ല — ഓഫ്‌ലൈൻ വിശകലനം"

VERIFY: Show HomeScreen.kt. Show SyncWorker.kt.
Confirm AlertBanner only shown when NOT connected.
Confirm SyncWorker skips items with retryCount > 5.
```

---

# PHASE 4 — TESTING AND SECURITY

---

## PROMPT P4-01: Complete Test Suite

```
Agri-SAGE project. Testing phase.

TASK: Create the complete test suite. Never modify tests to make them pass — fix the implementation.

CREATE FILE: tests/conftest.py
Fixtures:
async_client: httpx AsyncClient with test FastAPI app
test_db: creates test database, runs all 17 migrations, yields AsyncSession, drops tables after test
test_user_token(phone): creates test user, runs OTP verify, returns JWT access token
test_farm(user_id): creates test farm owned by user, returns farm dict

CREATE FILE: pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
filterwarnings = ignore::DeprecationWarning

CREATE FILE: tests/unit/test_crop_stage.py
class TestGDDCalculation:
    def test_rice_gdd_formula(self):
        gdd = compute_gdd(tmax=30.0, tmin=22.0, crop='rice')
        assert gdd == pytest.approx(16.0, abs=0.1)  # ((30+22)/2) - 10 = 16

    def test_gdd_below_base_returns_zero(self):
        gdd = compute_gdd(tmax=12.0, tmin=8.0, crop='rice')
        assert gdd == 0.0  # Never negative

    def test_banana_different_base_temp(self):
        gdd = compute_gdd(tmax=30.0, tmin=22.0, crop='banana')
        assert gdd == pytest.approx(11.0, abs=0.1)  # ((30+22)/2) - 15 = 11

    def test_rice_tillering_at_260_gdd(self):
        result = CropStageAgent().estimate_stage(crop='rice', cumulative_gdd=260.0)
        assert result.stage_code == 'tillering'
        assert result.disease_vulnerability == 'high'

    def test_rice_flowering_at_700_gdd(self):
        result = CropStageAgent().estimate_stage(crop='rice', cumulative_gdd=700.0)
        assert result.stage_code == 'flowering'
        assert result.disease_vulnerability == 'critical'

CREATE FILE: tests/unit/test_weather_agent.py
class TestDFI:
    def test_high_humidity_wet_days_high_dfi(self):
        dfi = compute_dfi(humidity_pct=88.0, temperature_c=26.0, consecutive_wet_days=4)
        assert dfi > 0.7

    def test_dry_conditions_low_dfi(self):
        dfi = compute_dfi(humidity_pct=45.0, temperature_c=35.0, consecutive_wet_days=0)
        assert dfi < 0.3

    def test_dfi_clamped_between_0_and_1(self):
        dfi = compute_dfi(humidity_pct=100.0, temperature_c=25.0, consecutive_wet_days=14)
        assert 0.0 <= dfi <= 1.0

    def test_dfi_formula_correct(self):
        # humidity>80 → 0.4, 20<=temp<=30 → 0.3, wet_days/7*0.3
        dfi = compute_dfi(humidity_pct=85.0, temperature_c=25.0, consecutive_wet_days=7)
        expected = 0.4 + 0.3 + (7/7)*0.3
        assert dfi == pytest.approx(expected, abs=0.01)

CREATE FILE: tests/safety/test_critic_safety.py
ALL THESE TESTS MUST PASS — These protect farmers from unsafe recommendations:

class TestCriticSafetyBlocks:
    async def test_unknown_pesticide_blocked(self):
        rec = {'product_name': 'FakeChemical_XYZ_9999', 'crop': 'rice', 'dosage': 1.0}
        safe, issues = await critic.safety_checker.run_all_checks(rec)
        assert safe == False
        assert any('BLOCK' in issue for issue in issues)

    async def test_valid_pesticide_passes(self):
        # Tricyclazole 75 WP is CIB&RC registered for rice blast
        rec = {'product_name': 'Tricyclazole 75 WP', 'crop': 'rice', 'dosage': 0.6}
        safe, issues = await critic.safety_checker.run_all_checks(rec)
        assert safe == True

    async def test_wrong_crop_registration_blocked(self):
        rec = {'product_name': 'Tricyclazole 75 WP', 'crop': 'banana', 'dosage': 0.6}
        safe, issues = await critic.safety_checker.run_all_checks(rec)
        assert safe == False

    async def test_conflicting_evidence_no_treatment(self):
        state = make_conflicting_state(vision_label='rice_blast', dfi=0.1, wet_days=0)
        result = await critic_agent.run(state)
        assert result['critic_result']['confidence_state'] == 'CONFLICTING_EVIDENCE'
        assert result['critic_result']['safe_to_act'] == False

    async def test_uncertain_confidence_no_treatment(self):
        state = make_low_confidence_state(confidence_score=0.35)
        result = await critic_agent.run(state)
        assert result['critic_result']['confidence_state'] == 'UNCERTAIN'
        assert result['critic_result']['safe_to_act'] == False

    async def test_modelled_estimate_label_always_present(self):
        # Any advisory with yield numbers must have modelled_estimate=True
        advisory = create_test_advisory_with_yield()
        for scenario in advisory['scenarios']:
            assert scenario.get('modelled_estimate') == True

    async def test_expired_scheme_not_returned(self):
        state = make_state_with_expired_scheme()
        result = await scheme_agent.run(state)
        names = [s['scheme_name'] for s in result.get('scheme_matches', [])]
        assert 'ExpiredTestScheme2020' not in names

    async def test_mandatory_caveat_always_present(self):
        state = make_valid_state_with_scheme()
        result = await scheme_agent.run(state)
        for match in result.get('scheme_matches', []):
            assert 'mandatory_caveat' in match
            assert 'concerned authority' in match['mandatory_caveat']

CREATE FILE: tests/security/test_rls.py
async def test_user_cannot_read_other_users_farm(async_client, test_db):
    token_a = await create_test_user_token('+919000000001')
    token_b = await create_test_user_token('+919000000002')
    resp = await async_client.post('/api/v1/farms',
        json={'name': 'Farm A', 'location_lat': 10.0, 'location_lon': 76.0},
        headers={'Authorization': f'Bearer {token_a}'})
    farm_id = resp.json()['id']
    resp = await async_client.get(f'/api/v1/farms/{farm_id}',
        headers={'Authorization': f'Bearer {token_b}'})
    assert resp.status_code == 404  # MUST be 404 — not 403, not 200

async def test_user_cannot_access_other_users_advisory(async_client, test_db):
    advisory_id = await create_advisory_for_user_a()
    resp = await async_client.get(f'/api/v1/advisories/{advisory_id}',
        headers={'Authorization': f'Bearer {token_b}'})
    assert resp.status_code == 404

CREATE FILE: tests/performance/locustfile.py
from locust import HttpUser, task, between

class AgriSAGEFarmerUser(HttpUser):
    wait_time = between(2, 8)

    def on_start(self):
        resp = self.client.post('/api/v1/auth/verify-otp',
            json={'phone': f'+9199{self.user_id:08d}', 'otp': '123456'})
        if resp.status_code == 200:
            self.headers = {'Authorization': f"Bearer {resp.json()['access_token']}"}

    @task(3)
    def get_farms(self):
        self.client.get('/api/v1/farms', headers=self.headers)

    @task(2)
    def get_weather(self):
        self.client.get('/api/v1/weather/10.12/76.34', headers=self.headers)

    @task(1)
    def generate_advisory(self):
        self.client.post('/api/v1/diagnose',
            json={'observation_id': 'test-obs-id'},
            headers=self.headers)

VERIFY: Run pytest tests/safety/ -v — show all 8 tests pass.
Run pytest tests/security/ -v — show RLS test passes with 404 response.
```

---

## PROMPT P4-02: Security Audit and Deployment Scripts

```
Agri-SAGE project. Security and DevOps phase.

TASK: Create security audit scripts and deployment configuration.

CREATE FILE: scripts/security_audit.py
Run 6 automated security checks — print PASS or FAIL for each:

Check 1: No hardcoded secrets
  grep -rn patterns like SECRET_KEY="actual_value" in all .py and .kt files
  FAIL if any match found

Check 2: .env not in git
  Run: git ls-files --error-unmatch .env
  FAIL if .env is tracked

Check 3: Dependency vulnerabilities
  Run pip-audit on requirements.txt
  FAIL if any CRITICAL CVEs found

Check 4: RLS enabled on all user tables
  Connect to DB, run:
  SELECT tablename FROM pg_tables WHERE rowsecurity=true
  FAIL if any of [farms, fields, crop_cycles, observations, images, advisories, notifications] not in result

Check 5: Rate limiting active
  Send 6 POST requests to /auth/send-otp with same phone
  FAIL if 6th request does not return 429

Check 6: SQL injection strings rejected
  POST /farms with name containing SQL: "'; DROP TABLE farms; --"
  FAIL if not returned 400 or 422 (must be rejected by validation)

CREATE FILE: scripts/smoke_tests.py
3 checks after deployment:
1. GET /health → assert status=200 AND response.db_connected==True
2. GET /api/v1/weather/10.12/76.34 (with test JWT) → assert status=200
3. POST /api/v1/auth/send-otp {phone: "+919999999999"} → assert status=200

Print PASS/FAIL per check. sys.exit(1) if any fail.

CREATE FILE: scripts/deploy.sh
#!/bin/bash
set -e
echo "Deploying Agri-SAGE..."
cd /home/ubuntu/agrisage
git pull origin main
docker compose -f docker-compose.prod.yml pull
docker compose -f docker-compose.prod.yml up -d --no-deps backend
sleep 5
alembic upgrade head
python scripts/smoke_tests.py
echo "Deployment complete"

CREATE FILE: nginx/nginx.conf
Rate limiting and reverse proxy:
http {
    limit_req_zone $binary_remote_addr zone=general:10m rate=20r/s;
    limit_req_zone $binary_remote_addr zone=diagnose:10m rate=2r/s;
    limit_req_zone $binary_remote_addr zone=otp:10m rate=5r/10m;

    server {
        listen 80;
        server_name api.agrisage.in;
        return 301 https://$server_name$request_uri;
    }

    server {
        listen 443 ssl;
        server_name api.agrisage.in;

        location /api/v1/auth/send-otp {
            limit_req zone=otp burst=2 nodelay;
            limit_req_status 429;
            proxy_pass http://localhost:8000;
        }

        location /api/v1/diagnose {
            limit_req zone=diagnose burst=5 nodelay;
            limit_req_status 429;
            proxy_pass http://localhost:8000;
        }

        location / {
            limit_req zone=general burst=40 nodelay;
            proxy_pass http://localhost:8000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
        }
    }
}

CREATE FILE: docker-compose.prod.yml
Production docker-compose with:
- no --reload flag on uvicorn
- restart: always on backend
- json-file logging with max-size: 10m
- explicit database volume
- no port exposure for DB (internal only)

VERIFY: Run scripts/security_audit.py — show output for all 6 checks.
Show nginx.conf rate limiting configuration.
```

---

# PHASE 5 — EXPERT DASHBOARD AND MONETIZATION

---

## PROMPT P5-01: Expert Review Dashboard

```
Agri-SAGE project. Expert dashboard phase.

TASK: Create the React web expert review dashboard.

Create apps/web-expert/ as a React 18 + Vite + TailwindCSS project.

CREATE FILE: apps/web-expert/src/App.tsx
Three pages using React Router v6:
1. /login — POST to /api/v1/auth/verify-otp, store JWT in localStorage
2. /dashboard — list of advisories needing review
3. /review/:advisory_id — full advisory detail + review form

CREATE FILE: apps/web-expert/src/pages/Dashboard.tsx
GET /api/v1/expert/queue (requires JWT with tier='expert')
Display advisories in a table:
  Columns: Created At | Crop | Confidence State | Farmer District | Actions
  Actions: "Review" button → navigate to /review/:id
Filter controls: by confidence_state, by crop
Show count of pending reviews

CREATE FILE: apps/web-expert/src/pages/ReviewDetail.tsx
Full advisory display + verdict form:
  Show: diagnosis, confidence state, all evidence, all scenarios
  Show: vision result, weather indicators, crop stage, knowledge sources
  Verdict form:
    verdict: select (correct / partially_correct / incorrect / insufficient_data)
    corrected_diagnosis: text input (if verdict != correct)
    notes: textarea
  Submit: POST /api/v1/expert/reviews/{advisory_id}

CREATE backend endpoints for expert dashboard:
GET /api/v1/expert/queue
  Require tier='expert' in JWT
  Return advisories ordered by created_at, not yet reviewed
  Include: observation details, farm district, confidence state

POST /api/v1/expert/reviews/{advisory_id}
  Require tier='expert'
  Accept: verdict, corrected_diagnosis, notes
  Store in expert_reviews table
  Return: {review_id, message: "Review submitted"}

VERIFY: Show Dashboard.tsx and expert queue endpoint. Confirm expert tier check is enforced.
```

---

## PROMPT P5-02: Subscription and Payment

```
Agri-SAGE project. Monetization phase.

TASK: Implement Razorpay subscription integration.

CREATE backend subscription endpoints:

POST /api/v1/subscriptions/create-order
Input: {plan: "kisan_basic" | "kisan_pro" | "agronomist"}
Prices: kisan_basic=4900 (₹49), kisan_pro=14900 (₹149), agronomist=49900 (₹499)
  Call Razorpay Orders API with amount in paise, currency=INR
  Return: {order_id, amount, currency, key_id}

POST /api/v1/subscriptions/verify-payment
Input: {razorpay_payment_id, razorpay_order_id, razorpay_signature}
  Compute HMAC-SHA256: hash(order_id + "|" + payment_id, key=RAZORPAY_SECRET_KEY)
  Verify signature matches
  If valid:
    Update user.subscription_tier and user.subscription_expires
    Log audit event: subscription_activated
  Return: {success: true, plan: str, expires_at: str}

POST /api/v1/subscriptions/webhook
  Verify Razorpay webhook signature from X-Razorpay-Signature header
  Handle events: payment.captured, subscription.charged, subscription.cancelled
  On payment.captured: update user subscription
  Return: {"status": "ok"}

Advisory limit enforcement middleware:
  Check user.advisories_this_month against tier limits:
    free: max 5
    kisan_basic, kisan_pro, agronomist: unlimited
  If over limit: raise HTTPException(429, "Monthly advisory limit reached. Upgrade to continue.")
  Reset counter monthly (check advisories_reset_at, update to today + reset count)

CREATE Android SubscriptionScreen.kt:
  Show 4 tier cards with prices
  Featured card (Pro): gold border, slightly elevated
  Payment button: "Pay with UPI / Card"
  On tap: call /create-order, launch Razorpay Android SDK
  On payment success: call /verify-payment, refresh subscription status

VERIFY: Show create-order endpoint. Confirm HMAC signature verification in verify-payment.
Confirm advisory limit check happens before running the pipeline.
```

---

# PHASE 6 — FINAL VERIFICATION

---

## PROMPT P6-01: Production Readiness Check

```
Agri-SAGE project. Final phase.

TASK: Run complete production readiness verification.

Run ALL of these checks and report PASS/FAIL for each:

BACKEND CHECKS:
1. docker compose up -d — both services healthy
2. curl localhost:8000/health → {status:ok, db_connected:true}
3. docker exec db psql -U agrisage -c '\dt' → shows all 20 tables
4. alembic upgrade head → "Already at head" (all migrations run)
5. pytest tests/unit/ -v → all pass
6. pytest tests/safety/ -v → ALL 8 safety tests pass
7. pytest tests/security/ -v → RLS test returns 404
8. python scripts/security_audit.py → all 6 checks PASS
9. cat .gitignore | grep '.env' → .env is listed
10. git ls-files | grep '.env' → empty (not tracked)

AI MODEL CHECKS:
11. Run evaluate_vision_model.py → macro_f1 >= 0.82 AND ECE <= 0.12
12. Run retrieval_benchmark.py → recall@5 > 0.80 on 20 test queries
13. Generate 10 test advisories → confirm zero invented product names
14. Verify all advisories: UNCERTAIN/INSUFFICIENT_DATA → safe_to_act=False

DATABASE CHECKS:
15. SELECT tablename FROM pg_tables WHERE rowsecurity=true → shows 7 tables
16. SELECT COUNT(*) FROM knowledge_chunks → > 100 rows
17. SELECT COUNT(*) FROM schemes WHERE valid_until > NOW() → at least 3 schemes
18. SELECT COUNT(*) FROM knowledge_documents WHERE status='PUBLISHED' → > 10 documents

ANDROID CHECKS:
19. App builds release APK without errors
20. App opens on emulator — no crash on HomeScreen
21. Camera opens and quality indicator changes color based on image quality
22. Offline mode: airplane mode → camera → advisory shows offline banner in Malayalam

For any FAIL: explain exact error and exact fix. Fix the issue, then re-run that check.
Do not proceed to launch until all 22 checks show PASS.

FINAL OUTPUT:
Show complete check report with PASS/FAIL per item.
If all pass: print "AGRI-SAGE PRODUCTION READY — LAUNCH APPROVED"
If any fail: print "BLOCKERS FOUND — DO NOT LAUNCH" with list of failures.
```

---

## FINAL NOTE FOR THE AI EXECUTING THESE PROMPTS

```
You are building a world-class agricultural AI platform that will:
- Serve 146 million smallholder farmers across India
- Expand to Southeast Asia, Africa, and Latin America
- Compete with large global AgriTech companies from day one of launch

Every prompt above must be executed to production quality:
- No placeholder code
- No "TODO" comments in critical paths
- No hardcoded test values in production code
- Every safety check must be real and functional
- Every Malayalam string must be accurate
- Every LLM prompt must be copied verbatim

The farmers who use this platform make life-or-death decisions
based on its recommendations. Build accordingly.
```

---

# APPENDIX A — COMPATIBILITY RULES FOR EXISTING CODE
## Read This Before Executing ANY Prompt Above

---

## WHAT IS ALREADY BUILT — DO NOT TOUCH

From the repository analysis, the following already exists:
- `index.html` — existing HTML file — DO NOT overwrite
- `public/` folder — existing public assets — ADD to it, never delete
- `src/` folder — existing source files — ADD to it, never delete
- `package.json` — existing config — MERGE new fields, never overwrite
- `.gitignore` — existing file — APPEND missing lines, never overwrite
- `.env.local` — existing env file — ADD missing variables, never overwrite
- `components.json` — existing component config — DO NOT touch
- `README.md` — existing readme — UPDATE by appending, never overwrite
- GitHub Pages deployment — already working — DO NOT touch `.github/workflows/`
- `functions/analyze-interview/` folder — separate project — DO NOT touch
- `Zebec_ai/` folder — separate project — DO NOT touch
- `lazy_terminal(useless_project)/` folder — DO NOT touch

---

## COMPATIBILITY RULE — PASTE THIS AT THE TOP OF EVERY PROMPT

```
IMPORTANT COMPATIBILITY RULES — READ BEFORE EXECUTING:

1. CHECK BEFORE CREATE: Before creating any file, check if it already exists.
   If it exists: READ it first, then EXTEND or MERGE — never overwrite blindly.
   Command to check: ls -la [filepath]

2. PACKAGE.JSON: Never replace package.json. Only ADD missing dependencies.
   Use: npm install [package] to add new packages.
   Never remove existing scripts or dependencies.

3. .GITIGNORE: Never replace. Only append missing lines at the bottom.
   Check first: cat .gitignore | grep [term]

4. EXISTING FOLDERS: Never delete or rename any existing folder.
   Only create new folders and files inside or alongside them.

5. ENV FILES: Never overwrite .env or .env.local.
   Only add missing variables. Check first: cat .env.local | grep [VAR_NAME]

6. HTML/CSS/JS FILES: If index.html already exists and has content,
   do not overwrite it. Create new files alongside it.

7. GITHUB WORKFLOWS: If .github/workflows/ already has files that work,
   do not modify them unless specifically asked. Add new workflow files only.

8. MIGRATIONS: Never re-run a migration that already exists.
   Always check: alembic current — before running alembic upgrade head.

9. DATABASE TABLES: Never DROP or ALTER existing tables.
   Only CREATE IF NOT EXISTS. Use new migrations for schema changes.

10. ANDROID DEPENDENCIES: Never remove existing dependencies from build.gradle.kts.
    Only add new ones. Check for conflicts before adding.

VERIFICATION STEP: After any file creation or modification, show:
- What files were created (new)
- What files were modified (changed)
- What files were skipped (already existed and kept)
This prevents any accidental overwrites.
```

---

## PROMPT EXECUTION CHECKLIST — RUN BEFORE EACH PROMPT

Before giving any prompt to the AI, answer these questions:

```
□ Did I paste the CONTEXT BLOCK at the top of this prompt?
□ Did I paste the COMPATIBILITY RULES at the top of this prompt?
□ Have I told the AI which files already exist in my project?
□ Have I verified the previous prompt completed without errors?
□ Am I giving ONE prompt at a time (not multiple)?
```

---

## HOW TO TELL THE AI WHAT ALREADY EXISTS

At the start of each session, run this in your terminal and paste the output to the AI:

```bash
# Run this in your project root — paste output to AI before each prompt
find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' \
  -not -path '*/__pycache__/*' -not -path '*/venv/*' \
  | sort | head -100
```

Then tell the AI:

```
Here are the files that already exist in my project:
[paste output here]

Do NOT overwrite any of these files.
Only create files that are NOT in this list.
For files that DO exist, read them first and only ADD what is missing.
```

---

## SAFE MODIFICATION PATTERNS — USE THESE EXACT APPROACHES

### Adding to package.json safely
```
Read the existing package.json first.
Then ADD only these missing dependencies to the dependencies section:
[list new deps]
Do not remove any existing entry.
Show me the diff of what changed.
```

### Adding to .gitignore safely
```
Read the existing .gitignore first.
Then APPEND these lines at the bottom if they are not already present:
[list new entries]
Do not remove any existing entry.
```

### Adding to existing Python file safely
```
Read backend/[filename].py first.
Then ADD this function/class to the file without changing existing functions:
[new code]
Show me exactly what was added and where.
```

### Adding to existing Kotlin file safely
```
Read mobile/android/.../[filename].kt first.
Then ADD this composable/function to the file without changing existing code:
[new code]
Show me exactly what was added and where.
```

### Adding environment variables safely
```
Read the existing .env.local file.
Then ADD only these variables that are NOT already present:
[list variables]
Do not modify or delete any existing variable.
```

---

## CONFLICT RESOLUTION — WHEN AI TRIES TO OVERWRITE

If the AI starts replacing existing file content, stop it immediately with:

```
STOP. Do not overwrite [filename].
That file already exists with important content.
Read the current file first using: cat [filename]
Then only ADD what is missing from the task.
Show me what you are going to change BEFORE making changes.
```

---

## PHASE-BY-PHASE — WHAT TO SKIP IF ALREADY DONE

Use this table to skip prompts for work already completed:

| Prompt | Skip If |
|--------|---------|
| P0-01: Project Structure | Main folders already exist |
| P0-02: Docker + Requirements | docker-compose.yml and requirements.txt already exist |
| P0-03: FastAPI Core | backend/main.py already exists |
| P0-04: Migrations | alembic/versions/ folder has migration files |
| P0-05: Auth | backend/api/v1/auth.py already exists |
| P0-06: Farm CRUD | backend/api/v1/farms.py already exists |
| P0-07: CI/CD | .github/workflows/ci.yml already exists |
| P1-01: LangGraph | backend/agents/orchestrator.py already exists |
| P1-02: Vision/Critic | backend/agents/vision.py has real implementation |
| P1-03: Weather/Stage | backend/agents/weather.py has real implementation |
| P1-04: Decision/Explain | backend/agents/explanation.py has real implementation |
| P1-05: Diagnose endpoint | backend/api/v1/diagnose.py already exists |
| P1-06: Scheme/Monitoring | backend/agents/scheme.py has real implementation |
| P2-01: Data Files | backend/data/disease_classes.json already exists |
| P2-02: Knowledge Pipeline | backend/knowledge/ingestion.py already exists |
| P2-03: Vision Training | backend/ml/vision/train.py already exists |
| P3-01: Android Setup | mobile/android/app/build.gradle.kts already exists |
| P3-02: Room DB | AgriSAGEDatabase.kt already exists |
| P3-03: Camera Screen | CameraScreen.kt already exists |
| P3-04: Advisory Screen | AdvisoryResultScreen.kt already exists |
| P3-05: Home Screen | HomeScreen.kt already exists |
| P4-01: Tests | tests/safety/ folder has test files |
| P4-02: Security Scripts | scripts/security_audit.py already exists |
| P5-01: Expert Dashboard | apps/web-expert/src/ already exists |
| P5-02: Payments | backend/api/v1/ has subscription endpoint |

### How to check quickly before running any prompt:
```bash
# Run this before each prompt to know what exists
ls backend/api/v1/          # backend endpoints
ls backend/agents/           # agent files
ls alembic/versions/         # migrations
ls tests/safety/             # safety tests
ls mobile/android/app/src/main/java/com/agrisage/app/ui/screens/  # Android screens
```

---

## PARTIAL BUILD PROMPT — FOR FILES ALREADY PARTIALLY BUILT

If a file exists but is just a stub (empty class, placeholder), use this pattern:

```
Read [filename] — it currently exists as a stub/placeholder.
Keep everything that already exists in that file.
Implement ONLY the following functions that are currently empty:
- [function 1]: [what it should do]
- [function 2]: [what it should do]
Do not change any function that already has real implementation.
Show me a diff of exactly what you added.
```

---

## WEBSITE FRONTEND — SPECIAL COMPATIBILITY NOTE

The Agri-SAGE website frontend is partially built with:
- index.html (existing)
- src/ folder (existing)
- public/ folder (existing)
- GitHub Pages deployment working

When building website features:
```
My Agri-SAGE website already has these files built:
[list what exists: index.html, src/, public/]

Add the [SECTION NAME] section to the website.
Rules:
1. Do not touch index.html if it already has the hero section
2. Add new sections BELOW existing content
3. Do not change existing CSS variables or color tokens
4. Maintain the existing dark theme (#0A0F0A background)
5. All new sections must match the existing design system
6. After adding, show me what changed
```

---

## FINAL MASTER PROMPT — USE THIS FOR FIRST SESSION WITH NEW AI

If starting fresh with a new AI model on this project, give this first:

```
I am building Agri-SAGE — a world-class agricultural AI platform for
India's 146 million smallholder farmers. I have a 2673-line master
build prompt file that guides the entire build.

Before I give you any tasks, here is what already exists in my project:
[RUN: find . -type f -not -path '*/node_modules/*' -not -path '*/.git/*' | sort]
[PASTE OUTPUT HERE]

Rules for this entire project:
1. Never overwrite files that already exist — read first, then extend
2. Never remove existing code — only add new code
3. Always check if a file exists before creating it
4. Show me what changed after every task
5. One task at a time — complete and verify before next
6. All technology versions are fixed — use only the versions specified
7. All LLM prompts in the agents must be copied verbatim — no paraphrasing
8. All safety checks are non-negotiable — never skip them
9. Free tools only — no paid APIs
10. October 1, 2026 is the demo deadline — prioritize MVP features

I will now give you tasks from the master build guide one at a time.
Confirm you understand all rules before I give the first task.
```

