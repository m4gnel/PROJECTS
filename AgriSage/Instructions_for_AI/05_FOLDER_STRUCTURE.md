# 05_FOLDER_STRUCTURE.md — Agri-SAGE Complete File Tree
# ⚠️ ONLY CREATE FILES LISTED HERE. DO NOT INVENT NEW FILES OR FOLDERS.

## Root Structure
```
agri-sage/
├── brain/                          # AI agent context — READ ONLY, never modify
│   ├── 00_MASTER_RULES.md
│   ├── 01_PRD.md
│   ├── 02_ARCHITECTURE.md
│   ├── 03_DATA_MODEL.md
│   ├── 04_API_CONTRACT.md
│   ├── 05_FOLDER_STRUCTURE.md      ← THIS FILE
│   ├── 06_PINNED_DEPENDENCIES.md
│   ├── 07_AGENT_CONTRACTS.md
│   ├── 08_ANDROID_CONTRACTS.md
│   ├── 09_DATABASE_SCHEMA.md
│   └── 10_API_RESPONSE_SHAPES.md
│
├── backend/                        # FastAPI application (M1 + M2 territory)
│   ├── app/
│   │   ├── __init__.py             # empty
│   │   ├── main.py                 # FastAPI app, lifespan, router includes
│   │   ├── config.py               # pydantic-settings Settings class
│   │   ├── database.py             # async engine, session factory, get_db dep
│   │   │
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── __init__.py
│   │   │   ├── base.py             # DeclarativeBase, timestamps mixin
│   │   │   ├── farmer.py           # Farmer model
│   │   │   ├── field.py            # Field model
│   │   │   ├── crop.py             # CropRecord model
│   │   │   ├── alert.py            # Alert model
│   │   │   ├── chat.py             # ChatSession, ChatMessage models
│   │   │   └── knowledge.py        # KnowledgeChunk (pgvector) model
│   │   │
│   │   ├── schemas/                # Pydantic v2 request/response schemas
│   │   │   ├── __init__.py
│   │   │   ├── farmer.py           # FarmerCreate, FarmerRead, FarmerUpdate
│   │   │   ├── field.py            # FieldCreate, FieldRead, FieldUpdate
│   │   │   ├── chat.py             # ChatRequest, ChatResponse, MessageRead
│   │   │   ├── weather.py          # WeatherCurrent, WeatherForecast, WeatherDay
│   │   │   ├── alert.py            # AlertRead, AlertCreate, AlertSeverity enum
│   │   │   ├── advisory.py         # AdvisoryRequest, AdvisoryResponse
│   │   │   └── auth.py             # TokenResponse, LoginRequest, RegisterRequest
│   │   │
│   │   ├── routers/                # FastAPI APIRouter endpoints
│   │   │   ├── __init__.py
│   │   │   ├── auth.py             # POST /auth/register, POST /auth/token
│   │   │   ├── farmers.py          # GET/PUT /farmers/me, GET /farmers/{id}
│   │   │   ├── fields.py           # CRUD /fields/
│   │   │   ├── chat.py             # POST /chat/, WS /chat/ws/{session_id}
│   │   │   ├── weather.py          # GET /weather/current, GET /weather/forecast
│   │   │   ├── alerts.py           # GET /alerts/, POST /alerts/mark-read
│   │   │   └── advisory.py         # POST /advisory/ask
│   │   │
│   │   ├── agents/                 # LangGraph agent nodes (14 total)
│   │   │   ├── __init__.py
│   │   │   ├── state.py            # AgriState TypedDict definition
│   │   │   ├── graph.py            # Builds and exports the compiled graph
│   │   │   ├── weather_agent.py    # Agent 01: weather data + analysis
│   │   │   ├── soil_agent.py       # Agent 02: soil type + fertility
│   │   │   ├── crop_agent.py       # Agent 03: crop health + calendar
│   │   │   ├── pest_agent.py       # Agent 04: pest/disease alerts
│   │   │   ├── market_agent.py     # Agent 05: commodity prices
│   │   │   ├── dssat_agent.py      # Agent 06: DSSAT crop simulation
│   │   │   ├── satellite_agent.py  # Agent 07: NDVI from NASA
│   │   │   ├── irrigation_agent.py # Agent 08: irrigation schedule
│   │   │   ├── fertilizer_agent.py # Agent 09: fertilizer plan
│   │   │   ├── harvest_agent.py    # Agent 10: harvest timing prediction
│   │   │   ├── market_timing_agent.py # Agent 11: when to sell
│   │   │   ├── rag_agent.py        # Agent 12: KAU PDF vector search
│   │   │   ├── translator_agent.py # Agent 13: ML/TA/HI translation
│   │   │   ├── alert_agent.py      # Agent 14: alert generation + priority
│   │   │   └── orchestrator.py     # routes query → right agents
│   │   │
│   │   ├── pipelines/              # Scheduled data ingestion (runs every N hours)
│   │   │   ├── __init__.py
│   │   │   ├── scheduler.py        # APScheduler setup, job registration
│   │   │   ├── weather_pipeline.py # Open-Meteo → DB (every 1 hr)
│   │   │   ├── soil_pipeline.py    # NBSS API → DB (every 24 hr)
│   │   │   ├── satellite_pipeline.py # NASA EarthData → DB (every 24 hr)
│   │   │   ├── pest_pipeline.py    # NBAIR RSS → alerts DB (every 6 hr)
│   │   │   ├── market_pipeline.py  # data.gov.in → DB (every 12 hr)
│   │   │   └── knowledge_pipeline.py # KAU PDFs → pgvector (on startup)
│   │   │
│   │   └── utils/
│   │       ├── __init__.py
│   │       ├── embeddings.py       # multilingual-e5-large embed() function
│   │       ├── gemini.py           # Gemini Flash API wrapper
│   │       ├── dssat_runner.py     # subprocess DSSAT runner
│   │       ├── auth.py             # JWT create/verify helpers
│   │       └── pagination.py       # PageParams, paginate() helper
│   │
│   ├── migrations/                 # Alembic
│   │   ├── env.py                  # async migration env
│   │   ├── script.py.mako
│   │   └── versions/
│   │       └── 001_initial_schema.py # all tables + pgvector extension
│   │
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── conftest.py             # pytest fixtures, test DB, test client
│   │   ├── test_auth.py
│   │   ├── test_weather.py
│   │   ├── test_chat.py
│   │   ├── test_agents.py
│   │   ├── test_pipelines.py
│   │   └── test_advisory.py
│   │
│   ├── kau_pdfs/                   # KAU crop advisory PDFs (committed to repo)
│   │   └── .gitkeep                # PDFs go here, not tracked
│   │
│   ├── requirements.txt            # EXACT versions (from brain/06)
│   ├── requirements-dev.txt        # test/lint tools only
│   ├── Dockerfile
│   ├── alembic.ini
│   ├── .env.example                # template — no secrets
│   └── railway.toml                # Railway deployment config
│
├── android/                        # Android app (M3 territory)
│   ├── app/
│   │   ├── src/
│   │   │   ├── main/
│   │   │   │   ├── java/
│   │   │   │   │   └── com/
│   │   │   │   │       └── agrisage/
│   │   │   │   │           └── app/
│   │   │   │   │               ├── AgriSageApplication.kt   # Hilt @HiltAndroidApp
│   │   │   │   │               ├── MainActivity.kt          # single activity
│   │   │   │   │               │
│   │   │   │   │               ├── navigation/
│   │   │   │   │               │   ├── Screen.kt            # sealed class routes
│   │   │   │   │               │   └── AppNavHost.kt        # NavHost + all composables
│   │   │   │   │               │
│   │   │   │   │               ├── ui/
│   │   │   │   │               │   ├── theme/
│   │   │   │   │               │   │   ├── Color.kt         # design tokens
│   │   │   │   │               │   │   ├── Theme.kt         # MaterialTheme
│   │   │   │   │               │   │   └── Type.kt          # typography
│   │   │   │   │               │   │
│   │   │   │   │               │   ├── components/          # reusable UI pieces
│   │   │   │   │               │   │   ├── BottomNavBar.kt
│   │   │   │   │               │   │   ├── WeatherChip.kt
│   │   │   │   │               │   │   ├── AlertCard.kt
│   │   │   │   │               │   │   ├── ChatBubble.kt
│   │   │   │   │               │   │   ├── FieldCard.kt
│   │   │   │   │               │   │   ├── QuickActionButton.kt
│   │   │   │   │               │   │   ├── SeverityBadge.kt
│   │   │   │   │               │   │   └── LoadingOverlay.kt
│   │   │   │   │               │   │
│   │   │   │   │               │   └── screens/
│   │   │   │   │               │       ├── splash/
│   │   │   │   │               │       │   └── SplashScreen.kt
│   │   │   │   │               │       ├── onboarding/
│   │   │   │   │               │       │   ├── OnboardingScreen.kt
│   │   │   │   │               │       │   └── OnboardingViewModel.kt
│   │   │   │   │               │       ├── home/
│   │   │   │   │               │       │   ├── HomeScreen.kt
│   │   │   │   │               │       │   └── HomeViewModel.kt
│   │   │   │   │               │       ├── advisor/
│   │   │   │   │               │       │   ├── AdvisorScreen.kt
│   │   │   │   │               │       │   └── AdvisorViewModel.kt
│   │   │   │   │               │       ├── fields/
│   │   │   │   │               │       │   ├── FieldsScreen.kt
│   │   │   │   │               │       │   ├── FieldDetailScreen.kt
│   │   │   │   │               │       │   └── FieldsViewModel.kt
│   │   │   │   │               │       ├── weather/
│   │   │   │   │               │       │   ├── WeatherScreen.kt
│   │   │   │   │               │       │   └── WeatherViewModel.kt
│   │   │   │   │               │       ├── alerts/
│   │   │   │   │               │       │   ├── AlertsScreen.kt
│   │   │   │   │               │       │   └── AlertsViewModel.kt
│   │   │   │   │               │       └── profile/
│   │   │   │   │               │           ├── ProfileScreen.kt
│   │   │   │   │               │           └── ProfileViewModel.kt
│   │   │   │   │               │
│   │   │   │   │               ├── data/
│   │   │   │   │               │   ├── local/
│   │   │   │   │               │   │   ├── AppDatabase.kt       # Room DB
│   │   │   │   │               │   │   ├── dao/
│   │   │   │   │               │   │   │   ├── WeatherDao.kt
│   │   │   │   │               │   │   │   ├── AlertDao.kt
│   │   │   │   │               │   │   │   ├── ChatDao.kt
│   │   │   │   │               │   │   │   └── FieldDao.kt
│   │   │   │   │               │   │   └── entity/
│   │   │   │   │               │   │       ├── WeatherEntity.kt
│   │   │   │   │               │   │       ├── AlertEntity.kt
│   │   │   │   │               │   │       ├── ChatMessageEntity.kt
│   │   │   │   │               │   │       └── FieldEntity.kt
│   │   │   │   │               │   │
│   │   │   │   │               │   ├── remote/
│   │   │   │   │               │   │   ├── ApiService.kt        # Retrofit interface
│   │   │   │   │               │   │   ├── AuthInterceptor.kt   # JWT injector
│   │   │   │   │               │   │   └── dto/
│   │   │   │   │               │   │       ├── WeatherDto.kt
│   │   │   │   │               │   │       ├── AlertDto.kt
│   │   │   │   │               │   │       ├── ChatDto.kt
│   │   │   │   │               │   │       ├── FieldDto.kt
│   │   │   │   │               │   │       └── AuthDto.kt
│   │   │   │   │               │   │
│   │   │   │   │               │   └── repository/
│   │   │   │   │               │       ├── WeatherRepository.kt
│   │   │   │   │               │       ├── AlertRepository.kt
│   │   │   │   │               │       ├── ChatRepository.kt
│   │   │   │   │               │       ├── FieldRepository.kt
│   │   │   │   │               │       └── AuthRepository.kt
│   │   │   │   │               │
│   │   │   │   │               ├── domain/
│   │   │   │   │               │   ├── model/
│   │   │   │   │               │   │   ├── Weather.kt
│   │   │   │   │               │   │   ├── Alert.kt
│   │   │   │   │               │   │   ├── ChatMessage.kt
│   │   │   │   │               │   │   ├── Field.kt
│   │   │   │   │               │   │   └── Farmer.kt
│   │   │   │   │               │   └── usecase/
│   │   │   │   │               │       ├── GetWeatherUseCase.kt
│   │   │   │   │               │       ├── SendMessageUseCase.kt
│   │   │   │   │               │       ├── GetAlertsUseCase.kt
│   │   │   │   │               │       └── GetFieldsUseCase.kt
│   │   │   │   │               │
│   │   │   │   │               └── di/
│   │   │   │   │                   ├── AppModule.kt             # singletons
│   │   │   │   │                   ├── DatabaseModule.kt        # Room DB
│   │   │   │   │                   └── NetworkModule.kt         # Retrofit + OkHttp
│   │   │   │   │
│   │   │   │   ├── res/
│   │   │   │   │   ├── drawable/
│   │   │   │   │   │   ├── ic_launcher_foreground.xml
│   │   │   │   │   │   ├── ic_agrisage_logo.xml   # SVG vector
│   │   │   │   │   │   └── bg_splash.xml           # splash gradient
│   │   │   │   │   ├── values/
│   │   │   │   │   │   ├── strings.xml             # English strings
│   │   │   │   │   │   ├── colors.xml              # resource colors
│   │   │   │   │   │   └── themes.xml
│   │   │   │   │   ├── values-ml/
│   │   │   │   │   │   └── strings.xml             # Malayalam strings
│   │   │   │   │   ├── values-ta/
│   │   │   │   │   │   └── strings.xml             # Tamil strings
│   │   │   │   │   └── values-hi/
│   │   │   │   │       └── strings.xml             # Hindi strings
│   │   │   │   │
│   │   │   │   └── AndroidManifest.xml
│   │   │   │
│   │   │   └── test/
│   │   │       └── java/com/agrisage/app/
│   │   │           ├── WeatherViewModelTest.kt
│   │   │           ├── AdvisorViewModelTest.kt
│   │   │           └── RepositoryTest.kt
│   │   │
│   │   ├── build.gradle.kts        # app-level build file
│   │   ├── google-services.json    # Firebase (add manually — not in git)
│   │   └── proguard-rules.pro
│   │
│   ├── gradle/
│   │   └── libs.versions.toml      # VERSION CATALOG (from brain/06)
│   ├── build.gradle.kts            # project-level build file
│   └── settings.gradle.kts
│
├── .github/
│   └── workflows/
│       ├── backend-ci.yml          # pytest on push to dev/m1*, dev/m2*
│       ├── android-ci.yml          # gradle build on push to dev/m3*
│       └── deploy-railway.yml      # deploy on push to main
│
├── .gitignore
└── README.md
```

---

## Files You Must NEVER Create
- Any file ending in `_old.py`, `_backup.py`, `_v2.py`, `_copy.py`
- Any file named `test_app.py` in the root (tests go in backend/tests/ only)
- Any file named `app.py` (it's `main.py`)
- Any file named `models.py` (models are per-entity in models/ folder)
- Any file named `utils.py` (utils are per-purpose in utils/ folder)
- Any `__pycache__/` directories (auto-generated, in .gitignore)
- Any `.env` file (use .env.example template only)

## Total File Count Expectation
- backend/: ~75 Python files
- android/: ~65 Kotlin files  
- brain/: 11 Markdown files
- CI/configs: ~10 files
- TOTAL: ~161 files (not hundreds — if you see more, junk was created)
