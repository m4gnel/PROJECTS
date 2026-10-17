# 🌾 AGRI-SAGE — MASTER BUILD PROMPT
## Complete Android App Build System for Gemini 2.5 Flash High
### Version 2.0 — India-Wide · Production-Grade · Zero Budget

---

> **HOW TO USE THIS FILE**
> Paste this entire file into Gemini 2.5 Flash High at session start.
> Gemini will work phase by phase, verify each phase fully, then push to GitHub via Issues before moving to the next.
> Do NOT skip phases. Do NOT proceed if a validation gate shows red.
> Time budget: ~6 hours total. Each phase has a time estimate.

---

## ⚙️ GLOBAL RULES — READ BEFORE ANYTHING ELSE

```
IDENTITY: You are the Agri-SAGE Senior Build Agent.
PROJECT: Agri-SAGE — AI agricultural advisor for ALL Indian farmers (not just Kerala).
PLATFORM: Android (Kotlin + Jetpack Compose) + FastAPI backend.
BUDGET: Zero cost — only free APIs, free tiers, open-source.
LANGUAGES: Hindi, Malayalam, Tamil, English, Telugu, Punjabi (6 primary).

RULE 1 — AUDIT BEFORE TOUCH:
Before modifying ANY existing file:
  a) Read the file completely
  b) Score it: Completeness (0-10), Correctness (0-10), Production-Ready (0-10)
  c) Score >= 8 on ALL three = PROTECTED. Do NOT rewrite. Only improve/extend.
  d) Any score < 8 = NEEDS_WORK. Fix what is specifically wrong.
  e) Print audit table before building anything.

RULE 2 — GITHUB ISSUES (NOT direct push to main):
After each phase completes and is verified:
  Step 1: git add -A
  Step 2: git commit -m "feat(phase-N): <description>"
  Step 3: git push origin dev/<branch-name>
  Step 4: Create GitHub Issue with title "[Phase N Complete] <title>"
           Body must include:
           - Files created (list every file)
           - Files protected (skipped because already complete)
           - Validation gate results (paste actual output)
           - How to review: git checkout <branch> && <test command>
           - Label: phase-N, ready-for-review
           - Assign: @Magnel
  Step 5: Print "✅ Phase N pushed. Issue created. Awaiting review."
  Step 6: STOP. Do not proceed to next phase until told to continue.

RULE 3 — ZERO HALLUCINATION:
  - If unsure about a library version → use the exact version in LOCKED VERSIONS below
  - If unsure about an API endpoint shape → print "UNCERTAIN: <detail>" and use safe fallback
  - Never invent API fields, library methods, or file paths
  - Gemini model string: "gemini-1.5-flash" (exact — not "gemini-flash" or "gemini-2.0")

RULE 4 — VERSION LOCK (NEVER change these):
  Backend:
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
    structlog==24.4.0
    pytest==8.3.4
    pytest-asyncio==0.24.0
    ruff==0.7.1

  Android:
    compileSdk = 35
    minSdk = 26
    targetSdk = 35
    kotlin_version = "2.0.21"
    compose_bom = "2024.09.00"
    navigation_compose = "2.8.5"
    room_version = "2.7.0"
    ksp_version = "2.0.21-1.0.27"    ← KSP ONLY, never kapt
    hilt_version = "2.52"
    retrofit_version = "2.11.0"
    okhttp_version = "4.12.0"
    coil_version = "2.7.0"
    datastore_version = "1.1.1"
    workmanager_version = "2.10.0"
    moshi_version = "1.15.1"
    coroutines_version = "1.9.0"

RULE 5 — REAL DEVICE WORKFLOW:
  All code must work on a real Android device connected via USB/Wireless ADB.
  Use @Preview annotations on every composable for instant desktop preview.
  Test voice input only on real device (emulator STT is unreliable for Indian languages).

RULE 6 — TIME DISCIPLINE:
  Phase 0: 20 min
  Phase 1: 60 min
  Phase 2: 90 min
  Phase 3: 120 min
  Phase 4: 45 min
  Phase 5: 45 min
  Phase 6: 60 min
  Total: ~6 hours
  If a phase is taking longer, print a warning and list what is blocking.
```

---

## 📁 REQUIRED REPOSITORY STRUCTURE

```
agrisage/
├── brain/                          ← AI agent reads this every session
│   ├── 00_MASTER_RULES.md
│   ├── 01_PRD.md
│   ├── 02_ARCHITECTURE.md
│   ├── 03_DATA_MODEL.md
│   ├── 04_API_CONTRACT.md
│   ├── 05_UI_UX_SPEC.md
│   └── kerala_soil_data.json       ← + national soil zones
├── android/
│   ├── app/
│   │   ├── build.gradle.kts
│   │   └── src/main/
│   │       ├── AndroidManifest.xml
│   │       ├── AgriSageApplication.kt
│   │       ├── MainActivity.kt
│   │       ├── data/
│   │       │   ├── local/
│   │       │   │   ├── AgriSageDatabase.kt
│   │       │   │   ├── dao/
│   │       │   │   └── entities/
│   │       │   ├── remote/
│   │       │   │   ├── AgriSageApiService.kt
│   │       │   │   └── dto/
│   │       │   └── repository/
│   │       ├── di/
│   │       ├── domain/usecases/
│   │       ├── ui/
│   │       │   ├── theme/
│   │       │   ├── screens/
│   │       │   ├── components/
│   │       │   └── viewmodel/
│   │       └── util/
│   ├── build.gradle.kts
│   ├── settings.gradle.kts
│   ├── gradle/libs.versions.toml
│   └── local.properties.example
├── backend/
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── models/
│   │   ├── agents/
│   │   ├── services/
│   │   ├── routers/
│   │   └── schemas/
│   ├── migrations/
│   ├── tests/
│   ├── scripts/
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── railway.toml
│   └── .env.example
├── .github/
│   ├── workflows/
│   │   ├── backend-ci.yml
│   │   └── android-ci.yml
│   ├── ISSUE_TEMPLATE/
│   │   └── phase_complete.md
│   └── pull_request_template.md
├── .gitignore
└── README.md
```

---

## 🎨 DESIGN SYSTEM — LOCKED TOKENS

### Colors
```kotlin
// ui/theme/Color.kt — EXACT values, do not change

// Primary — Sage Green (India's agricultural identity)
val SageDeep     = Color(0xFF1B4332)
val SageMid      = Color(0xFF2D6A4F)
val SageLight    = Color(0xFF40916C)
val SageLeaf     = Color(0xFF52B788)
val SagePale     = Color(0xFFD8F3DC)

// Surface
val SurfaceWhite = Color(0xFFFAFDF8)
val Surface1     = Color(0xFFF1F8F1)
val Surface2     = Color(0xFFE8F4E8)
val SurfacePale  = Color(0xFFF8FCF8)

// Soil Accent (for contrast CTAs)
val SoilLaterite = Color(0xFF7C4D26)
val SoilLight    = Color(0xFFF0E0D0)

// Alert System
val AlertCritical = Color(0xFFDC2626)   // Red — pest outbreak, flood
val AlertWarning  = Color(0xFFF59E0B)   // Amber — rain, temperature
val AlertInfo     = Color(0xFF2563EB)   // Blue — crop stage, advisory
val AlertSuccess  = Color(0xFF16A34A)   // Green — optimal conditions

// Alert backgrounds
val AlertCriticalBg = Color(0xFFFEE2E2)
val AlertWarningBg  = Color(0xFFFEF3C7)
val AlertInfoBg     = Color(0xFFDBEAFE)
val AlertSuccessBg  = Color(0xFFDCFCE7)

// Text
val TextPrimary   = Color(0xFF1B4332)
val TextSecondary = Color(0xFF3D7A5C)
val TextMuted     = Color(0xFF6B7280)
val TextOnDark    = Color(0xFFFFFFFF)
```

### Typography
```kotlin
// ui/theme/Type.kt
// Download fonts: Nunito (900 weight) + Inter (400/500/600)
// Place in res/font/

val AgriSageTypography = Typography(
    displayLarge  = TextStyle(fontFamily = NunitoFamily, fontSize = 32.sp, fontWeight = FontWeight.Black),
    headlineLarge = TextStyle(fontFamily = NunitoFamily, fontSize = 24.sp, fontWeight = FontWeight.ExtraBold),
    headlineMedium= TextStyle(fontFamily = NunitoFamily, fontSize = 18.sp, fontWeight = FontWeight.Bold),
    bodyLarge     = TextStyle(fontFamily = InterFamily,  fontSize = 15.sp, fontWeight = FontWeight.Medium),
    bodyMedium    = TextStyle(fontFamily = InterFamily,  fontSize = 13.sp, fontWeight = FontWeight.Normal),
    labelSmall    = TextStyle(fontFamily = InterFamily,  fontSize = 11.sp, fontWeight = FontWeight.SemiBold),
)
```

### Spacing & Shapes
```kotlin
// ui/theme/Shape.kt
val Shapes = Shapes(
    extraSmall = RoundedCornerShape(8.dp),
    small      = RoundedCornerShape(12.dp),
    medium     = RoundedCornerShape(16.dp),
    large      = RoundedCornerShape(24.dp),
    extraLarge = RoundedCornerShape(32.dp),
)

// Spacing constants — use these, never magic numbers
object Spacing {
    val xs = 4.dp
    val sm = 8.dp
    val md = 16.dp
    val lg = 24.dp
    val xl = 32.dp
}
```

---

## 📱 ALL 8 SCREENS — COMPLETE SPEC

### Screen 1: Splash Screen
```
Route: /splash
Auto-navigate to: Onboarding (first launch) OR Home (returning user)
Delay: 2000ms
Animation: Logo scale in (0.8 → 1.0, 600ms EaseOutBack) + fade in tagline (400ms delay)

Layout:
  Background: SageDeep gradient (top) to SageMid (bottom) — use hardcoded hex, not theme vars
  Center:
    - Agri-SAGE leaf logo SVG (64dp × 64dp, white)
    - "Agri-SAGE" text (Display, white, 32sp, Nunito 900)
    - "SCALABLE AGRICULTURAL GUIDANCE ENGINE" (Caption, white 60% alpha, 11sp, letter-spacing 2)
    - SizedBox 24dp
    - "Powered by AI · Free for Farmers" (Body, white 80% alpha, 13sp)
    - SizedBox 48dp
    - LinearProgressIndicator (color=SageLeaf, trackColor=white20%, width=120dp, height=3dp)
  Bottom:
    - "Version 1.0" (Caption, white 40% alpha)
    - "Built at ASIET Kalady" (Caption, white 40% alpha)

State logic:
  val context = LocalContext.current
  val dataStore = DataStoreManager(context)
  LaunchedEffect(Unit) {
      delay(2000)
      val isOnboarded = dataStore.isOnboardingComplete.first()
      if (isOnboarded) navController.navigate(Home) { popUpTo(Splash) { inclusive = true } }
      else navController.navigate(Onboarding(step = 0)) { popUpTo(Splash) { inclusive = true } }
  }
```

