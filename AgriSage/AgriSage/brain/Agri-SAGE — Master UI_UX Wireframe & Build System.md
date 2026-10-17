[🌿 Agri-SAGE](#)

# Agri-SAGE Design System

Mobile-first UI/UX for Kerala smallholder farmers — multilingual, zero-budget, zero-complexity. Every pixel earns its place.

Jetpack Compose Material You 3 Kotlin Multilingual Offline-First WCAG AA

Color Palette

Built from Kerala's agricultural landscape — rice paddy greens, laterite soil, monsoon sky, harvest gold.

#### Primary — Sage

Deep #1B4332 · Mid #2D6A4F · Light #40916C · Leaf #52B788

#### Alert System

Critical · Warning · Info · Success

#### Surfaces

White #FAFDF8 · Surface1 · Surface2 · Pale

#### Soil Accent

Laterite #7C4D26 — Used sparingly for CTAs needing contrast against green

#### Typography

Nunito 900

Display headings — Expressive, farmer-friendly

Inter 400/500/600

Body — Clean, readable at small sizes

#### Spacing Scale

4px — xs

8px — sm

16px — md

24px — lg

32px — xl

#### Border Radius

8

12

16

24

#### Icon Set

🌾🌧️🌡️🐛⚠️📍🗓️💬🔔👨‍🌾🌱🏞️📊🔍🌤️💧🧪🤖

Material Symbols + Emoji fallback for rural accessibility

Type Scale

6-level scale. All sizes in sp (scale-independent pixels) for Android.

| Role | Font | Size (sp) | Weight | Use |
| --- | --- | --- | --- | --- |
| Display | Nunito | 32 | 900 | Splash, hero titles |
| H1 | Nunito | 24 | 800 | Screen titles |
| H2 | Nunito | 18 | 700 | Section headers |
| Body Large | Inter | 15 | 500 | Primary content |
| Body | Inter | 13 | 400 | Secondary content |
| Caption | Inter | 11 | 600 | Labels, metadata |

Elevation & Shadows

#### Level 0

No shadow — flat surfaces, lists

#### Level 1

Cards, inputs — subtle

#### Level 2

Floating buttons, tooltips

#### Level 3

Modals, bottom sheets

Screen Wireframes

All 8 core screens — pixel-accurate proportions, 360×800dp reference device.

1 · Splash Screen

🌿

Agri-SAGE

SCALABLE AGRICULTURAL GUIDANCE ENGINE

Powered by AI · Free for Farmers

2 · Onboarding

👨‍🌾

Your AI Farm Advisor

Get expert guidance in Malayalam, Tamil, or English — free, offline-capable

3 · Home Dashboard

Good morning,

Rajan's Farm 🌾

🌤️ 28°C · 82% humidity · Kalady

Quick Actions

🤖

Ask Advisor

AI farm guidance

🌧️

Weather

7-day forecast

📍

My Fields

3 active plots

⚠️

Alerts

2 new today

Alerts

🐛

Pest risk HIGH — paddy field 2. Check immediately

Today's Tasks

Apply fertiliser — Field 1

Before 9 AM

Soil moisture check

Done ✓

🏠Home

🤖Advisor

📍Fields

🌧️Weather

👤Profile

4 · AI Advisor Chat

### 🤖 Farm Advisor

14 AI agents · Responds in Malayalam

ML

EN

TA

HI

🤖

നമസ്കാരം! ഇന്ന് ഞാൻ നിങ്ങൾക്ക് എങ്ങനെ സഹായിക്കാം? (Hello! How can I help you today?)

9:02 AM

👨‍🌾

My paddy is yellowing. What to do?

9:04 AM

🤖

Nitrogen deficiency detected for your Jyothi variety. Apply urea at 40kg/acre. **Today's ideal window: 6–9 AM.** 💊

9:04 AM

5 · My Fields

### 📍 My Fields

🌾

Paddy Field — North

2.4 acres · Jyothi variety

Soil: Laterite · pH 6.2

Active

🥦

Vegetable Plot

0.8 acres · Mixed crops

Soil: Alluvial · pH 7.0

Harvesting

\+ Add New Field

🏠Home

🤖Advisor

📍Fields

🌧️Weather

👤Profile

6 · Weather & Forecast

📍 Kalady, Kerala

28°C

Partly Cloudy — Good for field work

82%

Humidity

12 km/h

Wind

4mm

Rain today

UV 7

UV Index

7-Day Forecast

Today

⛅

28°

Fri

🌧️

25°

Sat

⛈️

24°

Sun

🌤️

29°

Mon

☀️

31°

🤖 Agri-SAGE Advisory

Rain expected Fri–Sat. Delay chemical spraying to Sunday. Ideal fertiliser window: today before 9AM.

🏠Home

🤖Advisor

📍Fields

🌧️Weather

👤Profile

7 · Alerts & Notifications

### 🔔 Alerts

🐛

Pest Alert — Brown Planthopper

NBAIR data shows active BPH in your district. Field 1 at HIGH risk. Inspect tonight.

⏰ 2 hours ago

🌧️

Heavy Rain Warning

IMD alert: 40mm+ rainfall Friday. Ensure drainage channels are clear.

⏰ 5 hours ago

🌱

Crop Stage Update

DSSAT simulation: Paddy Field 1 entering tillering stage in 3 days. Apply potash.

⏰ Yesterday

✅

Soil Moisture Optimal

Field 2 moisture level is ideal. No irrigation needed for 48 hours.

⏰ Yesterday

🏠Home

🤖Advisor

📍Fields

🌧️Weather

👤Profile

8 · Profile & Settings

👨‍🌾

Rajan Pillai

📍 Kalady, Ernakulam · 3.2 acres

Farm Details

🌾Primary CropPaddy

📏Total Area3.2 acres

💧IrrigationCanal›

Preferences

🌐LanguageMalayalam›

🔔NotificationsEnabled›

📴Offline ModeOn

Account

🔒Privacy Policy›

🆘Help & Support›

🏠Home

🤖Advisor

📍Fields

🌧️Weather

👤Profile

Component Library

All reusable UI components with Jetpack Compose equivalents.

#### 🔘 Buttons

#### 📝 Inputs

⚠ This field is required

#### 🏷️ Status Badges

✅ Healthy ⚠️ Moderate Risk 🚨 Critical 💧 Irrigating

🌾 Paddy 🌿 Active Pending

#### 🔔 Toasts & Snackbars

✅ Fertiliser schedule saved

⚠️ Connection lost — offline mode

💡 Tip: Best spray time 6AM

#### 📊 Progress

Crop Growth68%

Soil Moisture45%

Pest Risk85%

#### 🔄 Toggle & Chips

Push notifications

Offline sync

🌾 Paddy

🌴 Coconut

🥦 Veg

🌶️ Spices

#### 📋 Bottom Sheet (Modal)

🤖 Advisory Generated

Apply 40kg urea/acre before rain. Spray at 6AM window. Check drainage on Friday.

#### 🌐 Language Selector

🇮🇳 ML

EN

🇮🇳 TA

🇮🇳 HI

Multilingual support: Malayalam, English, Tamil, Hindi — switches instantly

#### 📈 Stat Card

28°

Temperature

82%

Humidity

6.2

Soil pH

HIGH

Pest Risk

Motion & Animation System

Purposeful motion only. Every animation must communicate state change or guide attention — never decorate.

ℹ️All animations respect **reduceMotion** user preference. Disabled = instant state change, no animation.

#### ⏱️ Duration Scale

Micro: 80ms · Short: 150ms · Standard: 250ms · Long: 400ms · Extra: 600ms

#### 📐 Easing Curves

Enter: EaseOut · Exit: EaseIn · Emphasized: cubic-bezier(.22,1,.36,1)

🌱

#### 🔀 Screen Transitions

Shared element transition on card → detail. Slide-up for bottom sheets. Fade for tab switches.

📱 Home → 🤖 Advisor

#### 💫 Micro-interactions

Button press: scale(0.97). Toggle: spring physics. FAB: scale-up entry.

#### 🔔 Alert Entrance

Critical alerts: slide from top + haptic. Success: scale-up fade-in from center.

⚠️ Pest detected!

#### 💬 Chat Bubble

New AI message: fade + scale from bottom-left. User message: slide from right.

🤖 Advisory ready!

Compose Animation Patterns

// Standard card entrance — use in LazyColumn items AnimatedVisibility( visible = isVisible, enter = fadeIn(tween(250)) + slideInVertically( initialOffsetY = { it / 4 }, animationSpec = tween(300, easing = EaseOutQuart) ) ) // Shared element — card to detail screen Modifier.sharedElement( rememberSharedContentState(key = "field-${field.id}"), animatedVisibilityScope = scope ) // Button press haptic + scale val scale by animateFloatAsState( if (pressed) 0.96f else 1f, spring(dampingRatio = 0.6f) )

App Architecture & Navigation Flow

Complete user journey from install to daily farm management.

### User Onboarding Flow

📲

Install

→

🌿

Splash

→

👤

Language

→

📍

Location

→

🌾

Crop Setup

→

🏠

Dashboard

### AI Advisory Flow

💬

User Query

→

🔍

Intent Agent

→

🌤️

Weather Agent

→

🧪

Soil Agent

→

🌾

Crop Agent

→

✅

Response

### Navigation Graph — Type-Safe Compose Navigation 2.8.5

// Sealed destinations with kotlinx-serialization @Serializable object Home @Serializable object Advisor @Serializable data class FieldDetail(val fieldId: String) @Serializable object Weather @Serializable object Alerts @Serializable object Profile @Serializable data class Onboarding(val step: Int = 0) // Bottom nav tabs val bottomNavItems = listOf(Home, Advisor, Fields, Weather, Profile)

### Screen Hierarchy

| Screen | Route | Data Source | Offline? |
| --- | --- | --- | --- |
| Splash | /splash | Local | ✅ |
| Onboarding | /onboard/{step} | Local | ✅ |
| Home Dashboard | /home | Room + API | ✅ cached |
| AI Advisor | /advisor | FastAPI + LangGraph | ⚠ limited |
| Field Detail | /field/{id} | Room + DSSAT | ✅ |
| Weather | /weather | Open-Meteo API | ✅ 6hr cache |
| Alerts | /alerts | NBAIR + IMD RSS | ✅ cached |
| Profile | /profile | Room local | ✅ |

Master Build Prompt System

5-phase Cline + Gemini 2.5 Pro prompt system. Each phase is atomic, verifiable, and git-committed before next phase begins. Feed to Cline/Cursor at session start.

⚠️**Protocol:** Always run AUDIT first. Never start a phase if the previous phase's test gate shows red. Push git after each phase. Protect existing completed files.

0

MASTER RUNNER — Audit & Setup

Repository audit · Environment · Brain folder validation

Day 0

#### 🔍 Cline Session Start Prompt

\# AGRI-SAGE MASTER RUNNER — AUDIT PROTOCOL # Paste this at EVERY Cline/Cursor session start You are the Agri-SAGE AI Build Agent. Before taking ANY action: STEP 1 — READ brain/ folder Read ALL files in brain/ directory in this order: - 00_MASTER_RULES.md (architecture constraints) - 01_PRD.md (product requirements) - 02_ARCHITECTURE.md (system design) - 03_DATA_MODEL.md (DB schema) - 04_API_CONTRACT.md (endpoint specs) STEP 2 — AUDIT existing files List all files in: /android/app/src/, /backend/, /agents/, /tests/ Report: what exists, what is complete, what is partial. NEVER overwrite a file that already contains working code. If a file exists → improve only. If missing → create fresh. STEP 3 — CONFIRM before building Print audit report. Wait for human confirmation. Then proceed to the requested phase prompt only.

#### 📁 Required brain/ Files

00_MASTER_RULES.md 01_PRD.md 02_ARCHITECTURE.md 03_DATA_MODEL.md 04_API_CONTRACT.md 05_UI_UX_SPEC.md

1

Backend Foundation

FastAPI · PostgreSQL · LangGraph orchestration · 14 agents scaffold

Week 1

#### 🚀 Phase 1 Cline Prompt

\# PHASE 1 — BACKEND FOUNDATION # Run MASTER RUNNER audit first. Then execute: TARGET: Build production FastAPI backend with all 14 AI agents scaffolded and PostgreSQL + pgvector ready. TECH (pinned — DO NOT change versions): - FastAPI 0.115.0 (lifespan pattern, NOT @app.on_event) - PostgreSQL 16 + pgvector 0.4.0 (HNSW index, m=16, ef=64) - LangGraph 1.0.8 (START/END constants, MemorySaver) - Embeddings: multilingual-e5-large (query: prefix) - LLM: Gemini Flash 2.0 free tier (primary) BUILD ORDER: 1. /backend/main.py — FastAPI app with lifespan 2. /backend/database.py — PostgreSQL async engine 3. /backend/models/ — SQLAlchemy models (Farm, Field, Advisory, Alert, WeatherCache, SoilData) 4. /backend/agents/\_\_init\_\_.py — LangGraph graph setup 5. /backend/agents/ — Scaffold 14 agents: intent, weather, soil, crop, pest, irrigation, market, fertiliser, dssat, scheduler, alert, translator, memory, supervisor 6. /backend/api/v1/ — Routers: advisory, weather, fields, alerts, auth, health 7. alembic/ — Migration setup 8. requirements.txt — All pinned versions 9. docker-compose.yml — Postgres + Redis + API VALIDATION GATE: - \[ \] \`uvicorn main:app --reload\` starts without error - \[ \] All 14 agent files exist with proper structure - \[ \] pgvector extension enabled and HNSW index created - \[ \] /api/v1/health returns 200 - \[ \] All models migrate successfully ON COMPLETION: git add -A && git commit -m "phase1: backend foundation" git push origin dev/m1-backend

#### ✅ Phase 1 Deliverables

- FastAPI app with lifespan context manager
- Async PostgreSQL with pgvector HNSW index
- LangGraph orchestrator with 14 agent nodes
- Full API router structure (/api/v1/\*)
- Alembic migrations working
- Docker Compose for local dev

#### ⚙️ Tech Stack

FastAPI 0.115 PostgreSQL 16 pgvector 0.4 LangGraph 1.0.8 Gemini Flash Alembic Docker

2

Data Pipelines & Agents

8 free real-time sources · Agent intelligence · DSSAT integration

Week 2–3

#### 🚀 Phase 2 Cline Prompt

\# PHASE 2 — DATA PIPELINES & AGENT INTELLIGENCE TARGET: Connect all 8 free real-time data sources and implement full agent logic for weather, soil, pest, crop, irrigation, market agents. DATA SOURCES (all free, no key needed unless noted): 1. Open-Meteo API — weather + forecast (free, no key) URL: api.open-meteo.com/v1/forecast 2. NASA EarthData APPEEARS — satellite NDVI (free signup) 3. data.gov.in — government agricultural data 4. IMD API — India Meteorological Dept alerts 5. NBAIR RSS feed — pest alerts (no key) 6. NBSS soil data — National Bureau Soil Survey 7. KAU PDF scraper — Kerala Ag Univ recommendations 8. Gemini Flash free tier — LLM reasoning BUILD ORDER: 1. /backend/services/data_fetcher.py - Async fetchers for all 8 sources - Retry logic (3 attempts, exponential backoff) - Response caching in PostgreSQL (TTL per source) - Graceful degradation on source failure 2. /backend/agents/weather_agent.py (FULL implementation) - Consume Open-Meteo + IMD - Generate 7-day forecast with ag advisory - Calculate evapotranspiration (FAO-56 method) 3. /backend/agents/soil_agent.py (FULL) - NBSS data lookup by GPS coordinates - pH, N/P/K status, texture classification 4. /backend/agents/pest_agent.py (FULL) - NBAIR RSS parser - District-level risk scoring - Threshold alerts (critical/warning/info) 5. /backend/agents/crop_agent.py (FULL) - DSSAT simulation bridge - Growth stage tracking - Yield prediction 6. /backend/agents/irrigation_agent.py (FULL) - Soil moisture × weather × crop stage - Irrigation schedule generation 7. /backend/agents/translator_agent.py (FULL) - Gemini Flash for ML/TA/HI translation - Fallback: Google Translate free tier 8. /backend/services/dssat_bridge.py - DSSAT subprocess wrapper - Input file generation from farm data - Output parsing → JSON VALIDATION GATE: - \[ \] Open-Meteo returns forecast for Kalady, Kerala - \[ \] NBAIR RSS parsed and 3+ alerts stored in DB - \[ \] DSSAT simulation runs without error - \[ \] All 6 agent tests pass (pytest /tests/agents/) - \[ \] Translator returns Malayalam for English input ON COMPLETION: git add -A && git commit -m "phase2: data pipelines + agents"

#### ✅ Phase 2 Deliverables

- All 8 data sources connected and cached
- Weather, Soil, Pest, Crop, Irrigation agents fully implemented
- DSSAT bridge functional with test simulation
- Multilingual translator agent working
- 100% graceful degradation — no single-source failure breaks app

3

Android App — Jetpack Compose

All 8 screens · Room DB · Retrofit · Offline-first architecture

Week 4–5

#### 🚀 Phase 3 Cline Prompt

\# PHASE 3 — ANDROID APP COMPLETE TARGET: Build complete Kotlin/Compose Android app with all 8 screens, offline-first Room database, Retrofit API client, and full MVVM architecture. TECH (pinned — DO NOT change): - Kotlin 2.0+ with KSP (NOT kapt — kapt is deprecated) - Jetpack Compose with Material3 (Material You) - Navigation Compose 2.8.5 (type-safe, serialization) - Room 2.7.0 with KSP annotation processing - Retrofit 2.11 + OkHttp 4.12 + Moshi - Hilt 2.51 (Dependency Injection) - DataStore Preferences (NOT SharedPreferences) - WorkManager 2.9.1 (background sync) - Kotlin Coroutines + Flow - Coil 2.6 (image loading) ARCHITECTURE: MVVM + Repository pattern - UI Layer: Compose screens + ViewModels - Domain Layer: Use cases - Data Layer: Room + Retrofit repositories BUILD ORDER: ## 1. Project Setup - build.gradle.kts (Kotlin DSL, all versions pinned) - libs.versions.toml version catalog - Hilt setup (Application class, hiltViewModel) - NavGraph with all serializable routes ## 2. Design System - ui/theme/Color.kt — all tokens from UI spec - ui/theme/Type.kt — Nunito + Inter scale - ui/theme/Theme.kt — AgriSageTheme light/dark - ui/theme/Shape.kt — border radius scale ## 3. All 8 Screens - SplashScreen.kt (animated logo, auto-navigate 2s) - OnboardingScreen.kt (3-step, language select) - HomeScreen.kt (dashboard, quick actions, alerts, tasks) - AdvisorScreen.kt (chat UI, voice input, lang switch) - FieldsScreen.kt (list + map placeholder + FAB) - WeatherScreen.kt (current + 7-day + advisory banner) - AlertsScreen.kt (categorised alerts + read/dismiss) - ProfileScreen.kt (farm details + settings + language) ## 4. Components - AgriButton.kt (primary, secondary, danger, gold) - AgriCard.kt (with border, shadow, press animation) - AlertBanner.kt (critical, warning, info, success) - StatCard.kt (icon + value + label) - BottomNavBar.kt (5 tabs, badge support) - LanguageChip.kt (ML/EN/TA/HI) - LoadingDots.kt (3 animated dots) - ErrorState.kt (icon + message + retry) - EmptyState.kt (illustration + CTA) ## 5. Data Layer - Room entities: Farm, Field, Advisory, Alert, Weather - DAOs with Flow return types - Retrofit service interface matching /api/v1/\* exactly - Repository implementations with offline-first logic: * Load from Room → emit → fetch API → update Room → emit ## 6. ViewModel Layer - HomeViewModel (dashboard aggregation) - AdvisorViewModel (chat history, streaming response) - FieldViewModel (CRUD, map data) - WeatherViewModel (forecast + ag advisory) - AlertViewModel (alert list, mark read, filter) ## 7. Background Work - WeatherSyncWorker (WorkManager, 6hr interval) - AlertSyncWorker (WorkManager, 1hr interval) - DataStoreManager (user prefs, language, farm setup) VALIDATION GATE: - \[ \] App builds with \`./gradlew assembleDebug\` zero errors - \[ \] All 8 screens navigate without crash - \[ \] Room migrations clean (no missing migration error) - \[ \] Advisor screen sends query, receives response - \[ \] App works fully offline with cached data - \[ \] No deprecated APIs (no kapt, no SharedPreferences) ON COMPLETION: git add -A && git commit -m "phase3: android app complete" git push origin dev/m2-android

#### ⚙️ Android Tech Stack

Kotlin 2.0 Compose Material3 Navigation 2.8.5 Room 2.7 Hilt 2.51 WorkManager KSP DataStore Coil 2.6

4

Deployment & Integration

Railway free tier · CI/CD · Push notifications · End-to-end test

Week 6–7

#### 🚀 Phase 4 Cline Prompt

\# PHASE 4 — DEPLOYMENT & INTEGRATION TARGET: Deploy backend to Railway free tier, connect Android app to production API, setup GitHub Actions CI, enable push notifications via Firebase FCM (free). DEPLOYMENT (Railway free tier — zero cost): 1. railway.toml — build + start commands 2. Dockerfile — multi-stage (builder + runner) Base: python:3.12-slim (NOT full python) Max image: 500MB compressed 3. Environment variables in Railway dashboard: DATABASE_URL, GEMINI_API_KEY, SECRET_KEY 4. Health check: /api/v1/health (Railway requirement) 5. Custom domain: agrisage.railway.app CI/CD (GitHub Actions free tier): - .github/workflows/backend-ci.yml trigger: push to main/dev branches steps: lint → test → build docker → deploy Railway - .github/workflows/android-ci.yml trigger: push to dev/m2-android steps: ktlint → unit tests → assembleDebug NOTIFICATIONS (Firebase FCM — free): 1. Firebase project setup (free Spark plan) 2. FCM token registration in Android app 3. /backend/services/notification_service.py - Send push to specific farm user - Alert categories: PEST_CRITICAL, WEATHER_WARNING, CROP_STAGE, IRRIGATION_REMINDER, ADVISORY_READY 4. Background notification handler in Android PRODUCTION CONFIG: - CORS: allow Android app origin only - Rate limiting: 100 req/min per user (Redis) - Response compression (gzip) - Structured logging (structlog) - Error tracking (Sentry free tier) VALIDATION GATE: - \[ \] Backend live at https://agrisage.railway.app - \[ \] /api/v1/health returns 200 from Railway - \[ \] Android app connects to production URL - \[ \] Push notification received on test device - \[ \] GitHub Actions green on both workflows - \[ \] Zero secrets in git history ON COMPLETION: git add -A && git commit -m "phase4: deployment live"

#### ✅ Phase 4 Deliverables

- Backend live on Railway with custom domain
- Android app builds and connects to production
- FCM push notifications working end-to-end
- GitHub Actions CI/CD pipelines green
- Zero-cost deployment confirmed

5

QA, Polish & Demo Ready

Full test suite · Performance · HR demo build · APK generation

Week 8

#### 🚀 Phase 5 Cline Prompt

\# PHASE 5 — QA, POLISH & DEMO READY TARGET: Full test coverage, performance audit, UI polish, generate demo APK, prepare HR presentation build. TESTING: 1. /tests/agents/ — pytest for all 14 agents (mock APIs) 2. /tests/api/ — FastAPI TestClient for all endpoints 3. /tests/integration/ — end-to-end advisory flow test 4. Android — Unit tests for all ViewModels (JUnit5) 5. Android — UI tests for critical flows (Compose testing) - Onboarding flow completion - Advisor query → response - Alert tap → detail view PERFORMANCE TARGETS: - API response: \< 2s for advisory (p95) - App cold start: \< 2s on mid-range Android (API 29+) - Database query: \< 100ms (all indexed) - Memory: \< 150MB heap on device - APK size: \< 25MB (enable R8 + resource shrinking) UI POLISH: 1. Verify all animations (reduceMotion respected) 2. Malayalam, English, Tamil: test all 3 languages 3. Offline → Online transition: smooth state recovery 4. Dark mode: verify all color tokens work correctly 5. Accessibility: TalkBack testing on all screens 6. Landscape orientation: handled or locked (choose) DEMO BUILD: 1. Pre-seed demo data: Rajan's farm in Kalady - 2 fields, historical weather, 3 cached advisories - 2 active pest alerts, 7-day forecast 2. Demo mode toggle in Profile (no API key needed) 3. Generate signed APK: \`./gradlew assembleRelease\` 4. QR code for demo installation DOCUMENTATION: 1. README.md — setup, architecture, team 2. API_DOCS.md — all endpoints documented 3. DEMO_SCRIPT.md — 5-minute HR demo walkthrough VALIDATION GATE: - \[ \] pytest: 90%+ coverage, zero failures - \[ \] Advisory response \< 2s in production - \[ \] APK installs and runs on Android 10+ device - \[ \] Malayalam UI fully functional - \[ \] Demo script tested end-to-end, 5 min timing FINAL COMMIT: git tag v1.0.0-demo git push --tags

#### ✅ Final Deliverables

- 90%+ test coverage, all tests green
- Signed demo APK \< 25MB
- 5-minute HR demo script validated
- Malayalam UI tested end-to-end
- README and API docs complete
- v1.0.0-demo git tag pushed

📅 8-Week Sprint Timeline

| Week | Phase | Branch | Owner | Gate |
| --- | --- | --- | --- | --- |
| 0 | Setup + Audit | main | M1 (Magnel) | brain/ files ✓ |
| 1 | Phase 1: Backend | dev/m1-backend | M1 | API health 200 |
| 2–3 | Phase 2: Agents | dev/m3-agents | M3 | 6/6 agents tested |
| 4–5 | Phase 3: Android | dev/m2-android | M2 | APK builds clean |
| 6–7 | Phase 4: Deploy | dev/m1-backend | M1 + M4 | Live URL works |
| 8 | Phase 5: QA/Demo | dev/m5-tests | M5 | Demo APK ready |

Accessibility & Multilingual

WCAG 2.1 AA target. TalkBack compatible. Kerala farmer-first UX decisions.

#### 🎨 Color Contrast

All text meets AA minimum 4.5:1 ratio. Large text meets 3:1.

White on Sage — 8.2:1 ✓

Deep text on pale — 12:1 ✓

#### 👆 Touch Targets

Minimum 48×48dp for all interactive elements. Critical controls: 56×56dp.

48dp

56dp

#### 📢 TalkBack

All icons have contentDescription. Semantic roles set. Reading order defined.

Image( painter = painterResource(R.drawable.ic_pest), contentDescription = "Pest alert icon" )

#### 🌐 Languages

Malayalam, English, Tamil, Hindi. RTL layouts handled via LayoutDirection.

മലയാളം

English

தமிழ்

हिन्दी

#### 📵 Offline Mode

All critical features work without internet. Clear offline indicator. Auto-sync when reconnected.

📴 Offline — Showing cached data from 2h ago

#### ✋ Reduce Motion

All animations check reduceMotion preference. Disabled = instant transitions.

val reduceMotion = LocalAccessibilityManager .current?.isReduceMotionEnabled val duration = if (reduceMotion) 0 else 300

#### 📱 Font Scaling

All text in sp units. Layouts use weight/fillMaxWidth, not fixed height. Text wraps correctly at 200% font scale.

#### 🌾 Farmer UX Principles

Large tap targets for field workers. Emoji icons for non-literate users. Voice input on all text fields. Simple 1-tap task completion.

#### 🔋 Low-End Device

Tested on Android 9+ (API 28). Target min SDK 26. Memory \< 150MB. No heavy 3D animations. Bitmap caching via Coil.

**Agri-SAGE** — Scalable Agricultural Guidance Engine\
Built by Magnel & team · ASIET Kalady · Kerala, India\
Zero-budget · Open-source · Farmer-first · 2026