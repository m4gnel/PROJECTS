# AGRI-SAGE — MICROTASKS (Copy-Paste Prompts for Cline)

## How to Use This File
1. Find your role section below
2. Pick the next uncompleted task (mark done with ✅)
3. Open Cline in VSCode
4. Type: `@brain/00_MASTER_RULES.md @brain/[relevant-brain-file].md`
5. Paste the prompt EXACTLY
6. Verify output works
7. Commit with `git commit -m "M[number]: [task name]"`

---

## MEMBER 1 — Backend Tasks

### Phase 0 (Week 1-2)
- [ ] **M1-T01: Project Structure**
```
Read @brain/00_MASTER_RULES.md and @brain/02_ARCHITECTURE.md.
Create the complete Agri-SAGE project directory structure:
backend/ mobile/android/ tests/ scripts/ alembic/ docs/ brain/ apps/web-expert/ .github/workflows/
Create .gitignore for Python + Android + Node + .env + __pycache__ + *.onnx + *.pt + .DS_Store
Create .env.example with ALL variables: DATABASE_URL SECRET_KEY ENVIRONMENT CORS_ORIGINS R2_BUCKET R2_ACCESS_KEY R2_SECRET_KEY R2_ACCOUNT_ID FCM_KEY BHASHINI_API_KEY OTP_PROVIDER_KEY WEATHER_PROVIDER GEMINI_API_KEY OLLAMA_URL MAX_IMAGE_SIZE_MB MODEL_VERSION KNOWLEDGE_VERSION LOG_LEVEL DSSAT_BIN_PATH
Create README.md: project name, one-paragraph description, team roles, link to docs/
Show directory tree when done.
```

- [ ] **M1-T02: Docker Environment**
```
Read @brain/00_MASTER_RULES.md.
Create docker-compose.yml: service 'db' using pgvector/pgvector:pg16 with POSTGRES_DB=agrisage_dev POSTGRES_USER=agrisage POSTGRES_PASSWORD=${DB_PASSWORD} port 5432 healthcheck pg_isready named volume postgres_data. Service 'backend' built from Dockerfile port 8000 env_file .env depends_on db condition service_healthy.
Create Dockerfile: FROM python:3.11-slim, RUN apt-get install -y build-essential libpq-dev libmagic1, COPY requirements.txt, RUN pip install --no-cache-dir -r requirements.txt, COPY . /app, WORKDIR /app, CMD uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
Create backend/requirements.txt with EXACT versions from brain/00_MASTER_RULES.md Tech Stack section.
Show docker-compose.yml in full.
```

- [ ] **M1-T03: FastAPI App + Config**
```
Read @brain/00_MASTER_RULES.md @brain/08_SECURITY.md.
Create backend/config.py using pydantic-settings 2.7.0 BaseSettings with SettingsConfigDict(env_file='.env'). All fields from .env.example. Export settings = Settings().
Create backend/database.py: async SQLAlchemy engine, AsyncSessionLocal, Base=declarative_base(), async get_db() dependency, async check_db_connection() returns bool.
Create backend/main.py: FastAPI with @asynccontextmanager lifespan (load models on startup, dispose engine on shutdown). CORSMiddleware with settings.CORS_ORIGINS. Structlog middleware logging method+path+status+ms — NEVER log Authorization headers. All routers with prefix /api/v1. GET /health returns {status,version,environment,db_connected}. Global 500 handler returns only {"detail":"Internal server error"}.
Show backend/main.py in full.
```

- [ ] **M1-T04: All 17 Alembic Migrations**
```
Read @brain/03_DATA_MODEL.md carefully — every column and constraint.
Run: alembic init alembic
Configure alembic/env.py for async engine.
Create migrations 001 through 017 in separate files using EXACT SQL from brain/03_DATA_MODEL.md.
Migration order: 001_extensions → 002_users → 003_farms → 004_crop_cycles → 005_observations → 006_weather → 007_diagnoses → 008_advisories → 009_interventions → 010_simulation → 011_knowledge (use HNSW index NOT IVFFlat) → 012_schemes → 013_market → 014_notifications → 015_expert → 016_audit → 017_rls (LAST — all tables must exist first).
List all migration files when done.
```

