# PHASE_PROMPTS_V2.md — Agri-SAGE Build Prompts (Complete Rewrite)
# ⚠️ USE THESE PROMPTS INSTEAD OF THE OLD ONES. THESE ARE FINAL.

## Why These Are Different
Old prompts: "Build the backend" → AI invents everything
New prompts: "Read brain/X first, create THESE specific files with THESE exact patterns"

Each prompt:
1. Starts with "Read these brain/ files first"
2. Lists EXACTLY which files to create
3. Specifies EXACT patterns to follow
4. Ends with a VALIDATION CHECKLIST — do not proceed until all pass

---

# MASTER RUNNER PROMPT (Paste this at the start of EVERY new Cline/Cursor session)

```
AGRI-SAGE SESSION START — READ THIS BEFORE ANYTHING

You are building Agri-SAGE, a Kerala agricultural AI advisor.
Before writing a single line of code, run these commands:

  cat brain/00_MASTER_RULES.md
  cat brain/05_FOLDER_STRUCTURE.md
  git status

Rules you MUST follow:
1. Only create files listed in brain/05_FOLDER_STRUCTURE.md
2. Only use package versions in brain/06_PINNED_DEPENDENCIES.md
3. Follow agent signatures in brain/07_AGENT_CONTRACTS.md exactly
4. Follow Android contracts in brain/08_ANDROID_CONTRACTS.md exactly
5. Use database schema from brain/09_DATABASE_SCHEMA.md exactly
6. Return JSON from brain/10_API_RESPONSE_SHAPES.md exactly
7. NEVER add packages not in brain/06
8. NEVER create files not in brain/05
9. NEVER modify a file you were not explicitly told to modify
10. After each task, run: git add [specific files] && git status && git commit -m "feat: ..."

What is the current task? [describe your specific task here]
```

---

# PHASE 1 PROMPT — Backend Foundation
# (Run on branch: dev/m1-backend)