### Screen 2: Onboarding (3 steps)
```
Route: /onboard/{step}  (step = 0, 1, 2)
Progress: Dot indicators at top (3 dots, active = SageLeaf filled, inactive = Surface2)

STEP 0 — Language Selection:
  Title: "Choose your language" (H1, TextPrimary)
  Subtitle: "Get advice in the language you're comfortable with"
  Grid (2 columns):
    LanguageChip("हिंदी", "Hindi",     flag="🇮🇳", code="hi")
    LanguageChip("English", "English",  flag="🏴", code="en")
    LanguageChip("தமிழ்", "Tamil",    flag="🇮🇳", code="ta")
    LanguageChip("മലയാളം", "Malayalam", flag="🇮🇳", code="ml")
    LanguageChip("తెలుగు", "Telugu",  flag="🇮🇳", code="te")
    LanguageChip("ਪੰਜਾਬੀ", "Punjabi", flag="🇮🇳", code="pa")
  Save: DataStore → selected_language
  CTA: "Continue" button (Primary, full-width)

STEP 1 — Location:
  Title: "Where is your farm?"
  State dropdown: All 28 Indian states + UTs (use official list, not just Kerala)
  District dropdown: Loads dynamically based on state selection
  GPS button: "Use my location" → FusedLocationProvider → reverse geocode
  Farm size input: NumberField + "acres" / "hectares" toggle
  Save to DataStore: state, district, lat, lon, farm_size_acres
  CTA: "Continue"

STEP 2 — Crop Setup:
  Title: "What do you grow?"
  Subtitle: "Select all that apply — you can change this later"
  Crop chips (multi-select, scrollable grid):
    NATIONAL CROPS (show all, not just Kerala):
    Wheat, Rice/Paddy, Cotton, Sugarcane, Maize/Corn, Soybean
    Mustard, Groundnut, Sunflower, Onion, Potato, Tomato
    Chilli, Turmeric, Ginger, Garlic, Peas, Lentils (Dal)
    Coconut, Banana, Mango, Pomegranate, Grapes, Papaya
    Rubber, Cardamom, Pepper, Tea, Coffee, Arecanut
    Other (text input)
  Save to DataStore: selected_crops (List<String>)
  CTA: "Start Farming with AI 🌾"
  Action: navigate to Home, set onboarding_complete = true
```

### Screen 3: Home Dashboard
```
Route: /home
Data: HomeViewModel → combines WeatherRepository + AlertRepository + TaskRepository

TopBar:
  Left: "Good morning/afternoon/evening, [name]" (dynamic based on time)
  Subtitle: "[Farm name] · [district], [state]"
  Right: Bell icon with badge (unread alert count), tap → Alerts screen

Weather Strip (Card, full-width, SageDeep background):
  Left: Temperature (H1, white) + description (Body, white 80%)
  Right: Weather icon (emoji or Material Symbol)
  Row below: Humidity | Wind | Rain today | UV Index (4 stat chips, white)
  Tap → Weather screen

Alert Banner (shows only if active alerts exist):
  Background: AlertCriticalBg for HIGH, AlertWarningBg for MEDIUM
  Icon + Title + short description
  "View all →" link
  Swipe to dismiss

Quick Actions Grid (2×2):
  [🤖 Ask Advisor]    → Advisor screen
  [🌧️ Weather]        → Weather screen
  [📍 My Fields]      → Fields screen
  [🔔 Alerts (badge)] → Alerts screen

Today's Tasks (LazyColumn, max 3 shown):
  Each task: checkbox + title + time + field name
  Tap checkbox → marks done, crosses out with animation
  "View all tasks →" link

Market Prices Widget (if data available):
  Title: "Today's prices near you"
  2-3 crop rows: Crop name | APMC market | Price/quintal | UP/DOWN/STABLE badge
  "See more →" → full market screen

Bottom Navigation:
  🏠 Home (active)  🤖 Advisor  📍 Fields  🌧️ Weather  👤 Profile
  Each item: icon + label (11sp) + badge for alerts
```

### Screen 4: AI Advisor Chat
```
Route: /advisor
Data: AdvisorViewModel → chat history (Room) + streaming FastAPI response

TopBar:
  Left: Back arrow
  Center: "🤖 Farm Advisor" + subtitle "14 AI agents · Online/Offline"
  Right: Language toggle chips (ML | EN | TA | HI | TE | PA) — horizontal scroll

Chat area (LazyColumn, reversed):
  AI bubble: Left-aligned, white card, SageLeaf left-border 3dp, fade+slide animation
    - Content: advisory text
    - Source badge: "📡 Weather + Soil data" (shows which agents were used)
    - Timestamp (Caption, TextMuted)
    - Speak button (text-to-speech in selected language)
  User bubble: Right-aligned, SageMid background, white text, slide-from-right animation
    - Content: user message
    - Timestamp

Input area (sticky bottom):
  Language selector row: "Responding in: [active language chip]"
  Input row:
    - TextField: "Type or speak your question..." (multiline, max 3 lines)
    - Mic button (SageLight background) → SpeechRecognizer with EXTRA_LANGUAGE = selected_lang + "-IN"
    - Send button (SageDeep, arrow icon) → enabled only when text not empty

Empty state (first open):
  "🌾 Ask me anything about your farm"
  3 suggestion chips: "My crop is yellowing", "When to irrigate?", "Pest on my paddy"
  Tap chip → pre-fills input and sends

Offline state:
  Banner: "📴 Offline — Limited advisor mode. Last 10 responses available."
  Still shows chat history from Room
```

### Screen 5: My Fields
```
Route: /fields
Data: FieldViewModel → Room FieldEntity list

TopBar: "📍 My Fields" + "Add Field" FAB (SageMid, + icon, bottom-right)

Field list (LazyColumn):
  Each FieldCard:
    - Crop emoji + crop name (H2)
    - Field name (Body Large, TextPrimary)
    - "[X] acres · [variety]" (Body, TextMuted)
    - "Soil: [texture] · pH [value]" (Caption)
    - Status badge: Active / Harvesting / Fallow / Resting
    - Tap → FieldDetailScreen (shared element transition on card)

Field Detail (sub-screen):
  Route: /field/{fieldId}
  Top: Large header with field name + crop + area
  Sections:
    - Soil health (pH bar, N/P/K gauges)
    - Current crop stage (timeline: Sowing→Germination→Growth→Flowering→Harvest)
    - DSSAT prediction (next stage in X days, predicted yield)
    - Advisory history (last 5 advisories from Room)
    - Weather for this field (uses field GPS, not farm GPS)

Add Field Bottom Sheet:
  Fields:
    - Field name (TextField)
    - Crop type (dropdown — same crop list as onboarding)
    - Variety (TextField, optional)
    - Area in acres (NumberField)
    - Soil type (dropdown: Laterite, Alluvial, Black, Red, Sandy, Loamy, Clay)
    - Irrigation type (dropdown: Canal, Borewell, Rain-fed, Drip, Sprinkler)
    - GPS coordinates (auto-fill from current location OR manual)
  Save → Room → dismiss sheet → list refreshes
```

### Screen 6: Weather & Forecast
```
Route: /weather
Data: WeatherViewModel → Open-Meteo API (6hr cache in Room)

Current conditions card (SageDeep bg):
  Location: "[District], [State]" with GPS icon
  Temperature: Large (Display, 32sp, white)
  Description: "Partly Cloudy — Good for field work" (H2, white 80%)
  Stats row: Humidity | Wind | Rain today | UV Index | Feels like

7-Day forecast row (horizontal scroll):
  Each day: Day name | Weather icon | High/Low temp
  Today is highlighted (SageLeaf border)

AI Advisory Banner:
  "🤖 Agri-SAGE Advisory" header (SageMid bg)
  Text: specific farming advice based on current conditions
  Example: "Rain expected Thu–Fri. Delay chemical spraying to Saturday. Ideal fertiliser window: today before 9AM."

Farming conditions today:
  Cards for: Spray condition | Irrigation need | Field work suitability
  Each card: icon + "Good/Fair/Poor" + reason

Historical rainfall chart:
  Last 7 days bar chart (simple, no library — draw with Canvas)
```

### Screen 7: Alerts & Notifications
```
Route: /alerts
Data: AlertViewModel → Room AlertEntity (from NBAIR RSS + IMD + app-generated)

Filter chips (top, horizontal scroll):
  All | Pest 🐛 | Weather 🌧️ | Crop 🌾 | Market 💰 | Soil 🧪

Alert list (LazyColumn):
  Each AlertCard by severity:
    CRITICAL (red left border, AlertCriticalBg):
      - Large icon (🐛 or ⛈️) + CRITICAL badge
      - Title (H2, AlertCritical color)
      - Description (Body, TextPrimary)
      - Source: "NBAIR data" or "IMD alert"
      - Time: "2 hours ago"
      - Action button: "Ask AI what to do →" → Advisor with context pre-filled
      - Dismiss: swipe right

    WARNING (amber left border, AlertWarningBg):
      Same layout, amber colors, "Ask AI" or "View details"

    INFO (blue border, AlertInfoBg):
      Crop stage updates, DSSAT predictions — informational, no action needed

    SUCCESS (green border, AlertSuccessBg):
      "Soil moisture optimal" etc — positive confirmations

  Empty state: "✅ No active alerts. Your farm is doing well."
```