- [ ] **M1-T05: Auth Endpoints**
```
Read @brain/08_SECURITY.md JWT and OTP sections.
Create backend/services/jwt_service.py: create_access_token (HS256, 15min), create_refresh_token (SHA256 hash stored, 7day), verify_access_token.
Create backend/dependencies.py: require_auth dependency — decode JWT, validate, SET LOCAL app.current_user_id in PostgreSQL session for RLS, return payload. Raise HTTPException(401) on any failure.
Create backend/api/v1/auth.py: POST /send-otp (6-digit secrets.randbelow, bcrypt hash rounds=10, store in otp_sessions, rate limit 5/phone/10min, print OTP to console in dev mode), POST /verify-otp (check hash+expiry+attempts<5, mark used, create/get user, return JWT pair), POST /refresh (rotate token), POST /logout (revoke).
Show auth.py in full.
```

- [ ] **M1-T06: Farm CRUD + Image Upload**
```
Read @brain/03_DATA_MODEL.md @brain/08_SECURITY.md @brain/04_API_CONTRACT.md.
Create SQLAlchemy ORM models for farms, fields, soil_profiles, crop_cycles matching brain/03_DATA_MODEL.md exactly.
Create Pydantic v2 schemas with @field_validator sanitizing name fields (strip HTML tags, control chars).
Create backend/api/v1/farms.py: full CRUD for /farms /fields /crop-cycles. All require require_auth. SET LOCAL before every query. Return 404 for not-found OR not-owned (RLS returns empty = treat same as not found).
Create backend/services/image_security.py: process_uploaded_image function from brain/08_SECURITY.md exactly.
Create backend/services/storage.py: R2StorageService using boto3 endpoint_url=https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com. Methods: upload_image, delete_image, generate_signed_url (1 hour expiry).
Create backend/api/v1/observations.py: POST /observations multipart — validate image via image_security, upload to R2, store records, return {observation_id, image_ids}.
Show backend/api/v1/observations.py in full.
```

- [ ] **M1-T07: Diagnose Endpoint + Weather**
```
Read @brain/04_API_CONTRACT.md @brain/02_ARCHITECTURE.md.
Create backend/api/v1/diagnose.py: POST /diagnose {observation_id} — load observation+images, verify ownership, start timer, run advisory_graph (import from agents/orchestrator.py), record generation_ms, save advisory to DB, return full AdvisoryResponse from brain/04_API_CONTRACT.md.
Create backend/services/weather_provider.py: abstract WeatherProvider + OpenMeteoProvider calling https://api.open-meteo.com/v1/forecast. Cache in-memory dict 30 minutes by (round(lat,2),round(lon,2)).
Create backend/api/v1/weather.py: GET /weather/{lat}/{lon} returns WeatherResult with all indicators.
Show diagnose.py in full.
```

---

## MEMBER 2 — AI Agent Tasks

### Phase 1 (Weeks 3-8)
- [ ] **M2-T01: LangGraph Skeleton**
```
Read @brain/00_MASTER_RULES.md @brain/05_AGENTS.md.
Create backend/agents/orchestrator.py using LangGraph 1.0.8:
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
Define AgriSAGEState TypedDict with all fields from brain/05_AGENTS.md.
Build graph: START→intake→parallel[vision,weather,crop_stage,knowledge]→critic→[scheme,conditional simulation]→decision→explanation→END.
compile with MemorySaver checkpointer.
Create stub files for all 14 agents in backend/agents/ — each with class + run(state) returning state unchanged.
Show orchestrator.py in full.
```

