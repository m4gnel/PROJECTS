Agri-SAGE 🌾

Production Build Plan

🚀 Zero Budget · Real-Time Data · Production Grade

# Build What Actually Solves Farmer Problems

Complete production-ready build plan for Agri-SAGE — Scalable Agricultural Guidance Engine for Kerala smallholder farmers. Realtime data. Free APIs. 14 AI agents. Working Android app.

100%

Free-tier build

14

Specialized agents

8

Realtime data sources

3

Languages (ML/TA/EN)

4

Build phases

🎯

Foundation

## The Real Problems Agri-SAGE Solves

💡

**Why this matters** Kerala has 2.3 million smallholder farming families. Less than 12% access any digital advisory. Crop loss from preventable disease is ₹2,200 crore/year. We fix this with a free-to-use, Malayalam-speaking AI advisor on any Android phone.

#### ❌ No timely crop advice

Farmers wait days/weeks for a KAU extension officer visit. By then crop disease has spread. Agri-SAGE delivers sub-3-second answers 24/7.

#### ❌ Language barrier

Existing apps are English/Hindi only. Kerala farmers speak Malayalam (or Tamil). Our voice+text input works in native language.

#### ❌ No weather-crop linkage

Generic weather apps give temperature. We cross-reference realtime weather with crop disease risk models specific to each crop stage.

#### ❌ Market price blindness

Farmers sell at whatever the middleman says. We pull live APMC mandi prices daily so farmers know their crop's real value before selling.

#### ❌ Soil-blind recommendations

Generic advice ignores soil type. We integrate NBSS&LUP Kerala soil maps and personalize fertilizer/water recommendations per farm zone.

#### ❌ No crop simulation

Farmers guess sowing dates. DSSAT simulation backed by real weather data tells them exactly when to sow for maximum yield.

## 🌟 The Final Goal — North Star

**Agri-SAGE becomes the default AI agricultural advisor for every Kerala smallholder farmer** — accessible free on any Android phone, speaking Malayalam, giving real-time crop guidance backed by live weather, soil, pest, and market data — replacing the need for an extension officer for 90% of everyday farming decisions.

🌾 100K active farmers by Year 1 📱 Works on ₹5,000 Android phones 🗣️ Malayalam voice-first UX ⚡ Answers in \<3 seconds 🌧️ Realtime weather+pest alerts 💰 Free forever for farmers 🏛️ KAU/ICAR data integration 🤖 14 expert AI agents

📡

Phase 0 · Before Writing Code

## Realtime Data Sources — 100% Free

⚠️

**Do this first before any backend code.** Register for all API keys below. Each takes 5–15 min. Store them in a `.env` file. No keys = no realtime data. No realtime data = demo fails.

| Data Type | API / Source | What we fetch | Free Tier | Registration URL |
| --- | --- | --- | --- | --- |
| **☁️ Weather** | Open-Meteo FREE | Hourly temp, humidity, rainfall, UV, wind for any GPS coordinate. No key needed. | Unlimited, no auth | open-meteo.com |
| **🛰️ Satellite NDVI** | NASA EarthData FREE | MODIS NDVI crop health index per field every 8 days. Detect stress before visible. | Free, needs registration | earthdata.nasa.gov |
| **💰 Market Prices** | data.gov.in FREE | Daily APMC mandi prices for 200+ crops including coconut, rice, banana, rubber. | Free, needs API key | data.gov.in (register → Agriculture → APMC) |
| **🌧️ Rainfall Data** | IMD OpenData FREE | District-level daily rainfall from IMD stations. Monsoon tracking for Kerala. | Free JSON API | imdpune.gov.in / mosdac.gov.in |
| **🦟 Pest Alerts** | NBAIR RSS + KAU Bulletin FREE | National Bureau of Agricultural Insect Resources pest outbreak RSS feed. | Free RSS, no auth | nbair.res.in/PestAlerts |
| **🧪 Soil Data** | NBSS&LUP / IISR Kerala FREE | Kerala soil pH, texture, nutrient zones by district. Static dataset, ingest once. | Free download, GIS data | nbss.icar.gov.in |
| **🌿 Crop Advisory** | KAU Package of Practices FREE | KAU (Kerala Agricultural University) official PDF packages — scrape/embed into pgvector. | Publicly available PDFs | kau.in/package-of-practices |
| **🤖 LLM (AI brain)** | Gemini 1.5 Flash FREE | 15 req/min, 1M context — primary LLM for all 14 agents. Malayalam + English. | 15 RPM / 1M TPD free | aistudio.google.com |

