# 🏗️ PHASE 1 — Foundation + Realtime Data Pipeline
## Branch: `dev/m1-backend` · Owner: M1 · GitHub Issue: #1

---

## Paste This Into Gemini 2.5 Pro

```
=== AGRI-SAGE PHASE 1 — FOUNDATION + DATA PIPELINE ===

Run AUDIT-FIRST PROTOCOL on every existing file before writing anything.
Print the audit table. Then build only MISSING and NEEDS_WORK files.

TARGET FILE STRUCTURE:
agrisage-backend/
├── brain/
│   ├── 00_MASTER_RULES.md
│   ├── 01_PRD.md
│   ├── 02_ARCHITECTURE.md
│   ├── 03_DATA_MODEL.md
│   ├── 04_API_CONTRACT.md
│   └── kerala_soil_data.json
├── app/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   ├── models/
│   │   ├── farmer.py
│   │   ├── query_log.py
│   │   └── market.py
│   ├── routers/
│   │   ├── chat.py
│   │   ├── weather.py
│   │   ├── market.py
│   │   └── alerts.py
│   └── services/
│       ├── weather_service.py
│       ├── market_service.py
│       ├── pest_service.py
│       └── soil_service.py
├── migrations/
│   └── (3 Alembic files: init, pgvector ext, HNSW indexes)
├── requirements.txt
├── .env.example
├── Dockerfile
└── tests/
    └── test_services.py

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BRAIN/ FOLDER CONTENT SPEC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

brain/00_MASTER_RULES.md must contain:
  - All locked versions (FastAPI 0.115.0, LangGraph 1.0.8, pgvector 0.4.0,
    multilingual-e5-large dim=1024, Gemini 1.5 Flash, Room 2.7.0 KSP,
    Nav Compose 2.8.5, Compose BOM 2024.09.00)
  - Architecture rules: agents in app/agents/, services in app/services/,
    secrets in .env, Pydantic v2 models only, UTF-8 for Malayalam
  - Free API endpoints: Open-Meteo (no key), data.gov.in, NBAIR RSS, NASA EarthData

brain/01_PRD.md must contain:
  - Problem: 2.3M Kerala farming families, <12% digital advisory access
  - Solution: Malayalam-first AI advisor, <3s response, works on ₹5,000 phones
  - KPIs: 100K active farmers Year 1, 90% of everyday decisions answered
  - User personas: 3 Kerala farmer archetypes (coconut, rice, mixed crops)

brain/02_ARCHITECTURE.md must contain:
  ASCII diagram of: Android App → FastAPI → LangGraph → [14 Agents] →
  [pgvector RAG + Open-Meteo + data.gov.in + NBAIR RSS + NBSS Soil + DSSAT]

brain/03_DATA_MODEL.md must contain ALL table definitions:
  farmers(id UUID PK, name, phone, district, lat FLOAT, lon FLOAT,
          language_pref VARCHAR(2), primary_crop, created_at)
  farms(id UUID PK, farmer_id FK, name, area_acres, soil_district, crop_variety)
  query_logs(id UUID PK, farmer_id FK, query_text, language,
             intent_tags JSON, response_ml TEXT, response_time_ms INT, created_at)
  market_prices(id UUID PK, crop_name, variety, district, min_price FLOAT,
                max_price FLOAT, modal_price FLOAT, date DATE,
                UNIQUE(crop_name, district, date))
  pest_alerts(id UUID PK, title, description, affected_crops JSON,
              severity VARCHAR(6), pub_date, fetched_at)
  weather_cache(id UUID PK, district, data_json JSONB, fetched_at,
                expires_at)
  kau_documents(id UUID PK, source_file, crop_name, chunk_index INT,
                content TEXT, embedding vector(1024), created_at)
  farm_analytics(id UUID PK, farmer_id FK, season, crop, yield_kg_ha FLOAT,
                 query_count INT, advisory_count INT, created_at)

brain/04_API_CONTRACT.md must contain:
  POST /api/v1/chat
    Request:  {farmer_id, query, language, location:{district,lat,lon}, crop}
    Response: {answer_ml, answer_en, intent, agents_used, response_time_ms}

  GET /api/v1/weather?district=Ernakulam
    Response: {temp_c, humidity_pct, rain_mm_24h, rain_chance_pct,
               wind_kmh, advice_flag, cached}

  GET /api/v1/market?crop=coconut&district=Thrissur
    Response: {crop, district, min_price, max_price, modal_price,
               date, trend, sell_recommendation}

  GET /api/v1/alerts?district=Ernakulam&crop=coconut
    Response: {alerts:[{title, severity, description, pub_date}]}

  GET /health
    Response: {status:"healthy", service:"agrisage-backend", version:"1.0.0"}

brain/kerala_soil_data.json must contain all 14 districts:
  {
    "Ernakulam": {
      "ph_min": 5.5, "ph_max": 6.5, "texture": "laterite",
      "organic_carbon": "medium", "n_status": "low",
      "p_status": "medium", "k_status": "high",
      "suitable_crops": ["coconut","tapioca","banana","yam"]
    },
    ... (all 14: Thiruvananthapuram, Kollam, Pathanamthitta, Alappuzha,
         Kottayam, Idukki, Ernakulam, Thrissur, Palakkad, Malappuram,
         Kozhikode, Wayanad, Kannur, Kasaragod)
  }

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SERVICES EXACT SPEC
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

app/services/weather_service.py:
  URL: https://api.open-meteo.com/v1/forecast
  Params: latitude={lat}&longitude={lon}
          &hourly=temperature_2m,precipitation,relative_humidity_2m,windspeed_10m
          &forecast_days=7&timezone=Asia/Kolkata
  Cache TTL: 1 hour in weather_cache table (check expires_at before fetching)
  Return: WeatherContext dataclass:
    temp_c: float          # current hour temperature
    humidity_pct: int      # current hour humidity
    rain_mm_24h: float     # sum of next 24h precipitation
    rain_chance_pct: int   # max precipitation_probability next 12h
    wind_kmh: float        # current hour wind speed
    advice_flag: str       # one of: SPRAY_RISK | IRRIGATION_NEEDED | FLOOD_RISK | NORMAL
  advice_flag logic:
    SPRAY_RISK       if humidity_pct > 85 and rain_mm_24h < 2
    IRRIGATION_NEEDED if rain_mm_24h < 1 and temp_c > 32
    FLOOD_RISK        if rain_mm_24h > 50
    else NORMAL
  Error handling: httpx.TimeoutException → return cached data with stale=True flag

app/services/market_service.py:
  URL: https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070
  Headers: {"api-key": settings.DATA_GOV_IN_KEY}
  Params: filters[state]=Kerala&format=json&limit=100&offset=0
  Schedule: APScheduler CronTrigger(hour=8, minute=0, timezone="Asia/Kolkata")
  On fetch: for each record upsert into market_prices
            ON CONFLICT(crop_name, district, date) DO UPDATE SET modal_price=EXCLUDED.modal_price
  Trend calculation: compare today's modal_price vs 7-day average
                     trend = "UP" if today > avg*1.05, "DOWN" if today < avg*0.95, else "STABLE"
  Error handling: if API key missing or 401 → log warning, skip run, retry next day

app/services/pest_service.py:
  URL: https://nbair.res.in/PestAlerts/rassFeed.php
  Parse with: feedparser library (feedparser==6.0.11)
  Schedule: every 6 hours via APScheduler IntervalTrigger(hours=6)
  KERALA_CROPS = ["coconut","rice","banana","rubber","tapioca",
                  "pepper","cardamom","ginger","turmeric","arecanut"]
  For each RSS entry:
    severity: "HIGH"   if any(w in title.lower() for w in ["outbreak","severe","emergency"])
    severity: "MEDIUM" if any(w in title.lower() for w in ["alert","warning","caution"])
    severity: "LOW"    otherwise
    affected_crops: [c for c in KERALA_CROPS if c in (title+description).lower()]
  Upsert into pest_alerts ON CONFLICT(title, pub_date) DO NOTHING
  Error handling: feedparser can return empty feed → log warning, do not crash

app/services/soil_service.py:
  Load kerala_soil_data.json once at startup into memory dict
  Method: get_soil_by_district(district: str) -> SoilContext | None
  SoilContext dataclass:
    district: str
    ph_min: float
    ph_max: float
    texture: str           # laterite | alluvial | forest | sandy
    organic_carbon: str    # low | medium | high
    n_status: str          # low | medium | high
    p_status: str
    k_status: str
    suitable_crops: list[str]
  If district not found: log warning, return None (agents handle None gracefully)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
REQUIREMENTS.TXT — EXACT PINNED VERSIONS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

fastapi==0.115.0
uvicorn[standard]==0.30.6
sqlalchemy==2.0.36
asyncpg==0.30.0
pgvector==0.4.0
alembic==1.13.3
pydantic==2.9.2
pydantic-settings==2.6.1
langchain-google-genai==2.0.4
langgraph==1.0.8
sentence-transformers==3.3.1
feedparser==6.0.11
apscheduler==3.10.4
httpx==0.28.0
python-dotenv==1.0.1
pypdf==5.1.0
tiktoken==0.8.0
prometheus-fastapi-instrumentator==7.0.0
pytest==8.3.4
pytest-asyncio==0.24.0
pytest-mock==3.14.0
ruff==0.7.1

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TEST SPEC (tests/test_services.py)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Write pytest tests that mock all 4 external APIs:
  test_weather_service_returns_context()
    mock httpx GET to open-meteo → assert WeatherContext returned
    assert advice_flag == "FLOOD_RISK" when rain_mm_24h > 50
  test_weather_service_uses_cache()
    insert a non-expired cache entry → assert no HTTP call made
  test_market_service_upserts_prices()
    mock data.gov.in response with 3 Kerala items → assert 3 rows in market_prices
  test_pest_service_parses_rss()
    mock feedparser with 2 entries including "coconut outbreak" →
    assert severity == "HIGH" and "coconut" in affected_crops
  test_soil_service_ernakulam()
    assert get_soil_by_district("Ernakulam").texture == "laterite"
  test_soil_service_unknown_district()
    assert get_soil_by_district("InvalidDistrict") is None

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GITHUB ISSUE PROTOCOL — PHASE 1
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

After all files are built and tests pass (pytest tests/test_services.py -v → 0 failures):

  git checkout dev/m1-backend
  git add -A
  git commit -m "feat(phase-1): foundation data pipeline — brain/, FastAPI skeleton, 4 realtime services"
  git tag v0.1.0

Then create a GitHub Issue with:
  Title: [Phase 1] Foundation + Realtime Data Pipeline
  Labels: phase-1, backend
  Assign: @M1
  Body: (list every file created, every PROTECTED file skipped, paste test output)

Print: "✅ Phase 1 committed to dev/m1-backend. Issue created. Waiting for team review."
STOP — do not proceed to Phase 2 until confirmation received.
```

---

## What This Phase Builds

| File | Status It Handles |
|---|---|
| `brain/00_MASTER_RULES.md` | Creates if missing; patches version numbers if wrong |
| `brain/kerala_soil_data.json` | Creates if missing — all 14 Kerala districts |
| `app/services/weather_service.py` | Creates or fixes if incomplete |
| `app/services/market_service.py` | Creates or fixes — data.gov.in APMC |
| `app/services/pest_service.py` | Creates or fixes — NBAIR RSS |
| `app/services/soil_service.py` | Creates or fixes — district JSON lookup |
| `requirements.txt` | Creates or updates to pinned versions |
| `tests/test_services.py` | Creates all 6 tests with mocks |

## GitHub Issue Created After This Phase

```
Title: [Phase 1] Foundation + Realtime Data Pipeline
Branch: dev/m1-backend
Labels: phase-1, backend
Assign to: M1
```

---

> **Next:** Paste `03-phase2-agents.md` after Issue #1 is reviewed and merged