- [ ] **M2-T02: Intake + Vision + Critic Agents**
```
Read @brain/05_AGENTS.md @brain/10_DATA_FILES.md.
Implement intake.py: merge observation data with farm profile, compute days_after_sowing, normalize crop name, flag null fields.
Implement vision.py: singleton ONNX session. Load class names from backend/data/disease_classes.json. Quality check (blur Laplacian<100, brightness<40or>220, crop<30% frame → INSUFFICIENT_DATA). Run inference, softmax, top-5. Return VisionResult.
Implement critic.py: ALL rules from brain/05_AGENTS.md Critic section. Conflict detection (fungal+dry weather, stage mismatch, high confidence+poor image). Safety blocks (unknown product, wrong crop registration, exceeded dosage, expired scheme, invented product). Assign confidence_state. Set run_simulation. NO LLM.
Show critic.py in full.
```

- [ ] **M2-T03: Weather + CropStage + Knowledge Agents**
```
Read @brain/05_AGENTS.md @brain/10_DATA_FILES.md.
Implement weather.py: call OpenMeteoProvider, compute DFI formula from brain/05_AGENTS.md, spray window (rain<20% AND wind<15 for 4hr block), heat stress risk. Cache 30min.
Implement crop_stage.py: load backend/data/gdd_thresholds.json. Compute cumulative GDD: max(0,((tmax+tmin)/2)-base_temp[crop]) for each day. Match to stage threshold. Return CropStageResult with vulnerability and upcoming windows.
Implement knowledge.py: HybridRetriever — dense pgvector search (ALWAYS prefix 'query: ', normalize_embeddings=True) + PostgreSQL FTS. RRF merge k=60. Cross-encoder rerank (cross-encoder/ms-marco-MiniLM-L-6-v2). Tier 1 authority boost ×1.3. Filter valid_until>today AND status=PUBLISHED.
Show crop_stage.py in full.
```

- [ ] **M2-T04: LLM Service + Decision + Explanation**
```
Read @brain/06_LLM_PROMPTS.md @brain/00_MASTER_RULES.md.
Create backend/services/llm_service.py: LLMService with Gemini primary (if GEMINI_API_KEY set) and Ollama fallback. Retry logic: on invalid JSON append 'Output ONLY valid JSON.' and retry once. Return None after 2 failures.
Implement decision.py: score each scenario — yield_score + profit_score - risk_penalty(critical=-3,high=-2,medium=-1,low=0) - uncertainty_penalty((1-confidence)*2). Flag BUDGET_EXCEEDED if over farmer_budget_inr.
Implement explanation.py: use system prompt from brain/06_LLM_PROMPTS.md Prompt 1 VERBATIM. temperature=0.2 max_tokens=1500. If confidence_state in [UNCERTAIN,INSUFFICIENT_DATA,CONFLICTING_EVIDENCE] → no treatment, request more info. Check for invented product names. Use SAFE_FALLBACK from brain/06_LLM_PROMPTS.md if LLM returns None.
Show explanation.py in full — confirm system prompt is copied verbatim.
```

- [ ] **M2-T05: Scheme + Monitoring Agents**
```
Read @brain/06_LLM_PROMPTS.md Prompts 2 and 4.
Implement scheme.py: query schemes table (valid_until>NOW, status=active, crop matches). Score eligibility from eligibility_rules JSON. Use LLM system prompt from brain/06_LLM_PROMPTS.md Prompt 2 VERBATIM for complex cases. ALWAYS append mandatory caveat. temperature=0.1.
Create backend/services/morning_briefing.py: MorningBriefingGenerator. For each active farmer: load farm+crop+weather+risk. Build briefing using Prompt 4 from brain/06_LLM_PROMPTS.md VERBATIM. temperature=0.3. Store in notifications table type=morning_briefing. Send FCM.
Create APScheduler job at 05:30 UTC daily calling generate_for_all_active_users().
Create backend/services/notifications.py: FCMNotificationService using firebase-admin. send(user_id, title, body, data) method.
Show scheme.py in full.
```

---