```
PHASE 1: Agri-SAGE Backend Foundation

FIRST — run these commands before coding:
  cat brain/00_MASTER_RULES.md
  cat brain/05_FOLDER_STRUCTURE.md
  cat brain/06_PINNED_DEPENDENCIES.md
  cat brain/07_AGENT_CONTRACTS.md
  cat brain/09_DATABASE_SCHEMA.md
  git status

YOU MUST CREATE EXACTLY THESE FILES (no others):

backend/
├── requirements.txt              ← COPY EXACTLY from brain/06
├── requirements-dev.txt          ← COPY EXACTLY from brain/06
├── .env.example                  ← COPY EXACTLY from brain/06
├── Dockerfile                    ← COPY EXACTLY from brain/06
├── railway.toml                  ← COPY EXACTLY from brain/06
├── alembic.ini                   ← standard alembic init
├── app/__init__.py               ← empty file
├── app/main.py                   ← see pattern below
├── app/config.py                 ← see pattern below
├── app/database.py               ← see pattern below
├── app/models/__init__.py        ← empty
├── app/models/base.py            ← DeclarativeBase + TimestampMixin
├── app/models/farmer.py          ← Farmer SQLAlchemy model
├── app/models/field.py           ← Field model
├── app/models/crop.py            ← CropRecord model
├── app/models/alert.py           ← Alert model
├── app/models/chat.py            ← ChatSession + ChatMessage models
├── app/models/knowledge.py       ← KnowledgeChunk with Vector(1024) column
├── app/schemas/__init__.py       ← empty
├── app/schemas/auth.py           ← TokenResponse, LoginRequest, RegisterRequest
├── app/schemas/farmer.py         ← FarmerCreate, FarmerRead, FarmerUpdate
├── app/schemas/field.py          ← FieldCreate, FieldRead, FieldUpdate
├── app/schemas/chat.py           ← ChatRequest, ChatResponse, MessageRead
├── app/schemas/weather.py        ← WeatherCurrent, WeatherForecast, WeatherDay
├── app/schemas/alert.py          ← AlertRead, AlertCreate, AlertSeverity
├── app/schemas/advisory.py       ← AdvisoryRequest, AdvisoryResponse
├── app/routers/__init__.py       ← empty
├── app/routers/auth.py           ← POST /auth/register, POST /auth/token
├── app/routers/farmers.py        ← GET/PUT /farmers/me
├── app/routers/fields.py         ← CRUD /fields/
├── app/routers/chat.py           ← POST /chat/
├── app/routers/weather.py        ← GET /weather/current + /weather/forecast
├── app/routers/alerts.py         ← GET /alerts/, POST /alerts/mark-read
├── app/routers/advisory.py       ← POST /advisory/ask
├── app/utils/__init__.py         ← empty
├── app/utils/auth.py             ← create_access_token, verify_token helpers
├── app/utils/pagination.py       ← PageParams dataclass, paginate() helper
├── migrations/env.py             ← async Alembic env
├── migrations/script.py.mako     ← standard mako template
└── migrations/versions/001_initial_schema.py  ← COPY EXACTLY from brain/09

EXACT CODE PATTERNS:

--- app/main.py ---
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import auth, farmers, fields, chat, weather, alerts, advisory

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="Agri-SAGE API",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(farmers.router, prefix="/farmers", tags=["farmers"])
app.include_router(fields.router, prefix="/fields", tags=["fields"])
app.include_router(chat.router, prefix="/chat", tags=["chat"])
app.include_router(weather.router, prefix="/weather", tags=["weather"])
app.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
app.include_router(advisory.router, prefix="/advisory", tags=["advisory"])

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}
--- END app/main.py ---

--- app/config.py ---
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    
    DATABASE_URL: str
    GEMINI_API_KEY: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440
    OPEN_METEO_BASE_URL: str = "https://api.open-meteo.com/v1"
    NASA_EARTHDATA_BASE_URL: str = "https://appeears.earthdatacloud.nasa.gov"
    DATA_GOV_IN_API_KEY: str = ""
    NBAIR_RSS_URL: str = "https://www.nbair.res.in/rss/pest-alerts.xml"
    NBSS_API_URL: str = "https://www.nbsslup.in/api"
    KAU_PDF_DIR: str = "./kau_pdfs"
    RAILWAY_URL: str = "http://localhost:8000"
    ENVIRONMENT: str = "development"

settings = Settings()
--- END app/config.py ---

--- app/database.py ---
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .config import settings
from .models.base import Base

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def init_db():
    async with engine.begin() as conn:
        # Tables are created via Alembic migrations, not here
        pass

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
--- END app/database.py ---

ALL ROUTER RESPONSES MUST MATCH brain/10_API_RESPONSE_SHAPES.md EXACTLY.
ALL MODELS MUST MATCH brain/09_DATABASE_SCHEMA.md EXACTLY.

PHASE 1 VALIDATION CHECKLIST (must all be true before committing):
□ uvicorn app.main:app --reload starts without error
□ GET /health returns {"status": "ok", "version": "1.0.0"}
□ alembic upgrade head runs without error
□ POST /auth/register creates a farmer and returns token
□ POST /auth/token returns token for existing farmer
□ GET /farmers/me returns farmer profile (with valid token)
□ POST /fields/ creates a field
□ GET /fields/ lists farmer's fields
□ All response shapes match brain/10_API_RESPONSE_SHAPES.md exactly
□ No files created outside brain/05_FOLDER_STRUCTURE.md

After all checks pass:
git add backend/
git status
git commit -m "feat(phase-1): backend foundation — FastAPI + PostgreSQL + auth + CRUD"
git push origin dev/m1-backend
```

---

# PHASE 2 PROMPT — 14 Agents + Data Pipelines
# (Run on branch: dev/m1-backend and dev/m4-integrations)