🤖

Architecture

## 14 Specialized AI Agents — Live Data Mapping

🌦️ WeatherAgent

Fetches hourly forecast + generates 7-day crop risk summary

→ Open-Meteo API (realtime)

🌱 SoilAgent

Matches GPS to Kerala soil zone, returns pH + nutrients

→ NBSS pgvector lookup

🦟 PestAgent

Checks NBAIR alerts + correlates with current weather for risk score

→ NBAIR RSS (realtime)

💰 MarketAgent

Pulls today's APMC prices + generates sell/hold recommendation

→ data.gov.in (daily)

🌾 CropAdvisorAgent

RAG over KAU Package of Practices PDFs for crop-specific advice

→ pgvector + KAU docs

💧 IrrigationAgent

Calculates water need from weather ET₀ and crop stage

→ Open-Meteo + DSSAT

🌿 FertilizerAgent

NPK recommendations per soil zone + crop growth stage

→ Soil data + KAU docs

🛰️ NDVIAgent

Pulls satellite NDVI, detects stress zones in field

→ NASA EarthData (8-day)

📅 SowingAgent

Optimal sowing window using DSSAT + weather forecast

→ DSSAT + Open-Meteo

🗣️ TranslatorAgent

Malayalam ↔ English translation + voice-to-text normalization

→ Gemini Flash (multilingual)

🔀 RouterAgent

Parses farmer query intent, dispatches to correct specialist agents

→ LangGraph orchestrator

✍️ SynthesizerAgent

Combines all agent outputs into a single coherent farmer-friendly answer

→ Gemini Flash + context

🔔 AlertAgent

Proactive push: rain, pest outbreak, price drop, frost alerts

→ FCM (free) + all feeds

📊 AnalyticsAgent

Tracks per-farm season data, generates end-of-season yield report

→ PostgreSQL farm records

🏗️

Build Phases

## 4-Phase Production Build — Week by Week

1

Foundation + Realtime Data Pipeline

FastAPI backend · PostgreSQL+pgvector · 4 live API integrations · Brain folder

Weeks 1–2

1. 1

   #### Set up repo structure + brain/ folder (M1 — Magnel)

   Create `brain/00_MASTER_RULES.md`, `01_PRD.md`, `02_ARCHITECTURE.md`, `03_DATA_MODEL.md`, `04_API_CONTRACT.md`. This is the first file Cline reads every session. Without it, every AI coding session drifts.
2. 2

   #### FastAPI skeleton with lifespan pattern (M1)

   Scaffold `app/main.py` with startup/shutdown lifespan. Register routers: `/api/v1/chat`, `/api/v1/weather`, `/api/v1/market`, `/api/v1/alerts`. Health check endpoint at `/health`.
3. 3

   #### PostgreSQL 16 + pgvector setup (M2)

   Install pgvector extension. Create tables: `farms`, `farmers`, `queries`, `advisories`, `embeddings`. HNSW index on embedding column. Run Alembic migrations.
4. 4

   #### Weather data pipeline — Open-Meteo (M2)

   Implement `services/weather_service.py`. Fetch hourly data for lat/lon. Cache in Redis (or PostgreSQL) for 1 hour to avoid redundant calls. Return structured `WeatherContext` object.
5. 5

   #### Market price pipeline — data.gov.in (M3)

   Daily cron job (APScheduler) at 8 AM IST fetches APMC prices for Kerala districts. Store in `market_prices` table. Expose via `/api/v1/market?crop=coconut&district=Ernakulam`.
6. 6

   #### KAU document ingestion + pgvector RAG (M3)

   Download KAU Package of Practices PDFs. Chunk at 512 tokens with 50-token overlap. Embed with `multilingual-e5-large` (query:/passage: prefix). Store 1536-dim vectors in pgvector HNSW index.