## MEMBER 3 — Android Tasks

### Phase 0-1 (Weeks 1-6)
- [ ] **M3-T01: Android Project + Design System**
```
Read @brain/07_ANDROID_SPEC.md.
Create Android project in mobile/android/ — package com.agrisage.app minSdk 26 targetSdk 35 Kotlin 2.0.21.
Create build.gradle.kts with ALL dependencies from brain/07_ANDROID_SPEC.md Stack section. Use KSP not kapt for Room.
Create ui/theme/Color.kt: ALL 30 color tokens from brain/07_ANDROID_SPEC.md with EXACT hex values.
Create ui/theme/Type.kt: ALL text styles with Noto Sans font — all sp values exact.
Create ui/theme/Shape.kt: cornerSm=8dp cornerMd=12dp cornerLg=16dp cornerXl=24dp.
Create ui/theme/Theme.kt: AgriSAGETheme composable.
Show Color.kt in full.
```

- [ ] **M3-T02: Room Database + Navigation**
```
Read @brain/07_ANDROID_SPEC.md @brain/03_DATA_MODEL.md.
Create all Room entities from brain/07_ANDROID_SPEC.md: FarmEntity, FarmerEntity, FieldEntity, CropCycleEntity, ObservationEntity, ImageEntity, CachedAdvisoryEntity, WeatherCacheEntity, SyncQueueEntity.
Create DAO for each. Create AgriSAGEDatabase @Database class.
Create Hilt DatabaseModule providing database and all DAOs.
Create NavGraph.kt with type-safe routes from brain/07_ANDROID_SPEC.md Navigation Routes section using @Serializable objects.
Create network_security_config.xml: cleartextTrafficPermitted=false.
Show AgriSAGEDatabase.kt in full.
```

- [ ] **M3-T03: Camera Screen**
```
Read @brain/07_ANDROID_SPEC.md Camera Screen section.
Create CameraScreen.kt:
- Full-screen CameraX preview via PreviewView in AndroidView
- ImageAnalysis every 500ms: Laplacian variance for blur, mean brightness, crop region coverage → QualityLevel enum (GOOD/OKAY/POOR)
- QualityIndicatorBar: 8dp height, animateColorAsState 200ms — Color(0xFF4CAF50)/Color(0xFFFF9800)/Color(0xFFF44336)
- Quality message text changes: 'Good — tap to capture' / 'Hold steady' / 'Too dark — move to shade'
- Capture button: 80dp circular white 4dp border, centered bottom 48dp, haptic feedback
- On POOR: AlertDialog with specific message + Retry
- On GOOD/OKAY: save to local file, navigate to ContextFormScreen
- CropChip top-right: tappable, opens crop picker BottomSheet
Create CameraViewModel.kt.
Show CameraScreen.kt in full.
```

- [ ] **M3-T04: Advisory Result Screen**
```
Read @brain/07_ANDROID_SPEC.md Advisory Result Screen section.
Create these composables in ui/components/:
ConfidenceBadge(state: String): pill 32dp, corner 16dp, colors from brain/07_ANDROID_SPEC.md. Text white on all.
RiskLevelBadge(level: String): pill 28dp, CRITICAL=Color(0xFFC62828) HIGH=Color(0xFFE65100) MEDIUM=Color(0xFFF57F17) LOW=Color(0xFF2E7D32).
EvidenceCard(items: List): bg Color(0xFFE3F2FD), corner 12dp, left border 2dp ColorPrimary, expandable expanded by default.
ActionCard(action): bg ColorPrimaryLight, corner 16dp, 2dp border ColorPrimary. All fields with icons.
ModelledEstimateLabel(): italic bodySmall Color(0xFF9E9E9E) text "* Modelled estimate — actual results vary by field conditions". MANDATORY under every yield/return figure.
FeedbackRow(onUp, onDown): thumbs up/down 48dp.
AdvisoryResultScreen: LazyColumn with all composables in correct order.
Show AdvisoryResultScreen.kt in full.
```