```
PHASE 2: Agri-SAGE Agents + Data Pipelines

FIRST — run these commands before coding:
  cat brain/00_MASTER_RULES.md
  cat brain/07_AGENT_CONTRACTS.md
  git status

YOU MUST CREATE EXACTLY THESE FILES:

backend/app/agents/
├── __init__.py
├── state.py           ← COPY EXACTLY from brain/07 "AgriState TypedDict"
├── graph.py           ← COPY EXACTLY from brain/07 "build_graph()"
├── orchestrator.py    ← orchestrator_node + should_continue from brain/07
├── weather_agent.py   ← weather_node
├── soil_agent.py      ← soil_node
├── crop_agent.py      ← crop_node
├── pest_agent.py      ← pest_node
├── market_agent.py    ← market_node
├── dssat_agent.py     ← dssat_node
├── satellite_agent.py ← satellite_node
├── irrigation_agent.py ← irrigation_node
├── fertilizer_agent.py ← fertilizer_node
├── harvest_agent.py    ← harvest_node
├── market_timing_agent.py ← market_timing_node
├── rag_agent.py        ← rag_node
├── translator_agent.py ← translator_node
└── alert_agent.py      ← alert_node

backend/app/pipelines/
├── __init__.py
├── scheduler.py         ← APScheduler with jobs below
├── weather_pipeline.py  ← Open-Meteo → weather_cache table (every 1hr)
├── soil_pipeline.py     ← NBSS → fields.soil_type (every 24hr)
├── satellite_pipeline.py ← NASA EarthData NDVI → fields.last_ndvi (every 24hr)
├── pest_pipeline.py     ← NBAIR RSS → alerts table (every 6hr)
├── market_pipeline.py   ← data.gov.in → market_prices table (every 12hr)
└── knowledge_pipeline.py ← KAU PDFs → knowledge_chunks + embeddings (on startup)

backend/app/utils/
├── embeddings.py  ← multilingual-e5-large embed() function
├── gemini.py      ← Gemini Flash wrapper
└── dssat_runner.py ← subprocess runner

CRITICAL PATTERNS:

--- app/utils/embeddings.py ---
from sentence_transformers import SentenceTransformer
import numpy as np

_model = None

def get_model() -> SentenceTransformer:
    global _model
    if _model is None:
        _model = SentenceTransformer('intfloat/multilingual-e5-large')
    return _model

def embed_query(text: str) -> list[float]:
    """For queries: prefix with 'query: '"""
    model = get_model()
    embedding = model.encode(f"query: {text}", normalize_embeddings=True)
    return embedding.tolist()

def embed_passage(text: str) -> list[float]:
    """For documents/passages: prefix with 'passage: '"""
    model = get_model()
    embedding = model.encode(f"passage: {text}", normalize_embeddings=True)
    return embedding.tolist()
--- END embeddings.py ---

--- app/utils/gemini.py ---
import google.generativeai as genai
from .config import settings

genai.configure(api_key=settings.GEMINI_API_KEY)

async def ask_gemini(prompt: str, system_prompt: str = "") -> str:
    """Call Gemini Flash. Returns text. On error returns fallback string."""
    try:
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=system_prompt if system_prompt else None
        )
        response = await model.generate_content_async(prompt)
        return response.text
    except Exception as e:
        return f"Advisory unavailable: {str(e)}"
--- END gemini.py ---

AGENT IMPLEMENTATION RULES:
- Each agent function signature: async def {name}_node(state: AgriState) -> dict
- Each agent must add its name to agents_completed: return {"agents_completed": ["{name}"]}
- Each agent must NEVER raise exceptions — catch all errors, add to error_messages
- Weather agent uses httpx.AsyncClient to call Open-Meteo (no API key needed)
- Pest agent uses feedparser.parse(settings.NBAIR_RSS_URL) synchronously in executor
- RAG agent uses: SELECT content FROM knowledge_chunks ORDER BY embedding <=> $1 LIMIT 5
- Translator agent uses gemini.py with: system_prompt="Translate to {language}. Use simple words."
- Alert agent synthesizes all agent_findings into advisory_text using Gemini

SCHEDULER SETUP:
--- app/pipelines/scheduler.py ---
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from .weather_pipeline import run_weather_pipeline
from .pest_pipeline import run_pest_pipeline
from .market_pipeline import run_market_pipeline
from .soil_pipeline import run_soil_pipeline
from .satellite_pipeline import run_satellite_pipeline

scheduler = AsyncIOScheduler(timezone="Asia/Kolkata")

def setup_scheduler():
    scheduler.add_job(run_weather_pipeline, 'interval', hours=1, id='weather')
    scheduler.add_job(run_pest_pipeline, 'interval', hours=6, id='pest')
    scheduler.add_job(run_market_pipeline, 'interval', hours=12, id='market')
    scheduler.add_job(run_soil_pipeline, 'interval', hours=24, id='soil')
    scheduler.add_job(run_satellite_pipeline, 'interval', hours=24, id='satellite')
    return scheduler
--- END scheduler.py ---

Update app/main.py lifespan to include:
  from .pipelines.scheduler import setup_scheduler
  from .pipelines.knowledge_pipeline import run_knowledge_pipeline
  
  @asynccontextmanager
  async def lifespan(app: FastAPI):
      await init_db()
      await run_knowledge_pipeline()   # index KAU PDFs on startup
      scheduler = setup_scheduler()
      scheduler.start()
      yield
      scheduler.shutdown()

Update app/routers/chat.py to use:
  from ..agents.graph import agri_graph
  Use the graph invocation pattern from brain/07 "How to Call the Graph"

PHASE 2 VALIDATION CHECKLIST:
□ python -c "from app.agents.graph import agri_graph; print('graph ok')" runs without error
□ All 14 agent files exist in backend/app/agents/
□ All 6 pipeline files exist in backend/app/pipelines/
□ POST /chat/ with a Malayalam test query returns advisory_text (not empty string)
□ POST /chat/ response matches brain/10 shape exactly
□ weather_pipeline.py calls Open-Meteo and stores in weather_cache table
□ pest_pipeline.py parses NBAIR RSS feed
□ knowledge_pipeline.py embeds KAU PDFs into knowledge_chunks table
□ No new packages installed beyond brain/06_PINNED_DEPENDENCIES.md

git commit -m "feat(phase-2): 14 agents + 6 data pipelines + LangGraph graph"
git push origin dev/m1-backend
```