### Screen 8: Profile & Settings
```
Route: /profile
Data: ProfileViewModel → DataStore + Room FarmEntity

Header:
  Avatar (initials, SageMid circle, 72dp)
  Farmer name (H1)
  "[District], [State] · [X] acres" (Body, TextMuted)

Section — Farm Details (tappable rows):
  🌾 Primary Crop    → [value] → CropPicker sheet
  📏 Total Area      → [value] acres → NumberInput
  💧 Irrigation      → [value] → dropdown
  📍 Location        → [state, district] → LocationPicker
  🌾 My Fields       → "[N] fields" → Fields screen

Section — Preferences:
  🌐 Language        → [language] → LanguagePicker (same 6 options)
  🔔 Notifications   → Toggle (DataStore)
  📴 Offline Mode    → Toggle (WorkManager sync frequency)
  🔊 Voice responses → Toggle (TTS on advisor responses)

Section — Account:
  📊 My Season       → season summary (advisory count, alerts handled)
  🔒 Privacy Policy  → WebView or external link
  🆘 Help & Support  → FAQ bottom sheet
  🔄 Clear cache     → confirmation dialog + Room clear
  ℹ️ App version 1.0.0 (Caption, TextMuted)
```

---

## 🤖 AGENT SYSTEM — ALL 14 AGENTS

```
Agent 1:  IntentAgent      — Classifies query into WEATHER|PEST|SOIL|CROP|IRRIGATION|MARKET|GENERAL
Agent 2:  TranslatorAgent  — Detects language, translates to EN for processing, translates response back
Agent 3:  WeatherAgent     — Open-Meteo + IMD → forecast + farming advisory
Agent 4:  SoilAgent        — NBSS data + user-entered pH → soil health + recommendations
Agent 5:  PestAgent        — NBAIR RSS → district-level risk scoring → threshold alerts
Agent 6:  CropAgent        — DSSAT simulation + KAU/ICAR docs RAG → growth stage + yield prediction
Agent 7:  IrrigationAgent  — Soil moisture + ET₀ + crop stage → irrigation schedule
Agent 8:  FertiliserAgent  — Soil NPK + crop stage + KAU docs → NPK recommendation
Agent 9:  MarketAgent      — data.gov.in APMC → price + trend + SELL/HOLD recommendation
Agent 10: AlertAgent       — Threshold monitoring → FCM push trigger
Agent 11: MemoryAgent      — LangGraph MemorySaver → conversation context per farmer_id
Agent 12: SchedulerAgent   — Generates today's task list from all agent outputs
Agent 13: NDVIAgent        — NASA EarthData → satellite crop health (8-day update)
Agent 14: SupervisorAgent  — Synthesizes all agent outputs → final coherent response (150 words max)

LangGraph State:
class AgriSageState(TypedDict):
    farmer_id:      str
    query_raw:      str           # original, any language
    query_en:       str           # translated to English
    language:       str           # detected: hi/en/ta/ml/te/pa
    location:       dict          # {state, district, lat, lon}
    crops:          list[str]     # farmer's crops
    query_intent:   list[str]     # from IntentAgent
    weather:        dict          # WeatherAgent output
    soil:           dict          # SoilAgent output
    pest_alerts:    list[dict]    # PestAgent output
    crop_stage:     dict          # CropAgent output
    irrigation:     dict          # IrrigationAgent output
    market_data:    dict          # MarketAgent output
    agent_outputs:  Annotated[dict, operator.ior]  # parallel merge
    final_en:       str           # SupervisorAgent English answer
    final_native:   str           # TranslatorAgent native language answer
    fcm_needed:     bool
    error:          str

Graph: START → Translator → Intent → [PARALLEL: Weather|Soil|Pest|Crop|Irrigation|Market|Memory] → Supervisor → Translator(post) → Alert → Scheduler → END
```

---

## 📡 REALTIME DATA SOURCES — ALL FREE

```
1. Open-Meteo       https://api.open-meteo.com/v1/forecast          No key, unlimited
2. NASA EarthData   https://appeears.earthdatacloud.nasa.gov/api/    Free signup
3. data.gov.in      https://api.data.gov.in/resource/<id>            Free key registration
4. IMD              https://mausam.imd.gov.in/imd_latest/contents/   Free RSS
5. NBAIR RSS        https://nbair.res.in/PestAlerts/rassFeed.php     No key, free
6. NBSS India       Static JSON (all India soil zones by state+district) One-time load
7. ICAR/KAU PDFs    Public domain — scrape + embed in pgvector       Free
8. Gemini Flash     https://aistudio.google.com                      15 RPM free tier

INDIA CROPS COVERED (not just Kerala):
North: Wheat, Mustard, Sugarcane, Maize, Potato, Onion
South: Rice, Coconut, Banana, Rubber, Pepper, Cardamom, Cotton
East: Rice, Jute, Tea
West: Cotton, Groundnut, Soybean, Grapes, Pomegranate
Central: Soybean, Pulses, Wheat, Maize
Northeast: Tea, Ginger, Turmeric, Bamboo

SUPPORTED LANGUAGES:
hi = Hindi         (primary — 50%+ of India)
en = English       (educated farmers, officers)
ta = Tamil         (Tamil Nadu)
ml = Malayalam     (Kerala)
te = Telugu        (Andhra/Telangana)
pa = Punjabi       (Punjab/Haryana)
```

---

## 🧩 COMPONENT LIBRARY — COMPLETE SPECS

```kotlin
// Every component listed here with full Compose implementation

// 1. AgriButton — 4 variants
@Composable
fun AgriButton(
    text: String,
    onClick: () -> Unit,
    variant: ButtonVariant = ButtonVariant.Primary,
    enabled: Boolean = true,
    icon: ImageVector? = null,
    modifier: Modifier = Modifier
) // variant: Primary(SageMid bg), Secondary(outlined), Danger(AlertCritical bg), Gold(SoilLaterite bg)
// Height: 52dp, corner: 16dp, full-width by default, icon left of text if provided

// 2. AgriCard
@Composable
fun AgriCard(
    modifier: Modifier = Modifier,
    elevation: Dp = 2.dp,
    borderColor: Color? = null,
    onClick: (() -> Unit)? = null,
    content: @Composable ColumnScope.() -> Unit
) // White bg, 16dp padding, 16dp corner, optional colored left border 3dp

// 3. AlertBanner
@Composable
fun AlertBanner(
    severity: AlertSeverity,  // CRITICAL | WARNING | INFO | SUCCESS
    title: String,
    description: String,
    onDismiss: (() -> Unit)? = null,
    onAction: (() -> Unit)? = null,
    actionLabel: String = "Ask AI →"
)
// Uses AlertCriticalBg/AlertWarningBg/AlertInfoBg/AlertSuccessBg
// Animated slide-in from top for CRITICAL
// Swipe-to-dismiss with SwipeToDismissBox

// 4. StatCard (for weather/soil stats)
@Composable
fun StatCard(
    icon: String,  // emoji
    value: String,
    label: String,
    modifier: Modifier = Modifier
)
// Surface1 bg, centered content, 8dp corner

// 5. BottomNavBar
@Composable
fun AgriBottomNav(
    currentRoute: String,
    onNavigate: (String) -> Unit,
    alertBadgeCount: Int = 0
)
// 5 items: Home, Advisor, Fields, Weather, Profile
// Badge on Alerts item (AlertCritical color bubble with count)
// Selected: SageLeaf icon + SagePale indicator pill
// 64dp height, white bg, top border 0.5dp Surface2

// 6. LanguageChip
@Composable
fun LanguageChip(
    nativeText: String,
    languageCode: String,
    selected: Boolean,
    onClick: () -> Unit
)
// Selected: SageLeaf bg, white text
// Unselected: Surface2 bg, TextSecondary text
// 36dp height, 20dp corner (pill)

// 7. LoadingDots (for advisor "thinking" state)
@Composable
fun LoadingDots()
// 3 circles, 8dp diameter each, 6dp gap
// Staggered scale animation: each dot 0.6→1.0→0.6, 80ms offset between dots
// Duration: 600ms loop

// 8. OfflineBanner
@Composable
fun OfflineBanner(lastSyncTime: String)
// Sticky at top, Surface2 bg, 📴 icon
// "Offline — Showing data from [time]"
// Disappears when connectivity restored

// 9. ProgressBar with label
@Composable
fun AgriProgressBar(
    label: String,
    value: Float,  // 0.0 to 1.0
    color: Color = SageLeaf
)
// Shows label left, percentage right, animated bar below
// Used for Crop Growth, Soil Moisture, Pest Risk

// 10. EmptyState
@Composable
fun EmptyState(
    emoji: String,
    title: String,
    subtitle: String,
    ctaText: String? = null,
    onCta: (() -> Unit)? = null
)
// Centered, emoji 48sp, title H2, subtitle Body, optional CTA button

// 11. ChatBubble (for Advisor screen)
@Composable
fun AiBubble(text: String, timestamp: String, sourceAgents: List<String>, onSpeak: () -> Unit)
@Composable
fun UserBubble(text: String, timestamp: String)

// 12. CropChip (for onboarding + profile)
@Composable
fun CropChip(emoji: String, cropName: String, selected: Boolean, onClick: () -> Unit)
```

---

## 🏗️ MVVM ARCHITECTURE — COMPLETE PATTERN

```
Data Flow:
  Compose Screen
    ↓ observes StateFlow
  ViewModel (+ UseCases)
    ↓ calls
  Repository
    ↓ reads Room cache first → emits → fetches API → updates Room → emits again
  Room DAO (local) + Retrofit (remote)

Offline-first pattern for every repository:
  fun getData(): Flow<Result<T>> = flow {
      // 1. Emit cached data immediately
      val cached = dao.getCached()
      if (cached != null) emit(Result.Success(cached.toDomain()))

      // 2. Fetch fresh from API
      try {
          val fresh = apiService.getData()
          dao.upsert(fresh.toEntity())
          emit(Result.Success(fresh.toDomain()))
      } catch (e: Exception) {
          if (cached == null) emit(Result.Error(e))
          // else: silently keep cached data, show offline banner
      }
  }

Room Entities:
  FarmerProfile(id, name, state, district, lat, lon, farm_size_acres, primary_crop, language, created_at)
  FieldEntity(id, farmer_id, name, crop, variety, area_acres, soil_type, ph, irrigation, lat, lon, status)
  AdvisoryEntity(id, farmer_id, query, response_en, response_native, agents_used, timestamp, is_read)
  AlertEntity(id, type, severity, title, description, source, affected_field_id, timestamp, is_read, is_dismissed)
  WeatherCacheEntity(id, district, state, data_json, fetched_at, expires_at)
  MarketPriceEntity(id, crop, market, district, state, min_price, modal_price, max_price, date, trend)
  ChatMessageEntity(id, farmer_id, role, content, timestamp, language)

DataStore keys:
  ONBOARDING_COMPLETE: Boolean
  SELECTED_LANGUAGE: String
  FARMER_NAME: String
  HOME_STATE: String
  HOME_DISTRICT: String
  FCM_TOKEN: String
  LAST_SYNC: Long
  DEMO_MODE: Boolean
```
---