- [ ] **M3-T05: Home Screen + Offline**
```
Read @brain/07_ANDROID_SPEC.md Home Screen section.
Create HomeScreen.kt:
- TopAppBar: bg ColorPrimaryDark, farm name headlineSmall white left, sync icon animates when syncing
- AlertBanner: shown when OFFLINE/LIMITED. OFFLINE=orange bg+text. LIMITED=amber.
- MorningBriefingCard: bg ColorPrimaryLight corner 16dp padding 16dp. 4 rows: crop+stage, risk, weather, action. Speaker IconButton top-right.
- 2x2 ActionTile grid: corner 12dp bg white elevation 2dp 100dp min height. 4 tiles as spec.
- BottomNavBar: 5 items Home|Farm|Diagnose|Alerts|Profile. Diagnose center elevated circular ColorPrimary.
Create HomeViewModel.kt: loads farm from Room, observes ConnectivityManager, loads cached morning briefing, refreshes if >12hrs old AND connected.
Create SyncWorker.kt CoroutineWorker: upload sync_queue ordered by priority ASC, download delta, check knowledge version. Schedule with WorkManager exponential backoff.
Create OfflineAdvisoryEngine.kt: ONNX inference + load templates from assets/offline_templates_ml.json + fill slots → advisory marked isOffline=true.
Show HomeScreen.kt in full.
```

---

## MEMBER 4 — Data Tasks

### Phase 0 (Days 1-3 — URGENT — unblocks everyone)
- [ ] **M4-T01: All JSON Data Files** ⚡ DO THIS FIRST — BLOCKS MEMBER 2
```
Read @brain/10_DATA_FILES.md carefully.
Create ALL 5 JSON files in backend/data/ using EXACT content from brain/10_DATA_FILES.md:
1. disease_classes.json — all 22 classes with index, class_name, common_name, ml_name, crop
2. gdd_thresholds.json — base_temperatures + thresholds for all 5 crops
3. offline_templates_ml.json — all 7 Malayalam templates with slots
4. intent_keywords_ml.json — all Malayalam keyword mappings
5. stage_disease_map.json — for each stage: expected diseases and unlikely diseases
Also create assets/offline_templates_ml.json (copy of #3 for Android assets folder).
Show gdd_thresholds.json in full.
```

- [ ] **M4-T02: Vision Model Training**
```
Read @brain/00_MASTER_RULES.md ML section.
Create backend/ml/vision/train.py:
Model: torchvision.models.efficientnet_b3(weights=EfficientNet_B3_Weights.IMAGENET1K_V1). Replace classifier[-1] with nn.Linear(1536, 22). 22 classes from backend/data/disease_classes.json.
FARMER-LEVEL split — group images by farmer folder, 70/15/15.
Adam lr=1e-4, CosineAnnealingLR T_max=50, CrossEntropyLoss with class weights, early stopping patience=7.
Augmentation: RandomResizedCrop(300), RandomHorizontalFlip, ColorJitter(0.3,0.3), GaussianBlur(p=0.2), Normalize(ImageNet stats).
After training: temperature scaling calibration targeting ECE<0.12.
ASSERT macro_f1>=0.82 AND ece<=0.12 before saving. Print PASS or FAIL.
Create backend/ml/vision/export.py: export_to_onnx (opset 17), quantize_int8 (QInt8), verify accuracy loss <0.02.
Show train.py in full.
```