---

# PHASE 3 PROMPT — Android App (All 8 Screens)
# (Run on branch: dev/m3-android)

```
PHASE 3: Agri-SAGE Android App

FIRST — run these commands before coding:
  cat brain/00_MASTER_RULES.md
  cat brain/05_FOLDER_STRUCTURE.md
  cat brain/06_PINNED_DEPENDENCIES.md
  cat brain/08_ANDROID_CONTRACTS.md
  git status

YOU MUST CREATE EXACTLY THESE FILES:
(refer to brain/05_FOLDER_STRUCTURE.md for the complete android/ tree)

BUILD FILES (copy from brain/06 EXACTLY):
- android/gradle/libs.versions.toml
- android/build.gradle.kts
- android/app/build.gradle.kts
- android/settings.gradle.kts

THEME FILES (copy tokens from brain/00 EXACTLY):
- android/app/src/main/java/com/agrisage/app/ui/theme/Color.kt
- android/app/src/main/java/com/agrisage/app/ui/theme/Theme.kt
- android/app/src/main/java/com/agrisage/app/ui/theme/Type.kt

NAVIGATION (copy from brain/08 EXACTLY):
- Screen.kt — the sealed class with all 9 routes
- AppNavHost.kt — NavHost with all 9 composable destinations

SCREENS (implement as per brain/08 contracts):
1. SplashScreen.kt + (no ViewModel — logic is inline)
2. OnboardingScreen.kt + OnboardingViewModel.kt
3. HomeScreen.kt + HomeViewModel.kt
4. AdvisorScreen.kt + AdvisorViewModel.kt
5. FieldsScreen.kt + FieldDetailScreen.kt + FieldsViewModel.kt
6. WeatherScreen.kt + WeatherViewModel.kt
7. AlertsScreen.kt + AlertsViewModel.kt
8. ProfileScreen.kt + ProfileViewModel.kt

COMPONENTS (implement these 8):
- BottomNavBar.kt  ← COPY EXACTLY from brain/08
- WeatherChip.kt
- AlertCard.kt (severity color-coded: RED/GOLD/BLUE/GREEN from brain/00 tokens)
- ChatBubble.kt (user=right SageGreen500, AI=left SurfaceDim)
- FieldCard.kt
- QuickActionButton.kt
- SeverityBadge.kt
- LoadingOverlay.kt

DATA LAYER (use DTOs from brain/10 JSON shapes):
- ApiService.kt  ← COPY EXACTLY from brain/08
- AuthInterceptor.kt ← injects "Authorization: Bearer <token>" header
- All DTO data classes must match brain/10 JSON field names exactly

DI MODULES:
- AppModule.kt — provides DataStore, coroutine dispatchers
- DatabaseModule.kt — provides Room database and all DAOs
- NetworkModule.kt — provides Retrofit + OkHttp with AuthInterceptor

EXACT PATTERNS TO FOLLOW:

--- MainActivity.kt --- COPY EXACTLY from brain/08 ---

--- Color.kt ---
// Use EXACT hex values from brain/00_MASTER_RULES.md design tokens
val SageGreen900 = Color(0xFF1B4332)
val SageGreen700 = Color(0xFF2D6A4F)
... (all 13 tokens)

--- BottomNavBar.kt --- COPY EXACTLY from brain/08 ---

SCREEN IMPLEMENTATION RULES:
- All screens follow: @Composable fun XxxScreen(navController: NavHostController)
- All ViewModels follow: @HiltViewModel class XxxViewModel @Inject constructor(...)
- All UiState follows: data class XxxUiState(... isLoading: Boolean = false, error: String? = null)
- Use collectAsStateWithLifecycle() to observe StateFlow (NOT collectAsState())
- Minimum touch target: 48dp height for all buttons and chips
- All text sizes in sp (never dp for text)
- Language strings: en strings in values/strings.xml, ml in values-ml/strings.xml

PHASE 3 VALIDATION CHECKLIST:
□ ./gradlew assembleDebug builds without error
□ APK size < 25MB
□ SplashScreen shows for 2 seconds then navigates correctly
□ OnboardingScreen 3 pages work, language selection works
□ HomeScreen shows weather chip + quick actions grid + alerts strip
□ AdvisorScreen sends message and shows response (connect to running backend)
□ FieldsScreen shows map + field list, FAB opens add dialog
□ WeatherScreen shows current + 7-day forecast
□ AlertsScreen shows alerts with correct severity colors
□ ProfileScreen shows farmer info + preferences toggles
□ BottomNavBar switches between all 5 main screens correctly
□ All 4 languages (ml/en/ta/hi) show correct strings
□ No hardcoded colors (all from Color.kt tokens)
□ No hardcoded strings (all in strings.xml)

git commit -m "feat(phase-3): Android app — all 8 screens + navigation + data layer"
git push origin dev/m3-android
```