## 🚀 PHASE 0 — AUDIT & ENVIRONMENT SETUP
### Time budget: 20 minutes | Branch: main | Owner: M1

```
GOAL: Verify the repo is clean, all tools are installed, brain/ folder is complete,
      and the environment is ready before writing any production code.
      This phase has NO code output — only audit and setup.

STEP 1 — TOOL VERIFICATION:
  Run these and confirm all pass:
    python --version          # must be 3.11+
    java --version            # must be 17+
    node --version            # must be 18+
    git --version             # any recent
    docker --version          # any recent (for local DB)

  Android Studio check:
    - KSP plugin installed (NOT kapt)
    - Kotlin plugin 2.0.21
    - Compose preview working

STEP 2 — REPO AUDIT:
  Run:
    find . -type f | grep -v .git | grep -v __pycache__ | grep -v .gradle | grep -v build | sort

  For each existing file score it:
    Completeness: 0-10 (is every function implemented?)
    Correctness:  0-10 (correct versions, correct patterns?)
    Prod-Ready:   0-10 (error handling, logging, no secrets?)
    Status: PROTECTED (all >= 8) | NEEDS_WORK (any < 8) | MISSING

  Print full audit table — do not skip any file.

STEP 3 — BRAIN/ FOLDER CHECK:
  Verify all 6 brain/ files exist and contain real content (not placeholders).
  If any brain/ file is missing or has placeholder content → CREATE IT NOW with full content.

  brain/00_MASTER_RULES.md must contain:
    - All locked versions (from GLOBAL RULES above)
    - Architecture rules: agents in app/agents/, services in app/services/
    - India-wide scope (not Kerala-only)
    - KSP not kapt, pgvector HNSW only, multilingual-e5-large with mandatory prefixes

  brain/01_PRD.md must contain:
    - Problem statement (India scale: 145M farming families, <15% digital advisory)
    - Solution: 6-language AI advisor, <3s response, works on ₹5,000 phones
    - KPIs: 100K users Year 1, <2s API P95, 90%+ offline functionality
    - User personas: Wheat farmer (Punjab), Rice farmer (UP/WB), Cotton farmer (Maharashtra)

  brain/02_ARCHITECTURE.md must contain:
    - ASCII diagram: Android → FastAPI → LangGraph → [14 Agents] → [Data Sources]
    - Component descriptions for every layer

  brain/03_DATA_MODEL.md must contain:
    - All 7 Room entities (exact fields, types, relations)
    - All 6 PostgreSQL backend tables
    - pgvector kau_documents table with HNSW index spec

  brain/04_API_CONTRACT.md must contain:
    - POST /api/v1/advisory
    - GET  /api/v1/weather?state=&district=
    - GET  /api/v1/market?crop=&state=
    - GET  /api/v1/alerts?district=&state=
    - GET  /api/v1/fields/{farmer_id}
    - POST /api/v1/fields
    - GET  /api/v1/health
    - Each with request/response schema

  brain/05_UI_UX_SPEC.md must contain:
    - All color tokens (exact hex values from DESIGN SYSTEM above)
    - Typography scale (sp values)
    - All 8 screen specs (from SCREENS section above)
    - Navigation graph (type-safe routes)

STEP 4 — ENVIRONMENT FILES:
  Create .env.example if missing:
    GEMINI_API_KEY=your_key_here
    DATA_GOV_IN_KEY=your_key_here
    NASA_EARTHDATA_TOKEN=your_token_here
    DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/agrisage
    ENVIRONMENT=development
    SECRET_KEY=generate_with_python_secrets_token_hex_32
    ALLOWED_ORIGINS=*
    FCM_SERVICE_ACCOUNT_JSON=path/to/firebase_service_account.json

  Create android/local.properties.example if missing:
    API_BASE_URL=http://10.0.2.2:8000/
    # Change to Railway URL for production

  Verify .gitignore contains:
    .env, *.env, __pycache__/, *.pyc, .DS_Store
    android/local.properties, android/.gradle/, android/app/build/
    *.bin, *.pt, sentence_transformers_cache/

STEP 5 — GITHUB SETUP:
  Verify these branches exist, create if missing:
    git checkout -b dev/m1-backend  && git push -u origin dev/m1-backend
    git checkout -b dev/m2-android  && git push -u origin dev/m2-android
    git checkout -b dev/m3-agents   && git push -u origin dev/m3-agents
    git checkout -b dev/m4-deploy   && git push -u origin dev/m4-deploy
    git checkout -b dev/m5-tests    && git push -u origin dev/m5-tests
    git checkout main

  Create GitHub labels if missing (use GitHub CLI):
    gh label create "phase-0" --color "#14532d"
    gh label create "phase-1" --color "#166534"
    gh label create "phase-2" --color "#15803d"
    gh label create "phase-3" --color "#16a34a"
    gh label create "phase-4" --color "#22c55e"
    gh label create "phase-5" --color "#4ade80"
    gh label create "phase-6" --color "#86efac"
    gh label create "backend"  --color "#1e293b"
    gh label create "android"  --color "#0e7490"
    gh label create "agents"   --color "#7c3aed"
    gh label create "protected" --color "#64748b"

VALIDATION GATE — Phase 0:
  [ ] python 3.11+ confirmed
  [ ] java 17+ confirmed
  [ ] All 5 git branches exist on remote
  [ ] All 6 brain/ files exist with real content
  [ ] .env.example and android/local.properties.example created
  [ ] .gitignore verified
  [ ] GitHub labels created
  [ ] Audit table printed (all files scored)

GITHUB ISSUE — Phase 0:
  Title: [Phase 0 Complete] Audit + Environment Setup
  Branch: main
  Labels: phase-0
  Assign: @Magnel
  Body:
    ## Audit results
    [paste audit table]
    ## Brain/ files status
    [list each file and whether it was created or already existed]
    ## Environment
    [confirm all tools and versions]
  STOP AND WAIT FOR CONFIRMATION.
```

---

## 🚀 PHASE 1 — ANDROID APP: FOUNDATION
### Time budget: 60 minutes | Branch: dev/m2-android | Owner: M2

```
GOAL: Complete Android project setup with build files, dependency injection,
      design system, navigation graph, and all placeholder screens navigating correctly.
      App must build with zero errors and all 8 screens reachable.

RUN AUDIT FIRST on android/ directory.

STEP 1 — BUILD FILES (check before touching):
  android/gradle/libs.versions.toml — create if missing:
    [versions]
    kotlin = "2.0.21"
    compose-bom = "2024.09.00"
    navigation-compose = "2.8.5"
    room = "2.7.0"
    ksp = "2.0.21-1.0.27"
    hilt = "2.52"
    retrofit = "2.11.0"
    okhttp = "4.12.0"
    coil = "2.7.0"
    datastore = "1.1.1"
    workmanager = "2.10.0"
    moshi = "1.15.1"
    [libraries]
    # ... all libraries mapped to versions

  android/app/build.gradle.kts:
    plugins {
        id("com.android.application")
        id("org.jetbrains.kotlin.android")
        id("com.google.devtools.ksp") version "2.0.21-1.0.27"  ← KSP ONLY
        id("com.google.dagger.hilt.android")
        id("org.jetbrains.kotlin.plugin.serialization")
        id("com.google.gms.google-services")
    }
    android {
        compileSdk = 35
        defaultConfig {
            minSdk = 26
            targetSdk = 35
            val apiUrl = project.findProperty("API_BASE_URL") ?: "http://10.0.2.2:8000/"
            buildConfigField("String", "API_BASE_URL", "\"$apiUrl\"")
        }
        buildFeatures { compose = true; buildConfig = true }
        composeOptions { kotlinCompilerExtensionVersion = "1.5.15" }
    }
    dependencies {
        implementation(platform(libs.compose.bom))
        implementation(libs.compose.ui)
        implementation(libs.compose.material3)
        implementation(libs.compose.ui.tooling.preview)
        implementation(libs.navigation.compose)
        implementation(libs.kotlinx.serialization.json)
        implementation(libs.room.runtime)
        implementation(libs.room.ktx)
        ksp(libs.room.compiler)          ← KSP not kapt
        implementation(libs.hilt.android)
        ksp(libs.hilt.compiler)          ← KSP not kapt
        implementation(libs.hilt.navigation.compose)
        implementation(libs.retrofit)
        implementation(libs.retrofit.moshi)
        implementation(libs.okhttp)
        implementation(libs.okhttp.logging)
        implementation(libs.coil.compose)
        implementation(libs.datastore.preferences)
        implementation(libs.workmanager.ktx)
        implementation(platform(libs.firebase.bom))
        implementation(libs.firebase.messaging)
        implementation(libs.moshi.kotlin)
        debugImplementation(libs.compose.ui.tooling)
    }

STEP 2 — APPLICATION CLASS + DI:
  AgriSageApplication.kt:
    @HiltAndroidApp
    class AgriSageApplication : Application() {
        override fun onCreate() {
            super.onCreate()
            // Schedule WorkManager background sync
            scheduleBackgroundSync(this)
        }
    }

  di/DatabaseModule.kt, di/NetworkModule.kt, di/RepositoryModule.kt
    - NetworkModule: provides Retrofit with BuildConfig.API_BASE_URL
    - DatabaseModule: provides Room database singleton
    - RepositoryModule: binds Repository interfaces to implementations

STEP 3 — DESIGN SYSTEM:
  ui/theme/Color.kt          ← All tokens from DESIGN SYSTEM section above (exact hex)
  ui/theme/Type.kt           ← Nunito + Inter scale
  ui/theme/Shape.kt          ← Border radius scale
  ui/theme/Theme.kt          ← AgriSageTheme { lightColorScheme + darkColorScheme }
  res/font/nunito_black.ttf  ← Download from Google Fonts
  res/font/inter_regular.ttf
  res/font/inter_medium.ttf
  res/font/inter_semibold.ttf

STEP 4 — NAVIGATION GRAPH:
  MainActivity.kt:
    @AndroidEntryPoint
    class MainActivity : ComponentActivity() {
        override fun onCreate(...) {
            setContent {
                AgriSageTheme {
                    val navController = rememberNavController()
                    NavHost(navController, startDestination = Splash) {
                        composable<Splash>     { SplashScreen(navController) }
                        composable<Onboarding> { OnboardingScreen(navController, it.toRoute<Onboarding>().step) }
                        composable<Home>       { HomeScreen(navController) }
                        composable<Advisor>    { AdvisorScreen(navController) }
                        composable<Fields>     { FieldsScreen(navController) }
                        composable<FieldDetail>{ FieldDetailScreen(navController, it.toRoute<FieldDetail>().fieldId) }
                        composable<Weather>    { WeatherScreen(navController) }
                        composable<Alerts>     { AlertsScreen(navController) }
                        composable<Profile>    { ProfileScreen(navController) }
                    }
                }
            }
        }
    }

  navigation/Routes.kt:
    @Serializable object Splash
    @Serializable data class Onboarding(val step: Int = 0)
    @Serializable object Home
    @Serializable object Advisor
    @Serializable object Fields
    @Serializable data class FieldDetail(val fieldId: String)
    @Serializable object Weather
    @Serializable object Alerts
    @Serializable object Profile

STEP 5 — ALL 8 SCREENS (placeholder + full @Preview):
  For EACH screen:
    - Create the file with correct route
    - Add BottomNavBar (shared component, 5 tabs)
    - Add TopBar where spec requires it
    - Add @Preview with showBackground=true, widthDp=360, heightDp=800
    - Use AgriSageTheme wrapper in preview
    - Show "Phase 1 — [Screen Name] placeholder" text in center

  Files to create:
    screens/SplashScreen.kt
    screens/OnboardingScreen.kt
    screens/HomeScreen.kt
    screens/AdvisorScreen.kt
    screens/FieldsScreen.kt
    screens/FieldDetailScreen.kt
    screens/WeatherScreen.kt
    screens/AlertsScreen.kt
    screens/ProfileScreen.kt

STEP 6 — SHARED COMPONENTS (full implementation, not placeholder):
  components/AgriBottomNav.kt      ← Full implementation with 5 tabs + badge
  components/AgriButton.kt         ← All 4 variants (Primary, Secondary, Danger, Gold)
  components/AgriCard.kt           ← With optional left border + elevation
  components/AlertBanner.kt        ← 4 severity levels with correct colors
  components/OfflineBanner.kt      ← "📴 Offline" sticky banner
  components/LoadingDots.kt        ← 3-dot animated loading

  Each component must have its own @Preview.

STEP 7 — DATA LAYER SKELETON:
  local/AgriSageDatabase.kt:
    @Database(entities = [FarmerProfile::class, FieldEntity::class, AdvisoryEntity::class,
                          AlertEntity::class, WeatherCacheEntity::class,
                          MarketPriceEntity::class, ChatMessageEntity::class], version = 1)
    abstract class AgriSageDatabase : RoomDatabase()

  local/entities/*.kt — All 7 entities (exact fields from DATA MODEL section)
  local/dao/*.kt — DAOs for each entity (Flow return types, suspend functions)
  util/DataStoreManager.kt — All DataStore keys from ARCHITECTURE section

VALIDATION GATE — Phase 1:
  [ ] ./gradlew assembleDebug → BUILD SUCCESSFUL (zero errors, zero warnings)
  [ ] All 8 screens navigate without crash (test on emulator or real device)
  [ ] @Preview renders correctly for all screens in Android Studio
  [ ] All @Preview render without error (no missing resource, no crash)
  [ ] BottomNavBar highlights correct tab based on current route
  [ ] Room database initializes without migration error
  [ ] Hilt injection works (no "Hilt not configured" crash)
  [ ] No kapt usage anywhere (search: grep -r "kapt" . → zero results)
  [ ] No SharedPreferences usage (search: grep -r "SharedPreferences" . → zero results)

GITHUB ISSUE — Phase 1:
  Title: [Phase 1 Complete] Android Foundation — Build + Navigation
  Branch: dev/m2-android
  Labels: phase-1, android
  Assign: @Magnel
  Body:
    ## What was built
    [list every file created]
    ## Files PROTECTED (not touched)
    [list any files with score >= 8 that were skipped]
    ## Validation output
    [paste ./gradlew assembleDebug last 10 lines]
    ## How to review
    git checkout dev/m2-android && ./gradlew assembleDebug
  STOP AND WAIT FOR CONFIRMATION.
```