- [ ] **M4-T03: Knowledge Ingestion Pipeline**
```
Read @brain/00_MASTER_RULES.md @brain/05_AGENTS.md Knowledge Agent section.
Create backend/knowledge/ingestion.py: DocumentIngestionPipeline with fetch_document(url), parse_pdf(PyMuPDF), parse_html(BeautifulSoup), extract_metadata, extract_chunks (split at headings then paragraphs, max 512 tokens min 100 chars preserve table rows), embed_chunks (multilingual-e5-large 'passage: ' prefix, normalize_embeddings=True), store_chunks (bulk INSERT).
Create backend/knowledge/retrieval.py: HybridRetriever with dense_search (pgvector 'query: ' prefix), sparse_search (PostgreSQL FTS), RRF merge k=60, cross-encoder rerank, Tier 1 boost ×1.3. Filter valid_until>today AND status=PUBLISHED.
Create scripts/seed_knowledge.py and scripts/seed_urls.json with 10 real ICAR/KAU document URLs.
Show retrieval.py in full.
```

- [ ] **M4-T04: Scheme + Market Data Seeding**
```
Read @brain/03_DATA_MODEL.md schemes table.
Create scripts/seed_schemes.py seeding:
1. PMFBY: crops=[rice,maize,tomato,banana], eligibility_rules={land_ownership:[owner,tenant],aadhaar_required:true}, benefits={premium_kharif_pct:2.0,premium_rabi_pct:1.5}, valid_until=2027-03-31, enrollment_url=https://pmfby.gov.in
2. PM-KISAN: eligibility_rules={land_ha_max:2,not_income_taxpayer:true,not_govt_employee:true}, benefits={annual_inr:6000,installments:3}, valid_until=2028-03-31
3. At least 3 Kerala state schemes from keralaagriculturedept.gov.in
Create backend/agents/market.py: fetch e-NAM data from data.gov.in resource 9ef84268-d588-465a-a308-a864a43d0070. Filter by state+district. Haversine for nearest markets. Cache 30min.
Show seed_schemes.py in full.
```

---

## MEMBER 5 — QA/DevOps Tasks

### Phase 0 (Days 1-3)
- [ ] **M5-T01: Test Infrastructure + CI/CD**
```
Read @brain/09_TESTING.md @brain/08_SECURITY.md.
Create tests/conftest.py: async_client fixture (httpx AsyncClient), test_db fixture (create test DB, run all migrations, yield, drop), test_user_token fixture, test_farm fixture.
Create pytest.ini from brain/09_TESTING.md.
Create tests/unit/test_crop_stage.py: ALL 3 test cases from brain/09_TESTING.md GDD section exactly.
Create tests/unit/test_weather_agent.py: ALL 3 DFI test cases from brain/09_TESTING.md exactly.
Create tests/safety/test_critic_safety.py: ALL 5 safety test cases from brain/09_TESTING.md exactly — do not modify.
Create tests/integration/test_auth_api.py: auth endpoint tests.
Create tests/security/test_rls.py: cross-user access test — assert status_code == 404 NOT 403 NOT 200.
Create .github/workflows/ci.yml: test job (PostgreSQL 16 service, pip install, alembic upgrade head, pytest -v), lint job (black + ruff), security job (pip-audit --fail-on CRITICAL, bandit -lll).
Show tests/safety/test_critic_safety.py in full.
```

- [ ] **M5-T02: Deployment Scripts**
```
Read @brain/13_GITHUB_ACTIONS.md (or brain/00_MASTER_RULES.md infrastructure section).
Create scripts/smoke_tests.py: 3 checks — GET /health returns 200 db_connected=true, GET /api/v1/weather/10.12/76.34 returns 200, POST /api/v1/auth/send-otp returns 200. Print PASS/FAIL per check. Exit 1 if any fail.
Create scripts/deploy.sh: git pull, docker compose pull, docker compose up -d --no-deps backend, sleep 5, alembic upgrade head, python scripts/smoke_tests.py. Exit 1 if smoke tests fail.
Create scripts/security_audit.py: 6 checks — pip-audit, bandit, grep for hardcoded secrets, verify RLS on all user tables, test rate limiting (6 OTPs → 429), test SQL injection strings (all return 400 not 500).
Create nginx/nginx.conf: reverse proxy to port 8000, SSL redirect, rate limits from brain/08_SECURITY.md, gzip compression.
Show nginx.conf in full.
```