---

# PHASE 4 PROMPT — Deployment (Railway + CI/CD + FCM)
# (Run on branch: dev/m4-integrations)

```
PHASE 4: Agri-SAGE Deployment

FIRST — run:
  cat brain/00_MASTER_RULES.md
  git status

FILES TO CREATE:
- railway.toml          ← COPY from brain/06
- Dockerfile            ← COPY from brain/06
- .github/workflows/backend-ci.yml
- .github/workflows/android-ci.yml
- .github/workflows/deploy-railway.yml

--- backend-ci.yml ---
name: Backend CI
on:
  push:
    branches: ['dev/m1-*', 'dev/m2-*', 'dev/m5-*']
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: pgvector/pgvector:pg16
        env:
          POSTGRES_PASSWORD: testpassword
          POSTGRES_DB: agrisage_test
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: pip install -r backend/requirements.txt -r backend/requirements-dev.txt
      - run: cd backend && pytest tests/ -v --cov=app --cov-report=xml
        env:
          DATABASE_URL: postgresql+asyncpg://postgres:testpassword@localhost:5432/agrisage_test
          GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }}
          SECRET_KEY: test-secret-key-32-chars-minimum
--- END backend-ci.yml ---

--- android-ci.yml ---
name: Android CI
on:
  push:
    branches: ['dev/m3-*']
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with:
          distribution: 'temurin'
          java-version: '17'
      - run: cd android && ./gradlew assembleDebug
      - run: cd android && ./gradlew test
--- END android-ci.yml ---

--- deploy-railway.yml ---
name: Deploy to Railway
on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
      - run: npm install -g @railway/cli
      - run: cd backend && railway up --service agrisage-backend
        env:
          RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }}
--- END deploy-railway.yml ---

FCM SETUP (backend side):
- Install: firebase-admin==6.5.0 (ADD to requirements.txt)
- Create: backend/app/utils/fcm.py
  - async def send_push_notification(farmer_id: str, title: str, body: str)
  - Fetches FCM token from farmers table (add fcm_token column to migration 001)
  - Uses firebase_admin.messaging.Message

PHASE 4 VALIDATION CHECKLIST:
□ railway up succeeds without error
□ GET https://your-app.up.railway.app/health returns {"status": "ok"}
□ POST https://your-app.up.railway.app/auth/register works from Android emulator
□ GitHub Actions backend-ci.yml runs green on push
□ GitHub Actions android-ci.yml runs green on push

git commit -m "feat(phase-4): Railway deployment + GitHub Actions CI/CD + FCM"
git push origin dev/m4-integrations
```