---

## 🚀 PHASE 2 — ANDROID APP: ALL 8 SCREENS FULLY IMPLEMENTED
### Time budget: 120 minutes | Branch: dev/m2-android | Owner: M2

```
GOAL: Every screen fully implemented with real UI (not placeholders).
      All ViewModels connected. All navigation paths working.
      Voice input working on real device.

RUN AUDIT FIRST. Only touch NEEDS_WORK and MISSING files.

STEP 1 — VIEWMODELS (full implementation):
  viewmodel/HomeViewModel.kt:
    @HiltViewModel
    class HomeViewModel @Inject constructor(
        private val weatherRepo: WeatherRepository,
        private val alertRepo: AlertRepository,
        private val farmerRepo: FarmerRepository
    ) : ViewModel() {
        val homeState: StateFlow<HomeUiState> = combine(
            weatherRepo.getCurrentWeather(),
            alertRepo.getActiveAlerts(),
            farmerRepo.getProfile()
        ) { weather, alerts, profile ->
            HomeUiState(weather=weather, alerts=alerts, profile=profile, isLoading=false)
        }.stateIn(viewModelScope, SharingStarted.Lazily, HomeUiState())
    }

    data class HomeUiState(
        val profile: FarmerProfile? = null,
        val weather: WeatherData? = null,
        val alerts: List<AlertItem> = emptyList(),
        val tasks: List<Task> = emptyList(),
        val marketPrices: List<MarketPrice> = emptyList(),
        val isLoading: Boolean = true,
        val isOffline: Boolean = false,
        val error: String? = null
    )

  viewmodel/AdvisorViewModel.kt:
    - chat history: StateFlow<List<ChatMessage>> from Room
    - sendMessage(text: String, language: String): calls API, streams response
    - isLoading: Boolean (shows LoadingDots while waiting)
    - selectedLanguage: StateFlow<String>
    - clearHistory(): clears Room chat messages

  viewmodel/FieldViewModel.kt:
    - fields: StateFlow<List<Field>> from Room
    - addField(field: FieldInput): inserts to Room + POST to API
    - deleteField(fieldId: String)
    - getFieldDetail(fieldId: String): StateFlow<FieldDetail?>

  viewmodel/WeatherViewModel.kt:
    - weatherData: StateFlow<WeatherData?> from Open-Meteo (via Room cache)
    - forecast: StateFlow<List<DayForecast>> (7 days)
    - advisory: StateFlow<String?> (AI-generated farming advice)
    - refresh(): triggers API fetch

  viewmodel/AlertViewModel.kt:
    - alerts: StateFlow<List<AlertItem>> (filtered by selectedFilter)
    - selectedFilter: StateFlow<AlertFilter>
    - markRead(alertId: String)
    - dismiss(alertId: String)
    - unreadCount: StateFlow<Int>

  viewmodel/OnboardingViewModel.kt:
    - selectedLanguage: StateFlow<String>
    - selectedCrops: StateFlow<Set<String>>
    - state: String, district: String, lat: Float, lon: Float
    - saveAndComplete(): saves to DataStore → sets onboarding_complete = true

  viewmodel/ProfileViewModel.kt:
    - profile: StateFlow<FarmerProfile?> from Room
    - updateLanguage(code: String)
    - updateCrops(crops: List<String>)
    - clearCache()
    - toggleDemoMode()

STEP 2 — REPOSITORIES (offline-first, full implementation):
  repository/WeatherRepository.kt:
    - getCurrentWeather(): Flow<Result<WeatherData>>
      pattern: Room cache check (< 6hr old) → if valid emit → if stale fetch Open-Meteo → update Room → emit
    - getForecast(): Flow<Result<List<DayForecast>>>

  repository/AlertRepository.kt:
    - getActiveAlerts(): Flow<List<AlertItem>> from Room
    - syncAlerts(): suspend — fetch NBAIR RSS + IMD via API backend → save to Room
    - markRead(id): suspend
    - dismiss(id): suspend

  repository/AdvisoryRepository.kt:
    - sendQuery(query: AdvisoryRequest): Flow<Result<AdvisoryResponse>>
      → POST to /api/v1/advisory
      → save request + response to Room (ChatMessageEntity)
    - getChatHistory(farmerId: String): Flow<List<ChatMessage>>

  repository/MarketRepository.kt:
    - getPrices(crops: List<String>, state: String): Flow<Result<List<MarketPrice>>>
      → Room cache (24hr TTL) → API → update → emit

STEP 3 — NETWORK LAYER:
  remote/AgriSageApiService.kt (Retrofit interface):
    interface AgriSageApiService {
        @POST("api/v1/advisory")
        suspend fun getAdvisory(@Body request: AdvisoryRequest): AdvisoryResponse

        @GET("api/v1/weather")
        suspend fun getWeather(@Query("state") state: String,
                               @Query("district") district: String): WeatherResponse

        @GET("api/v1/market")
        suspend fun getMarket(@Query("crop") crop: String,
                              @Query("state") state: String): MarketResponse

        @GET("api/v1/alerts")
        suspend fun getAlerts(@Query("district") district: String,
                              @Query("state") state: String): AlertsResponse

        @GET("api/v1/health")
        suspend fun health(): HealthResponse
    }

  remote/dto/  — All request/response DTOs with @Json annotations (Moshi)

STEP 4 — SCREEN IMPLEMENTATIONS (full UI per spec):
  Implement each screen using its full spec from SCREENS section above.
  Each screen: consumes ViewModel StateFlow, handles loading/error/empty states.

  SplashScreen: animated logo, DataStore check, auto-navigate
  OnboardingScreen: 3 steps with DataStore save at each step
  HomeScreen: full dashboard with all widgets (weather, alerts, tasks, market)
  AdvisorScreen: chat UI + voice input + language toggle
  FieldsScreen: list + FAB + AddField bottom sheet
  FieldDetailScreen: full detail with soil/crop/DSSAT section
  WeatherScreen: current + 7-day + advisory banner
  AlertsScreen: filter chips + categorized list + actions
  ProfileScreen: all settings rows with correct actions

STEP 5 — VOICE INPUT:
  util/SpeechRecognitionHelper.kt:
    class SpeechRecognitionHelper(private val context: Context) {
        fun createIntent(languageCode: String): Intent {
            return Intent(RecognizerIntent.ACTION_RECOGNIZE_SPEECH).apply {
                putExtra(RecognizerIntent.EXTRA_LANGUAGE_MODEL,
                         RecognizerIntent.LANGUAGE_MODEL_FREE_FORM)
                putExtra(RecognizerIntent.EXTRA_LANGUAGE, "${languageCode}-IN")
                putExtra(RecognizerIntent.EXTRA_LANGUAGE_PREFERENCE, "${languageCode}-IN")
                putExtra(RecognizerIntent.EXTRA_ONLY_RETURN_LANGUAGE_PREFERENCE, false)
                putExtra(RecognizerIntent.EXTRA_PROMPT, "बोलिए... / Speak...")
                putExtra(RecognizerIntent.EXTRA_MAX_RESULTS, 1)
            }
        }
        fun extractResult(data: Intent?): String? =
            data?.getStringArrayListExtra(RecognizerIntent.EXTRA_RESULTS)?.firstOrNull()
    }
  In AdvisorScreen: use rememberLauncherForActivityResult for speech intent

STEP 6 — BACKGROUND SYNC:
  util/WeatherSyncWorker.kt:
    @HiltWorker
    class WeatherSyncWorker @AssistedInject constructor(
        @Assisted ctx: Context, @Assisted params: WorkerParameters,
        private val weatherRepo: WeatherRepository
    ) : CoroutineWorker(ctx, params) {
        override suspend fun doWork(): Result {
            return try { weatherRepo.syncWeather(); Result.success() }
            catch (e: Exception) { Result.retry() }
        }
    }
  Interval: 6 hours (weather), 1 hour (alerts)
  Schedule in Application.onCreate()

STEP 7 — FCM NOTIFICATIONS:
  util/FcmService.kt:
    @AndroidEntryPoint
    class AgriSageFcmService : FirebaseMessagingService() {
        override fun onMessageReceived(message: RemoteMessage) {
            val severity = message.data["severity"] ?: "INFO"
            val title = message.data["title"] ?: message.notification?.title ?: ""
            val body = message.data["body"] ?: message.notification?.body ?: ""
            showNotification(severity, title, body)
        }
        private fun showNotification(severity: String, title: String, body: String) {
            // Use NotificationCompat.Builder
            // Channel: PEST_ALERTS (high priority), WEATHER (default), GENERAL (low)
            // CRITICAL severity → vibrate + full-screen intent
        }
    }

VALIDATION GATE — Phase 2:
  [ ] All 8 screens show real UI (no "placeholder" text)
  [ ] Home dashboard shows weather data (from cache or API)
  [ ] Advisor screen: type message → "Ask AI" sends to API → response shows in bubble
  [ ] Advisor screen: tap mic → speaks → text appears in input field
  [ ] Fields screen: Add Field → fill form → Save → appears in list
  [ ] Weather screen: shows 7-day forecast (cached or live)
  [ ] Alerts screen: filter chips work, dismiss works
  [ ] Profile screen: change language → app UI updates language immediately
  [ ] Offline: disable WiFi → app shows OfflineBanner + cached data (no crash)
  [ ] Back navigation works from every screen
  [ ] BottomNav badge updates when new alert arrives
  [ ] @Preview renders correctly in Android Studio for all screens
  [ ] No crash in logcat on any screen (test each screen for 30 seconds)

GITHUB ISSUE — Phase 2:
  Title: [Phase 2 Complete] All 8 Android Screens Fully Implemented
  Branch: dev/m2-android
  Labels: phase-2, android
  Assign: @Magnel
  Body:
    ## What was built
    [list every file created/modified]
    ## Key features working
    - [ ] Voice input (tested on real device)
    - [ ] Chat flow end to end
    - [ ] Offline mode verified
    ## Validation
    [paste ./gradlew assembleDebug last 5 lines]
  STOP AND WAIT FOR CONFIRMATION.
```