7. 7

   #### Pest alert RSS ingestion (M4)

   Parse NBAIR pest alerts RSS feed every 6 hours. Match pest names to Kerala crops in a lookup table. Store in `pest_alerts` table with crop affinity score.
8. 8

   #### Soil data ingest + district lookup (M4)

   Parse NBSS&LUP Kerala soil shapefile. Convert to district-level JSON lookup. Load into `soil_zones` table. Query by district name — return pH, texture, N/P/K baseline.

2

LangGraph Agent Orchestration

14 agents wired · LangGraph 1.0.8 · MemorySaver · Parallel execution

Weeks 3–4

1. 1

   #### LangGraph state schema (M1)

   Define `AgriSageState` TypedDict with fields: `farmer_query`, `language`, `location`, `crop`, `weather_context`, `soil_context`, `pest_alerts`, `market_data`, `agent_outputs`, `final_answer`. This is the single source of truth passed between all nodes.
2. 2

   #### Router node + intent classifier (M1)

   RouterAgent uses Gemini Flash to classify query into one or more categories: WEATHER | PEST | MARKET | FERTILIZER | IRRIGATION | SOWING | GENERAL. Returns list of agents to activate. This drives conditional edges in LangGraph.
3. 3

   #### Parallel agent subgraph (M2)

   Use LangGraph `Send()` API for parallel fan-out. WeatherAgent, SoilAgent, PestAgent, MarketAgent run simultaneously. Wait for all with `join` node. Reduces latency from 12s → 3s.
4. 4

   #### Gemini Flash integration for all agent LLM calls (M3)

   Each agent uses `langchain_google_genai.ChatGoogleGenerativeAI` with `model="gemini-1.5-flash"`. Implement exponential backoff for rate limit handling (15 RPM free tier). System prompt loaded from `brain/05_AGENT_PROMPTS.md`.
5. 5

   #### MemorySaver for conversation continuity (M3)

   Each farmer session has a `thread_id = farmer_id`. LangGraph MemorySaver stores last 10 turns in memory. Farmer can say "aake paranja padathin ennenna?" (what happened to the crop I mentioned?) and agent recalls context.
6. 6

   #### Malayalam TranslatorAgent (M4)

   Pre-processing node: detect input language (Gemini Flash detects ML/TA/EN). If Malayalam, translate to English for agent processing. SynthesizerAgent responds in English. Post-processing TranslatorAgent converts final answer back to Malayalam.
7. 7

   #### DSSAT integration for SowingAgent (M5)

   Run DSSAT via subprocess from Python wrapper. Input: soil type + current weather forecast + crop variety. Output: optimal sowing window + predicted yield curve. Cache results in PostgreSQL for 24 hours.
8. 8

   #### Unit tests for all agents (M5)

   Pytest suite: mock all external APIs. Test each agent in isolation. Integration test: full query → final Malayalam answer end-to-end. Target: 80%+ coverage. Run on every PR via GitHub Actions (free).

3

Android App (Kotlin + Jetpack Compose)

Voice input · Chat UI · Offline fallback · Push alerts · Bilingual

Weeks 5–6

1. 1

   #### App skeleton + Navigation Compose 2.8.5 (M1)

   3 screens: `HomeScreen` (chat), `FarmDashboardScreen` (weather + market widget), `AlertsScreen`. Type-safe navigation with kotlinx-serialization. Destination sealed classes.
2. 2

   #### Malayalam voice input via SpeechRecognizer (M2)

   Android SpeechRecognizer with `LANGUAGE_MODEL_FREE_FORM` + `in-ML` locale. Transcribed text passed directly to chat API. No extra API cost — uses device on-device STT.
3. 3

   #### Chat UI with Compose LazyColumn (M2)

   Bubble UI: user messages right-aligned, Agri-SAGE responses left-aligned with green accent. Show loading shimmer while agent responds. Timestamp + agent icon per message. Malayalam text renders natively on Android.
4. 4

   #### Farm Dashboard — Live widgets (M3)

   Top widget: today's weather (temp, rain chance, humidity) from Open-Meteo via backend. Middle: today's coconut/rice/banana price from APMC. Bottom: active pest alerts. Refresh every 30 min via WorkManager.