---

# PHASE 5 PROMPT — QA, Demo Prep, APK Signing
# (Run on branch: dev/m5-tests)

```
PHASE 5: Agri-SAGE QA + Demo

FIRST — run:
  cat brain/00_MASTER_RULES.md
  git status

FILES TO CREATE:
- backend/tests/conftest.py       ← pytest fixtures + test DB
- backend/tests/test_auth.py      ← register + login tests
- backend/tests/test_weather.py   ← weather endpoint tests
- backend/tests/test_chat.py      ← chat POST + agent invocation tests
- backend/tests/test_agents.py    ← individual agent unit tests
- backend/tests/test_pipelines.py ← pipeline mock tests
- backend/tests/test_advisory.py  ← advisory endpoint tests
- android/app/src/test/ tests     ← ViewModel unit tests

--- conftest.py ---
import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.main import app
from app.database import get_db
from app.models.base import Base

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:testpassword@localhost:5432/agrisage_test"

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture
async def test_db(test_engine):
    AsyncTestSession = async_sessionmaker(test_engine, expire_on_commit=False)
    async with AsyncTestSession() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
    app.dependency_overrides.clear()
--- END conftest.py ---

TARGET COVERAGE: 90% for backend/app/ directory
RUN: pytest tests/ --cov=app --cov-report=term-missing --cov-fail-under=90

SIGNED APK:
- keystore: generate with keytool, store in android/app/agrisage-release.jks
- DO NOT commit .jks to git — add to .gitignore
- Configure signing in app/build.gradle.kts release buildType
- Final APK must be < 25MB
- Test on real device: Android 9+ (API 28)

DEMO SCRIPT (5 minutes for HR presentation):
1. [0:00] Open app → Splash → Onboarding (language=Malayalam)
2. [0:45] Home Dashboard → show weather chip, alerts
3. [1:15] Tap "Ask Advisor" → type: "ഇന്ന് ഞാൻ ഏത് വളം ഇടണം?" (which fertilizer today?)
4. [2:00] Show AI response in Malayalam with confidence score
5. [2:30] Navigate to My Fields → show NDVI indicator
6. [3:00] Navigate to Weather → 7-day forecast
7. [3:30] Navigate to Alerts → show CRITICAL/WARNING severity badges
8. [4:00] Switch language to English on Profile → go back to Advisor → same question in English
9. [4:30] Show Railway deployment URL responding to API calls
10. [5:00] Q&A

PHASE 5 VALIDATION CHECKLIST:
□ pytest tests/ --cov=app --cov-fail-under=90 passes
□ Signed APK size < 25MB
□ App works on Android 9 (API 28) physical device
□ All 4 languages show correct UI strings (no English fallback in Malayalam mode)
□ Offline mode: Home + Weather (cached) work without internet
□ 5-minute demo script runs without crashes
□ All API calls in demo hit live Railway URL (not localhost)

git commit -m "feat(phase-5): 90%+ test coverage + signed APK + demo ready"
git push origin dev/m5-tests
```

---

## COMMON AI AGENT FAILURE PATTERNS AND HOW TO STOP THEM

| Failure | Why It Happens | Prevention |
|---------|---------------|------------|
| Creates `app.py` instead of `main.py` | Guesses a common name | brain/05 lists `main.py` explicitly |
| Uses `@app.on_event("startup")` | Training data has old patterns | brain/00 shows lifespan pattern |
| Adds `psycopg2` instead of `asyncpg` | Default for SQLAlchemy | brain/06 pins `asyncpg==0.29.0` |
| Creates 20+ agent files | Invents agents not in spec | brain/07 lists exactly 14 agents |
| Uses `Scaffold(...)` without `BottomNavBar` | Generic template | brain/08 shows BottomNavBar contract |
| Returns `{"data": {...}}` wrapper | Default REST convention | brain/10 shows flat response shapes |
| Uses `kapt` instead of `ksp` | Legacy Kotlin pattern | brain/06 uses ksp plugin only |
| `StateGraph(State)` without START/END | Old LangGraph API | brain/07 shows START/END pattern |
| Embeds without "query:"/"passage:" prefix | Ignores e5-large docs | brain/07 documents the prefix requirement |
| Creates `.env` with real keys | Fills in a template | brain/06 uses `.env.example` only |