---

## 🚀 PHASE 3 — BACKEND: FASTAPI + ALL AGENTS
### Time budget: 90 minutes | Branch: dev/m1-backend + dev/m3-agents | Owner: M1 + M3

```
GOAL: FastAPI backend running with all 14 agents, all 8 data sources connected,
      pgvector RAG working, real advisory responses in < 3 seconds.

RUN AUDIT FIRST on backend/ directory.

STEP 1 — FASTAPI FOUNDATION:
  backend/app/main.py:
    from contextlib import asynccontextmanager
    from fastapi import FastAPI
    from prometheus_fastapi_instrumentator import Instrumentator
    import structlog

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup
        await init_db()
        await init_pgvector()
        scheduler.start()
        logger.info("AgriSage backend started")
        yield
        # Shutdown
        scheduler.shutdown()
        await close_db()

    app = FastAPI(title="Agri-SAGE API", version="1.0.0", lifespan=lifespan)
    Instrumentator().instrument(app).expose(app, endpoint="/metrics")
    app.include_router(advisory_router, prefix="/api/v1")
    app.include_router(weather_router, prefix="/api/v1")
    app.include_router(market_router, prefix="/api/v1")
    app.include_router(alerts_router, prefix="/api/v1")
    app.include_router(fields_router, prefix="/api/v1")
    app.include_router(health_router, prefix="/api/v1")

  backend/app/config.py:
    class Settings(BaseSettings):
        gemini_api_key: str
        data_gov_in_key: str
        nasa_earthdata_token: str
        database_url: str
        environment: str = "development"
        secret_key: str
        allowed_origins: str = "*"
        model_config = SettingsConfigDict(env_file=".env")
    settings = Settings()

  backend/app/database.py:
    - Async SQLAlchemy engine
    - pgvector extension init on startup:
      await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
      await conn.execute("""
          CREATE INDEX IF NOT EXISTS kau_hnsw_idx
          ON kau_documents USING hnsw (embedding vector_cosine_ops)
          WITH (m=16, ef_construction=64)
      """)

STEP 2 — ALL 8 DATA SERVICES:
  services/weather_service.py:
    URL: https://api.open-meteo.com/v1/forecast
    Params: latitude, longitude, hourly=[temperature_2m, precipitation, relative_humidity_2m,
            windspeed_10m, uv_index], daily=[temperature_2m_max, precipitation_sum,
            weathercode], forecast_days=7, timezone=Asia/Kolkata
    Cache: PostgreSQL weather_cache (6hr TTL)
    advice_flag: FLOOD_RISK(rain>50mm) | SPRAY_RISK(humidity>85% & rain<2mm) |
                 IRRIGATION_NEEDED(rain<1mm & temp>35) | NORMAL

  services/market_service.py:
    URL: https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070
    Headers: api-key: settings.data_gov_in_key
    Params: filters[state]=<state>&format=json&limit=100
    Schedule: APScheduler CronTrigger(hour=8, minute=0, timezone="Asia/Kolkata")
    Covers: ALL Indian states (not just Kerala)

  services/pest_service.py:
    URL: https://nbair.res.in/PestAlerts/rassFeed.php
    Parse: feedparser
    Schedule: IntervalTrigger(hours=6)
    India crops: wheat, rice, cotton, sugarcane, maize, mustard, groundnut, soybean,
                 onion, potato, tomato, chilli, coconut, banana, rubber, pepper, cardamom

  services/soil_service.py:
    Source: brain/india_soil_data.json (create this — all states + districts)
    States: All 28 states + major districts
    Fields: ph_min, ph_max, texture, organic_carbon, n_status, p_status, k_status,
            suitable_crops, agroclimatic_zone
    Method: get_soil_by_state_district(state, district) -> SoilContext

  services/rag_service.py:
    Model: intfloat/multilingual-e5-large (dim=1024)
    MANDATORY prefix: "passage: [India crop advisory] " for documents
    MANDATORY prefix: "query: " for user queries
    Retrieve: top-5 chunks by cosine similarity from pgvector
    Threshold: similarity >= 0.70
    Sources: ICAR, KAU, TNAU, PAU (Punjab), IARI docs

  services/notification_service.py:
    Firebase Admin SDK (free)
    Topics: district_<district>_<state> (subscribe per farmer)
    Alert types: PEST_CRITICAL, WEATHER_WARNING, CROP_STAGE, IRRIGATION_REMINDER
    Send when: AlertAgent triggers threshold

  services/ndvi_service.py:
    NASA EarthData AppEEARS API
    MODIS NDVI product: MOD13Q1 (250m, 16-day)
    Cache: 16 days (matches product update frequency)

STEP 3 — ALL 14 AGENTS (full implementation):
  Each agent file in backend/app/agents/:
    - Inherits from BaseAgent
    - Implements async def run(state: AgriSageState) -> AgriSageState
    - Has error handling: return state with error field if fails
    - Calls Gemini with call_gemini_safe() (rate-limit handler)
    - Returns ONLY valid JSON in output (no prose from LLM)

  agents/state.py            ← AgriSageState TypedDict (from AGENT SYSTEM section)
  agents/graph.py            ← Full LangGraph graph (topology from AGENT SYSTEM section)
  agents/base_agent.py       ← BaseAgent with call_gemini_safe()
  agents/intent_agent.py     ← Query classification → WEATHER|PEST|SOIL|CROP|IRRIGATION|MARKET|GENERAL
  agents/translator_agent.py ← Language detect + translation (pre and post)
  agents/weather_agent.py    ← Open-Meteo + IMD → forecast + farming advisory
  agents/soil_agent.py       ← soil_service lookup → soil health + recommendations
  agents/pest_agent.py       ← pest_service DB query → district risk score
  agents/crop_agent.py       ← DSSAT subprocess + KAU RAG → growth stage + yield
  agents/irrigation_agent.py ← ET₀ (FAO-56) + soil moisture + crop stage
  agents/fertiliser_agent.py ← soil NPK + crop stage + RAG → NPK schedule
  agents/market_agent.py     ← market_service query → price + SELL/HOLD recommendation
  agents/alert_agent.py      ← threshold check → FCM trigger if critical
  agents/memory_agent.py     ← LangGraph MemorySaver → conversation context per farmer_id
  agents/scheduler_agent.py  ← generates today's task list from all outputs
  agents/ndvi_agent.py       ← NASA NDVI → crop health index for farmer's fields
  agents/supervisor_agent.py ← synthesizes all outputs → 150-word farmer-friendly answer

  call_gemini_safe() in base_agent.py:
    model = "gemini-1.5-flash"  ← EXACT string
    async def call_gemini_safe(self, messages, max_retries=2):
        for attempt in range(max_retries):
            try:
                return await self.llm.ainvoke(messages)
            except Exception as e:
                if "429" in str(e) or "quota" in str(e).lower():
                    await asyncio.sleep(4 * (attempt + 1))
                    continue
                raise
        raise RuntimeError("Gemini rate limit exceeded — retry in 60s")

STEP 4 — API ROUTERS:
  routers/advisory.py:
    @router.post("/advisory")
    async def get_advisory(request: AdvisoryRequest, db=Depends(get_db)):
        initial_state = AgriSageState(farmer_id=request.farmer_id, query_raw=request.query, ...)
        result = await graph.ainvoke(initial_state, config={"configurable": {"thread_id": request.farmer_id}})
        # Save to DB
        return AdvisoryResponse(answer_native=result["final_native"], answer_en=result["final_en"],
                                agents_used=list(result["agent_outputs"].keys()),
                                language=result["language"])

  routers/weather.py — GET /weather?state=&district= → WeatherResponse
  routers/market.py  — GET /market?crop=&state=      → MarketResponse
  routers/alerts.py  — GET /alerts?district=&state=  → AlertsResponse
  routers/fields.py  — GET/POST /fields/{farmer_id}  → FieldsResponse
  routers/health.py  — GET /health                   → {"status": "healthy", "version": "1.0.0"}

STEP 5 — ALEMBIC MIGRATIONS:
  migrations/versions/001_init.py          ← creates all tables
  migrations/versions/002_pgvector.py      ← adds vector extension + kau_documents
  migrations/versions/003_indexes.py       ← all HNSW + btree indexes

STEP 6 — DOCUMENT INGESTION:
  scripts/ingest_docs.py:
    - Download ICAR/KAU/TNAU/PAU PDFs
    - Chunk: 512 tokens, 50-token overlap, tiktoken cl100k_base
    - Embed: "passage: [India crop advisory] " + chunk
    - Store in kau_documents (id, source, crop, state_relevance, chunk_index, content, embedding)
    - Idempotent: skip if (source, chunk_index) already exists

VALIDATION GATE — Phase 3:
  [ ] uvicorn app.main:app --reload starts without error
  [ ] GET /api/v1/health returns {"status": "healthy"}
  [ ] POST /api/v1/advisory with {"query": "my wheat is yellowing", "farmer_id": "test", "state": "Punjab", "district": "Ludhiana"} returns response in < 5 seconds
  [ ] Open-Meteo fetch works for Ludhiana, Punjab coordinates
  [ ] NBAIR RSS parsed and >= 1 alert in DB
  [ ] data.gov.in market fetch returns wheat prices for Punjab
  [ ] pgvector: SELECT from kau_documents returns > 0 rows (after ingest)
  [ ] All 14 agent files exist with complete implementation
  [ ] pytest tests/test_agents.py -v → >= 10 tests passing
  [ ] pytest tests/test_api.py -v → all endpoint tests passing
  [ ] Gemini rate limit handler works (mock 429 → retries correctly)

GITHUB ISSUE — Phase 3:
  Title: [Phase 3 Complete] FastAPI Backend + 14 Agents + All Data Sources
  Branch: dev/m1-backend / dev/m3-agents
  Labels: phase-3, backend, agents
  Assign: @Magnel
  Body:
    ## Files created
    [complete list]
    ## API health
    curl https://localhost:8000/api/v1/health → [paste response]
    ## Advisory test
    [paste POST /advisory request and response]
    ## Agent test results
    [paste pytest -v output]
  STOP AND WAIT FOR CONFIRMATION.
```