5. 5

   #### Room 2.7.0 offline cache (M4)

   Cache last 20 queries + answers in Room DB. If no internet, show cached advice with "Last updated X mins ago" banner. Also cache weather data and market prices locally for 24-hour offline access.
6. 6

   #### FCM Push Notifications for AlertAgent (M4)

   AlertAgent triggers FCM message when: rain > 50mm forecast in 12h, pest outbreak in farmer's district, crop price drops > 15%, extreme heat advisory. FCM is free. Farmer registers crop + district on signup.
7. 7

   #### Farm registration onboarding (M5)

   3-step onboarding: (1) name + preferred language, (2) GPS location auto-detect or manual district select, (3) primary crops grown (multi-select). Stored in Room + synced to backend. Personalizes all subsequent advice.
8. 8

   #### Accessibility + low-end device optimization (M5)

   Target API 26 (Android 8). Test on 2GB RAM device. Lazy-load images. Compress API payloads with gzip. Font size follows system accessibility settings. Voice input as primary input method (many farmers low-literacy).

4

Deploy + Demo + Future Scale

Free hosting · GitHub Actions CI/CD · Live demo prep · Expansion roadmap

Weeks 7–8

1. 1

   #### Backend deploy — Railway.app or Render free tier (M1)

   Railway: 500 hours/month free. Deploy FastAPI Docker container. PostgreSQL 1GB free on Railway. Set all env vars in Railway dashboard. Expose public HTTPS URL for Android app to call.
2. 2

   #### GitHub Actions CI/CD pipeline (M1)

   On push to main: run pytest suite, lint with ruff, build Docker image, push to GitHub Container Registry (free), deploy to Railway. Android: build APK with Gradle on push, upload artifact for download.
3. 3

   #### Load test with Locust (M5)

   Simulate 100 concurrent farmers sending Malayalam queries. Target: P95 response \< 3s. If Gemini rate limit hit (15 RPM), implement request queue with APScheduler. Cache common answers in Redis (Railway Redis free tier).
4. 4

   #### HR Demo scenario scripts (ALL)

   Prepare 5 live demo scenarios: (1) Pest detection from leaf photo + advice, (2) "When should I sow rice?" → DSSAT answer in Malayalam, (3) Live market price check for coconut in Thrissur, (4) Weather-triggered irrigation alert, (5) Full voice query in Malayalam → voice answer.
5. 5

   #### Monitoring with Grafana Cloud free tier (M2)

   Ship FastAPI logs to Grafana Cloud (50GB free). Dashboard: API response times, agent activation frequency, error rate, queries per minute. Alert if P95 > 5s or error rate > 2%.

⌨️

Use These Now · Copy → Paste into Cline

## Production-Ready Cline Prompts

📋