---

## 🚀 PHASE 4 — INTEGRATION: ANDROID ↔ BACKEND
### Time budget: 45 minutes | Branch: dev/m2-android | Owner: M2

```
GOAL: Android app fully connected to running backend.
      Real advisories from real agents displaying in Advisor screen.
      Push notifications arriving on real device.

RUN AUDIT FIRST.

STEP 1 — CONNECT ANDROID TO BACKEND:
  Update android/local.properties (do not commit):
    API_BASE_URL=http://10.0.2.2:8000/  (emulator)
    OR
    API_BASE_URL=http://<your-laptop-IP>:8000/  (real device on same WiFi)

  Test connectivity:
    adb shell curl http://10.0.2.2:8000/api/v1/health  (emulator)
    OR verify health endpoint reachable from real device

STEP 2 — ADVISORY FLOW END-TO-END TEST:
  Open Advisor screen on device → type "मेरी फसल पीली हो रही है" (My crop is yellowing)
  → observe: LoadingDots appear → response arrives in chat bubble → source badge shows agents used
  If fails: check Logcat for network error, check backend logs for request received

STEP 3 — FCM INTEGRATION:
  Firebase project: create at console.firebase.google.com (free Spark plan)
  Add google-services.json to android/app/
  Implement token registration on app start:
    FirebaseMessaging.getInstance().token.addOnCompleteListener { task ->
        if (task.isSuccessful) {
            val token = task.result
            // POST token to backend /api/v1/farmer/fcm-token
        }
    }
  Test: send test FCM from Firebase Console → notification appears on device

STEP 4 — CONNECTIVITY HANDLING:
  util/NetworkMonitor.kt:
    class NetworkMonitor(private val context: Context) {
        val isOnline: StateFlow<Boolean> — observe ConnectivityManager
    }
  In each ViewModel: observe isOnline → set isOffline in UI state
  OfflineBanner appears automatically when isOnline = false

STEP 5 — ERROR HANDLING:
  Every API call wrapped in:
    try { ... } catch (e: HttpException) {
        when (e.code()) {
            429 -> emit(Result.Error(RateLimitException()))
            503 -> emit(Result.Error(ServiceUnavailableException()))
            else -> emit(Result.Error(ApiException(e.message())))
        }
    } catch (e: IOException) {
        emit(Result.Error(NetworkException()))
    }
  Every error shown via Snackbar or inline error state (never crash)

VALIDATION GATE — Phase 4:
  [ ] Advisor screen: real query → real AI response (not mock) appears in < 5s
  [ ] WeatherScreen shows real weather for device's GPS location
  [ ] Alerts screen shows at least 1 real pest or weather alert from backend
  [ ] FCM: send test push from Firebase Console → notification appears on device
  [ ] Offline: turn off WiFi → OfflineBanner appears → cached data still shows → turn WiFi on → banner disappears + data refreshes
  [ ] No crash in Logcat for 5 minutes of normal use
  [ ] Memory usage < 150MB in Android Studio profiler
  [ ] API response time < 3s for advisory (measure in Logcat)

GITHUB ISSUE — Phase 4:
  Title: [Phase 4 Complete] Android ↔ Backend Integration
  Branch: dev/m2-android
  Labels: phase-4, android
  Assign: @Magnel
  Body:
    ## Integration test results
    - [ ] Real advisory response received
    - [ ] FCM notification tested
    - [ ] Offline mode verified
    ## Screenshot
    [attach Advisor screen showing real response]
  STOP AND WAIT FOR CONFIRMATION.
```

---

## 🚀 PHASE 5 — DEPLOYMENT
### Time budget: 45 minutes | Branch: dev/m4-deploy | Owner: M1 + M4

```
GOAL: Backend live on Railway at public HTTPS URL.
      Android app BuildConfig pointing to Railway URL.
      GitHub Actions CI/CD running automatically.

STEP 1 — DOCKERFILE (multi-stage, < 500MB):
  FROM python:3.11-slim AS builder
  WORKDIR /build
  COPY requirements.txt .
  RUN pip install --no-cache-dir --user -r requirements.txt

  FROM python:3.11-slim
  WORKDIR /app
  COPY --from=builder /root/.local /root/.local
  COPY . .
  RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
  ENV PATH=/root/.local/bin:$PATH
  ENV PYTHONUNBUFFERED=1
  HEALTHCHECK --interval=30s --timeout=10s --start-period=20s --retries=3 \
    CMD curl -f http://localhost:8000/api/v1/health || exit 1
  EXPOSE 8000
  CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]

STEP 2 — RAILWAY.TOML:
  [build]
    builder = "dockerfile"
    dockerfilePath = "Dockerfile"
  [deploy]
    startCommand = "alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 2"
    healthcheckPath = "/api/v1/health"
    healthcheckTimeout = 30
    restartPolicyType = "on_failure"

STEP 3 — GITHUB ACTIONS:
  .github/workflows/backend-ci.yml:
    name: Backend CI/CD
    on:
      push:
        branches: [dev/m1-backend, dev/m3-agents, main]
    jobs:
      test:
        runs-on: ubuntu-latest
        services:
          postgres: { image: pgvector/pgvector:pg16, ... }
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-python@v5
            with: { python-version: "3.11" }
          - run: pip install -r requirements.txt
          - run: ruff check app/
          - run: pytest tests/ -v --tb=short
            env: { DATABASE_URL: ..., GEMINI_API_KEY: ${{ secrets.GEMINI_API_KEY }} }
      deploy:
        needs: test
        if: github.ref == 'refs/heads/main'
        steps:
          - run: npm install -g @railway/cli
          - run: railway up --detach
            env: { RAILWAY_TOKEN: ${{ secrets.RAILWAY_TOKEN }} }

  .github/workflows/android-ci.yml:
    name: Android CI
    on:
      push:
        branches: [dev/m2-android, main]
    jobs:
      build:
        runs-on: ubuntu-latest
        steps:
          - uses: actions/checkout@v4
          - uses: actions/setup-java@v4
            with: { distribution: temurin, java-version: "17" }
          - run: echo "API_BASE_URL=${{ secrets.RAILWAY_API_URL }}" >> android/local.properties
          - run: cd android && ./gradlew assembleDebug --no-daemon
          - uses: actions/upload-artifact@v4
            with:
              name: agrisage-debug-${{ github.sha }}
              path: android/app/build/outputs/apk/debug/app-debug.apk

STEP 4 — RAILWAY ENVIRONMENT VARIABLES (set in Railway dashboard):
  DATABASE_URL          ← Railway provides this for PostgreSQL plugin
  GEMINI_API_KEY        ← from aistudio.google.com
  DATA_GOV_IN_KEY       ← from data.gov.in
  NASA_EARTHDATA_TOKEN  ← from earthdata.nasa.gov
  SECRET_KEY            ← python -c "import secrets; print(secrets.token_hex(32))"
  ENVIRONMENT           ← production
  ALLOWED_ORIGINS       ← *

STEP 5 — UPDATE ANDROID FOR PRODUCTION:
  After Railway deployment:
  - Update android/local.properties: API_BASE_URL=https://your-app.railway.app/
  - Add RAILWAY_API_URL to GitHub Secrets
  - Trigger android-ci workflow → APK downloads automatically from GitHub Actions

VALIDATION GATE — Phase 5:
  [ ] curl https://your-app.railway.app/api/v1/health → {"status": "healthy"}
  [ ] POST advisory to Railway URL → real response in < 5s
  [ ] Android app APK downloadable from GitHub Actions artifacts
  [ ] GitHub Actions backend-ci: green ✅
  [ ] GitHub Actions android-ci: green ✅
  [ ] No secrets in git history (git log --all -S "GEMINI_API_KEY" → empty)
  [ ] Railway logs show successful startup, no errors

GITHUB ISSUE — Phase 5:
  Title: [Phase 5 Complete] Live on Railway + CI/CD Active
  Branch: main (via PR from dev/m4-deploy)
  Labels: phase-5
  Assign: @Magnel
  Body:
    ## Live URL
    https://your-app.railway.app
    ## CI/CD status
    - Backend CI: [green/red]
    - Android CI: [green/red]
    ## APK
    [link to GitHub Actions artifact]
  STOP AND WAIT FOR CONFIRMATION.
```