**How to use these:** Open Cline in VS Code. Make sure your `brain/` folder is populated first (Prompt #1 builds it). Then use each prompt in order. Each prompt assumes the previous one completed successfully.

PROMPT #1 — brain/ folder setup (Run this FIRST in every new session)

CLINE

Read the following project rules before writing ANY code: # AGRI-SAGE PROJECT — MASTER RULES # brain/00_MASTER_RULES.md PROJECT: Agri-SAGE (Scalable Agricultural Guidance Engine) TARGET: Smallholder farmers in Kerala, India LANGUAGE: Malayalam-first, also English and Tamil PLATFORM: Android (Kotlin + Jetpack Compose) + FastAPI backend BUDGET: ZERO — only free APIs, free tiers, open-source LOCKED VERSIONS — DO NOT CHANGE: - FastAPI: 0.115.0 - LangGraph: 1.0.8 (use START/END constants from langgraph.graph) - pgvector: 0.4.0 (HNSW index only — not IVFFlat) - multilingual-e5-large: always prefix with query: or passage: - LLM: gemini-1.5-flash via langchain_google_genai - Android: targetSdk 35, minSdk 26, Compose BOM 2024.09.00 - Room: 2.7.0 with KSP (NOT kapt) - Navigation: 2.8.5 with kotlinx-serialization type safety ARCHITECTURE RULES: 1. All agent classes live in app/agents/ — one file per agent 2. All API service calls live in app/services/ — never inline in agents 3. Brain folder files are READ-ONLY for agents — never write to them 4. Every endpoint returns Pydantic v2 models — no raw dicts 5. Malayalam text: always handle as UTF-8, never assume ASCII 6. Secrets go in .env — never hardcode API keys 7. Every external API call has a try/except with specific error message FREE API KEYS LOCATION: - .env file at project root - GEMINI_API_KEY, DATA_GOV_IN_KEY, NASA_EARTHDATA_TOKEN - Open-Meteo needs NO key # Confirm you have read these rules before proceeding. Now create the complete brain/ folder with all 5 files: 00_MASTER_RULES.md (this content above) 01_PRD.md (product requirements for Agri-SAGE) 02_ARCHITECTURE.md (FastAPI + LangGraph + pgvector + Android architecture diagram in ASCII) 03_DATA_MODEL.md (all PostgreSQL tables with columns and types) 04_API_CONTRACT.md (all FastAPI endpoints with request/response schemas) Write each file with complete, real content. No placeholders.

PROMPT #2 — FastAPI backend skeleton with realtime data services

CLINE

\# Read brain/00_MASTER_RULES.md before starting. Build the complete FastAPI backend for Agri-SAGE with these exact files: FILE STRUCTURE TO CREATE: agrisage-backend/ ├── app/ │ ├── main.py ← FastAPI app with lifespan pattern │ ├── config.py ← Pydantic Settings, loads .env │ ├── database.py ← SQLAlchemy async engine + pgvector │ ├── models/ │ │ ├── farmer.py ← Farmer, Farm SQLAlchemy models │ │ ├── query.py ← Query, Advisory models │ │ └── market.py ← MarketPrice model │ ├── services/ │ │ ├── weather_service.py ← Open-Meteo API fetch │ │ ├── market_service.py ← data.gov.in APMC prices │ │ ├── pest_service.py ← NBAIR RSS feed parser │ │ └── soil_service.py ← NBSS district lookup │ ├── routers/ │ │ ├── chat.py ← POST /api/v1/chat │ │ ├── weather.py ← GET /api/v1/weather │ │ ├── market.py ← GET /api/v1/market │ │ └── alerts.py ← GET /api/v1/alerts │ └── schemas/ │ └── responses.py ← All Pydantic v2 response models ├── migrations/ ← Alembic migration files ├── .env.example ← Template with all required keys ├── requirements.txt ← Pinned to locked versions ├── Dockerfile ← For Railway deployment └── tests/ └── test_services.py ← Pytest tests for all services WEATHER SERVICE SPEC: URL: https://api.open-meteo.com/v1/forecast Params: latitude, longitude, hourly=\[temperature_2m,precipitation,relative_humidity_2m\] Cache response for 1 hour in PostgreSQL weather_cache table Return WeatherContext(temp_c, humidity_pct, rain_mm_24h, rain_chance_pct, advice_flag) MARKET SERVICE SPEC: URL: https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070 Params: api-key=DATA_GOV_IN_KEY, filters\[state\]=Kerala, format=json, limit=100 Run daily at 08:00 IST via APScheduler Store in market_prices(id, crop_name, district, min_price, max_modal_price, date) Write COMPLETE, WORKING Python code. No pseudocode. No TODO comments. Every function complete.

PROMPT #3 — LangGraph 14-agent orchestration system

AGENT ORCHESTRATION

\# Read brain/00_MASTER_RULES.md and brain/02_ARCHITECTURE.md first. Build the complete LangGraph agent system for Agri-SAGE. EXACT IMPORTS TO USE (LangGraph 1.0.8): from langgraph.graph import StateGraph, START, END from langgraph.checkpoint.memory import MemorySaver from langchain_google_genai import ChatGoogleGenerativeAI STATE DEFINITION (app/agents/state.py): class AgriSageState(TypedDict): farmer_id: str farmer_query: str # raw input (could be Malayalam) language: str # "ml", "en", or "ta" location: dict # {district: str, lat: float, lon: float} crop: str # primary crop mentioned query_intent: list\[str\] # \["WEATHER", "PEST", "MARKET", etc.\] weather_context: dict # from WeatherAgent soil_context: dict # from SoilAgent pest_alerts: list\[dict\] # from PestAgent market_data: dict # from MarketAgent kau_rag_results: list\[str\] # from CropAdvisorAgent dssat_output: dict # from SowingAgent agent_outputs: dict # all agent results combined final_answer_en: str # English answer final_answer_ml: str # Malayalam translated answer error: str # any error messages GRAPH TOPOLOGY: START → TranslatorAgent (detect language, translate to English if Malayalam) → RouterAgent (classify intent → set query_intent list) → \[PARALLEL FAN-OUT using Send() API\]: WeatherAgent | SoilAgent | PestAgent | MarketAgent | CropAdvisorAgent → \[JOIN — wait for all parallel agents\] → ConditionalEdge: if "SOWING" in query_intent → SowingAgent (DSSAT), else skip → SynthesizerAgent (combine all context → English answer) → TranslatorAgent (English → Malayalam final_answer_ml) → AlertAgent (check if proactive alert needed, trigger FCM if yes) END GEMINI FLASH SYSTEM PROMPT TEMPLATE FOR EACH AGENT: Each agent gets this system prompt pattern loaded from brain/05_AGENT_PROMPTS.md: "You are the {AGENT_NAME} for Agri-SAGE, an AI agricultural advisor for Kerala farmers. Your ONLY job is: {SPECIFIC_TASK}. Input you receive: {INPUT_FIELDS} Output you must return: {OUTPUT_FORMAT} — return ONLY valid JSON, no explanation. Always prioritize advice relevant to Kerala climate, Kerala crops (coconut, rice, banana, rubber, tapioca, pepper, cardamom), and Kerala soil conditions. If data is unavailable, return {field: null} — never hallucinate data." Build app/agents/graph.py (the compiled graph), app/agents/router_agent.py, app/agents/weather_agent.py, app/agents/pest_agent.py, app/agents/market_agent.py, app/agents/synthesizer_agent.py, app/agents/translator_agent.py. Write COMPLETE working code. Rate limit handler: if Gemini 429 error, wait 4 seconds and retry once.

PROMPT #4 — Android Kotlin + Jetpack Compose app

CLINE

\# Read brain/00_MASTER_RULES.md and brain/04_API_CONTRACT.md before writing any Kotlin. Build the complete Android app for Agri-SAGE. build.gradle.kts (app) — LOCKED VERSIONS: compileSdk = 35 minSdk = 26 compose_bom = "2024.09.00" navigation_compose = "2.8.5" room_version = "2.7.0" ksp_version = "2.0.21-1.0.27" (use KSP, NOT kapt) kotlinx_serialization_json = "1.7.3" SCREENS TO BUILD: 1. HomeScreen — Chat interface - LazyColumn with ChatMessage composables - Bottom bar: TextField + MicButton + SendButton - MicButton activates SpeechRecognizer(in-ML locale) - Loading: circular progress + "Agri-SAGE is thinking..." in Malayalam - Message bubble: green for user, white card for assistant 2. DashboardScreen — Live farm data - WeatherCard: temp, rain chance, humidity (refresh every 30min via WorkManager) - MarketPriceCard: today's top 3 Kerala crop prices from API - PestAlertBanner: red banner if active pest alert in farmer's district - All data from backend API, cached in Room for offline 3. AlertsScreen — Notification history - List of past push alerts with timestamp - Tap alert → opens HomeScreen with alert context pre-filled ROOM DATABASE SCHEMA: @Entity CachedMessage(id, role, content, timestamp) @Entity CachedWeather(id, district, data_json, cached_at) @Entity CachedMarketPrice(id, crop, district, price, date) @Entity FarmerProfile(id, name, language_pref, district, crops_json, lat, lon) NETWORK (Retrofit + OkHttp): Base URL from BuildConfig.API_BASE_URL (set in build.gradle from .env) AgriSageApiService interface: @POST("api/v1/chat") suspend fun chat(@Body req: ChatRequest): ChatResponse @GET("api/v1/weather") suspend fun weather(@Query district: String): WeatherResponse @GET("api/v1/market") suspend fun market(@Query crop: String, @Query district: String): MarketResponse VIEWMODEL PATTERN: ChatViewModel: StateFlow, handles send message, speech result DashboardViewModel: StateFlow, fetches weather + market Use Hilt for dependency injection (hiltViewModel() in composables) Write complete, working Kotlin. No TODOs. Every composable complete. Follow Material3 design.

PROMPT #5 — KAU document RAG pipeline (crop knowledge base)

RAG PIPELINE

\# This prompt builds the knowledge base that powers CropAdvisorAgent. Build the complete RAG pipeline for Agri-SAGE's crop knowledge base. STEP 1 — Document ingestion script (scripts/ingest_kau_docs.py): - Accept a directory of KAU PDF files as input - Extract text using pypdf (pure Python, no external deps) - Split into chunks: 512 tokens, 50-token overlap, using tiktoken cl100k_base - For each chunk, prepend: "passage: \[Kerala crop advisory\] " (required by multilingual-e5-large) - Embed using sentence_transformers SentenceTransformer("intfloat/multilingual-e5-large") - Store in PostgreSQL table: kau_documents(id UUID, source_file, chunk_index, content TEXT, embedding vector(1024)) - HNSW index: CREATE INDEX ON kau_documents USING hnsw (embedding vector_cosine_ops) - Log: "Ingested X chunks from Y files" when complete STEP 2 — RAG retrieval function (app/services/rag_service.py): async def retrieve_kau_advice(query: str, crop: str, top_k: int = 5) -> list\[str\]: # Embed query with "query: " prefix # pgvector cosine similarity search # Filter by crop name if mentioned # Return top_k chunk contents # Log query + retrieved doc IDs for quality monitoring STEP 3 — CropAdvisorAgent integration (app/agents/crop_advisor_agent.py): - Call rag_service.retrieve_kau_advice(query, crop) - Pass retrieved chunks as context to Gemini Flash - System prompt: "You are an expert KAU-trained crop advisor. Using ONLY the provided KAU Package of Practices excerpts below, answer the farmer's question about {crop}. If the answer is not in the excerpts, say 'Please consult your nearest KAU extension officer.' Do not guess." - Return structured CropAdvice(recommendation, source_doc, confidence) STEP 4 — Test the pipeline: Write pytest tests with a sample 2-page KAU PDF. Test query: "What is the fertilizer dose for coconut palms in sandy soil?" Expected: retrieves correct NPK recommendation from KAU doc, no hallucination. Write complete working Python code.

PROMPT #6 — Deploy to Railway + CI/CD GitHub Actions

DEVOPS

\# Final deployment prompt. Run after Prompts 1-5 are complete and tested. Set up complete deployment for Agri-SAGE backend. 1. Dockerfile (production-grade): FROM python:3.11-slim WORKDIR /app COPY requirements.txt . RUN pip install --no-cache-dir -r requirements.txt COPY . . # Install PostgreSQL client for health check RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/\* EXPOSE 8000 CMD \["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"\] 2. .github/workflows/deploy.yml: Trigger: push to main branch Jobs: test: - python 3.11 setup - pip install -r requirements.txt - pytest tests/ -v --tb=short - ruff check app/ deploy (runs only if test passes): - docker build -t ghcr.io/YOUR_GITHUB/agrisage-backend:latest . - docker push to GitHub Container Registry - Railway deploy via railway.toml 3. railway.toml: \[build\] builder = "dockerfile" dockerfilePath = "Dockerfile" \[deploy\] healthcheckPath = "/health" healthcheckTimeout = 30 restartPolicyType = "on_failure" 4. Environment variables to set in Railway dashboard: DATABASE_URL = postgresql+asyncpg://... (Railway provides this) GEMINI_API_KEY = your_key DATA_GOV_IN_KEY = your_key NASA_EARTHDATA_TOKEN = your_token ENVIRONMENT = production ALLOWED_ORIGINS = * (for demo, tighten later) 5. Android BuildConfig setup: In app/build.gradle.kts, add: buildConfigField("String", "API_BASE_URL", "\\"https://YOUR_RAILWAY_URL.railway.app/\\"") So the Railway URL is baked into the APK. Change for production. Create all files completely. Include the Android GitHub Actions workflow too: on push to main, build APK with Gradle, upload as artifact for download.

🚀

Post-MVP

## Future Goals — After the Demo

| Feature | Real Problem It Solves | Tech Needed | Impact |
| --- | --- | --- | --- |
| **📸 Leaf Disease Photo Detection** | Farmers can't name diseases — they can see them. Photo → instant diagnosis → treatment plan. | Gemini Vision API (free tier) or PlantNet API | HIGH |
| **🛰️ Field-level NDVI crop health map** | Early stress detection before visible symptoms. Save 30-40% of crop that would be lost. | Sentinel-2 (free via Copernicus) + EarthEngine | HIGH |
| **🤝 Farmer-to-Farmer Knowledge Network** | Local folk knowledge is priceless. Enable peer Q&A moderated by AI agents. | WebSocket chat + community agent | MID |
| **🏦 Government Scheme Advisor** | Most farmers don't know about PM-KISAN, PMFBY crop insurance, state subsidies. | RAG over GOI scheme PDFs + FinanceAgent | HIGH |
| **📦 Input Supply Chain Agent** | Where to buy seeds/fertilizer at best price nearby? Link to nearest certified dealer. | Maps API + local dealer DB | MID |
| **🌐 WhatsApp / SMS channel** | Many farmers don't install apps. WhatsApp Business API or Twilio SMS = zero install friction. | Meta Cloud API (free tier) | HIGH |
| **📊 Harvest yield prediction** | Plan harvest labor, storage, and sale before crop is ready. Reduce waste. | DSSAT + historical yield data ML model | MID |
| **🌍 Expand to Tamil Nadu, Karnataka** | Same model, new soil data + crops + language. 10x farmer reach. | Tamil + Kannada in multilingual-e5, new KVK docs | HIGH |

📅

Execution Timeline

## 8-Week Build Timeline

Week 1 (Oct 1-7)

Foundation Sprint

Brain/ folder ✦ FastAPI skeleton ✦ PostgreSQL+pgvector setup ✦ Register all 4 free API keys ✦ Open-Meteo weather service working

Week 2 (Oct 8-14)

Data Pipeline Sprint

Market prices cron job ✦ NBAIR pest RSS parser ✦ Soil zone lookup ✦ KAU PDF ingestion → pgvector ✦ All 4 services tested with real data

Week 3 (Oct 15-21)

Agent Architecture Sprint

LangGraph state + graph topology ✦ RouterAgent ✦ WeatherAgent + PestAgent ✦ Gemini Flash rate limit handler ✦ MemorySaver conversation memory

Week 4 (Oct 22-28)

Full Agent System

All 14 agents wired ✦ Malayalam TranslatorAgent ✦ DSSAT SowingAgent ✦ SynthesizerAgent ✦ Parallel fan-out with Send() API ✦ End-to-end test in Malayalam

Week 5 (Oct 29 - Nov 4)

Android App Sprint

Jetpack Compose screens ✦ Malayalam voice input ✦ Chat UI ✦ Room offline cache ✦ Retrofit API integration

Week 6 (Nov 5-11)

Integration Sprint

Android ↔ Backend connected ✦ FCM push notifications ✦ Farm dashboard live data ✦ Full flow test on real Android device

Week 7 (Nov 12-18)

Deploy + Test Sprint

Railway.app deployment ✦ GitHub Actions CI/CD ✦ Locust load test ✦ Grafana monitoring ✦ Bug fixes

Week 8 (Nov 19-25)

Demo Prep Sprint

5 live demo scenarios polished ✦ Presentation deck ✦ Video walkthrough ✦ User testing with 3 real farmers from Kerala

## 🌾 Start Right Now

Open Cline in VS Code. Paste **Prompt #1** to create your brain/ folder. Then register your free API keys. The entire system is buildable in 8 weeks with zero cost. Kerala farmers are waiting.

$ git clone agrisage-repo\
$ cd agrisage\
$ cp .env.example .env\
\# Fill in your 4 free API keys\
$ pip install -r requirements.txt\
$ uvicorn app.main:app --reload\
\# Agri-SAGE is live. 🌾

Agri-SAGE Production Build Plan · Built for Magnel's 5-member team · Zero Budget · Real Impact\
Kerala Smallholder Farmers · Oct 2026