---

## 🚀 PHASE 6 — QA, POLISH & DEMO READY
### Time budget: 60 minutes | Branch: dev/m5-tests | Owner: M5

```
GOAL: 90%+ test coverage. Performance targets met. Demo build ready.
      App runs flawlessly for 5-minute HR demo without network or errors.

STEP 1 — FULL TEST SUITE:
  backend tests:
    tests/test_agents.py     ← mock all 14 agents, test state transitions
    tests/test_api.py        ← FastAPI TestClient, all endpoints
    tests/test_services.py   ← mock external APIs, test each service
    tests/test_integration.py← full advisory flow, no mocks

  android tests:
    test/HomeViewModelTest.kt     ← JUnit5, mock repos
    test/AdvisorViewModelTest.kt  ← test chat flow
    test/AlertViewModelTest.kt    ← test filter, dismiss
    androidTest/AdvisorFlowTest.kt← Compose UI test, send query → see response

  Run all:
    cd backend && pytest tests/ -v --cov=app --cov-report=term-missing
    cd android && ./gradlew test && ./gradlew connectedAndroidTest

STEP 2 — PERFORMANCE AUDIT:
  Backend: use Locust to simulate 50 concurrent users
    locust -f locustfile.py --headless --users 50 --spawn-rate 5 --run-time 60s
    Target: P95 advisory response < 3s

  Android: Android Studio profiler
    - Memory: < 150MB heap during normal use
    - Cold start: < 2s (measure with adb shell am start -W)
    - Frame rate: > 60fps on Home and Advisor screens (no jank)

STEP 3 — ACCESSIBILITY AUDIT:
  TalkBack test on every screen:
    [ ] All icons have contentDescription set
    [ ] Reading order is logical (top to bottom, left to right)
    [ ] All buttons have semantic role set
    [ ] Color contrast passes WCAG AA (4.5:1 for body text)
    [ ] Touch targets all >= 48dp (check with Layout Inspector)

  Font scale test (Settings → Accessibility → Font size → 200%):
    [ ] No text clipped on any screen
    [ ] No overflow hiding important content
    [ ] No layout broken at 200% font scale

STEP 4 — MULTILINGUAL AUDIT:
  Test all 6 languages (hi/en/ta/ml/te/pa):
    [ ] Onboarding completes in each language
    [ ] Advisory response returns in selected language
    [ ] UI labels show in correct language
    [ ] Voice input works for Hindi and Malayalam (on real device)
    [ ] RTL layout not needed (all 6 are LTR — confirmed)

STEP 5 — DEMO BUILD PREPARATION:
  Profile screen → enable Demo Mode toggle:
    - Pre-seeds Room DB with:
      FarmerProfile: "Rajan Singh", Punjab, Ludhiana, Wheat+Rice
      2 FieldEntities, 3 cached advisories, 2 active pest alerts
      7-day weather forecast (hardcoded demo data)
    - Advisory responses served from Room cache (no backend call needed)
    - Shows "🎬 Demo Mode" banner at top of every screen

  Demo scenario (5 minutes):
    1. (30s) Open app → Splash → Home → show weather widget + alert banner
    2. (60s) Tap Advisor → type "मेरी गेहूं पीली हो रही है" → see Hindi response with source tags
    3. (45s) Tap mic → speak in Hindi → text appears → send → get response
    4. (45s) Go to Alerts → show CRITICAL pest alert → tap "Ask AI" → advisor opens with context
    5. (45s) Go to Weather → show 7-day forecast → AI advisory banner
    6. (45s) Go to Fields → add a new field via bottom sheet → appears in list
    7. (30s) Go to Profile → change language to English → all UI switches to English instantly

  Demo APK generation:
    ./gradlew assembleRelease
    (requires signing config — create a debug keystore for demo)

STEP 6 — DOCUMENTATION:
  README.md:
    - What is Agri-SAGE (2 paragraphs)
    - Architecture diagram (ASCII)
    - Setup instructions (clone → .env → docker compose up → run Android)
    - Team: Magnel + M2 + M3 + M4 + M5, ASIET Kalady
    - Demo: how to enable demo mode

  API_DOCS.md:
    - All endpoints with curl examples
    - Request/response schemas
    - Rate limits

VALIDATION GATE — Phase 6:
  [ ] pytest tests/ -v --cov → >= 90% coverage, ZERO failures
  [ ] Advisory P95 < 3s (Locust output)
  [ ] APK size < 25MB (check: ls -lh app-release.apk)
  [ ] Cold start < 2s (adb shell am start -W com.agrisage.app/.MainActivity)
  [ ] Memory < 150MB (Android Studio profiler)
  [ ] TalkBack: all screens navigable without visual aids
  [ ] Font scale 200%: no clipping on any screen
  [ ] All 6 languages tested: advisory returns in selected language
  [ ] Demo Mode: 5-minute script runs without any API calls
  [ ] Demo APK installs on Android 9+ (API 28+)
  [ ] README complete: someone else can set up from scratch using it

FINAL GITHUB ACTIONS:
  git tag v1.0.0-demo
  git push origin main --tags

  Create GitHub Release:
    gh release create v1.0.0-demo \
      --title "Agri-SAGE v1.0.0 — Demo Build" \
      --notes "Complete demo build for HR presentation. See DEMO_SCRIPT.md." \
      android/app/build/outputs/apk/release/app-release.apk

GITHUB ISSUE — Phase 6 (FINAL):
  Title: [Phase 6 Complete] QA + Polish + Demo Build v1.0.0 Ready
  Branch: main
  Labels: phase-6, ready-for-demo
  Assign: @Magnel
  Body:
    ## Test results
    pytest coverage: [X]%
    Android tests: [passed/total]
    ## Performance
    Advisory P95: [X]ms
    APK size: [X]MB
    Cold start: [X]ms
    ## Demo
    Release URL: [GitHub Release link]
    APK: attached
    Demo script: see DEMO_SCRIPT.md
  🎉 ALL PHASES COMPLETE. Agri-SAGE v1.0.0 is ready.
```

---

## 📋 GITHUB ISSUE TEMPLATE

```markdown
<!-- Save as .github/ISSUE_TEMPLATE/phase_complete.md -->
---
name: Phase Complete
about: Automatically created by Gemini after phase completion
title: "[Phase N Complete] <title>"
labels: phase-N, ready-for-review
assignees: Magnel
---

## What was built
<!-- List every file created or modified -->

## Files PROTECTED (not touched — already complete)
<!-- List any files scored >= 8 that Gemini correctly skipped -->

## Validation gate results
<!-- Paste actual command output, not summary -->
```bash
# paste here
```

## How to review
```bash
git checkout <branch>
git pull origin <branch>
# test command here
```

## Notes
<!-- Anything unexpected, decisions made, trade-offs -->
```

---

## ✅ MASTER VALIDATION CHECKLIST

```
Run this final check after all 6 phases are complete:

ANDROID:
[ ] ./gradlew assembleDebug → BUILD SUCCESSFUL
[ ] ./gradlew assembleRelease → BUILD SUCCESSFUL
[ ] APK < 25MB
[ ] Installs on Android 9+ (API 28)
[ ] Cold start < 2s
[ ] All 8 screens reachable, no crash
[ ] Offline mode works (cached data shows, OfflineBanner appears)
[ ] Voice input works for Hindi and Malayalam on real device
[ ] All 6 languages switch correctly
[ ] TalkBack fully functional
[ ] Font scale 200% no clipping
[ ] Memory < 150MB
[ ] No kapt anywhere (grep -r "kapt" android/ → 0 results)
[ ] No SharedPreferences (grep -r "SharedPreferences" android/ → 0 results)
[ ] No hardcoded URLs (grep -r "10.0.2.2\|localhost" android/app/src/main/ → 0 results)

BACKEND:
[ ] uvicorn starts without error
[ ] GET /api/v1/health → 200
[ ] POST /api/v1/advisory → response in < 3s P95
[ ] All 14 agent files complete (no stubs, no pass, no TODO)
[ ] All 8 data sources responding (or graceful fallback)
[ ] pgvector HNSW index exists
[ ] Alembic migrations run clean
[ ] pytest 90%+ coverage, 0 failures
[ ] No hardcoded secrets (grep -r "API_KEY\|password\|secret" backend/app/ → 0 results)

DEPLOYMENT:
[ ] Backend live on Railway, health check green
[ ] GitHub Actions backend-ci: green
[ ] GitHub Actions android-ci: green
[ ] APK downloadable from GitHub Actions
[ ] v1.0.0-demo tag on GitHub

DEMO:
[ ] Demo Mode seeds correct data
[ ] 5-minute script runs without network
[ ] DEMO_SCRIPT.md complete
[ ] README setup works from scratch

GITHUB:
[ ] All 6 phase issues created and closed
[ ] All branches exist on remote
[ ] No secrets in any commit (git log --all -S "GEMINI_API_KEY")
[ ] PR template present
[ ] GitHub release v1.0.0-demo published with APK attached
```

---

*Agri-SAGE — Scalable Agricultural Guidance Engine*
*Built by Magnel & team · ASIET Kalady · India*
*Zero-budget · Open-source · Farmer-first · 2026*
*Scope: All India · Languages: Hindi, English, Tamil, Malayalam, Telugu, Punjabi*
