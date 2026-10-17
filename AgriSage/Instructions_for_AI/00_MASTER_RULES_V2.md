# 00_MASTER_RULES.md — Agri-SAGE AI Agent Rules (v2 — FINAL)
# ⚠️ READ THIS FILE FIRST. EVERY SESSION. NO EXCEPTIONS.

---

## MANDATORY SESSION START (copy-paste this into Cline/Cursor every time)
```
cat brain/00_MASTER_RULES.md
cat brain/05_FOLDER_STRUCTURE.md
cat brain/07_AGENT_CONTRACTS.md
git status
```

---

## Project Identity
- **Name**: Agri-SAGE (Scalable Agricultural Guidance Engine)
- **Purpose**: AI agricultural advisor for Kerala smallholder farmers
- **Interface**: Android mobile app (Kotlin + Jetpack Compose)
- **Backend**: FastAPI on Railway free tier
- **Budget**: ZERO — free tiers and open-source ONLY

---

## THE 10 COMMANDMENTS (violating any = broken build)

1. **NEVER** create a file not listed in `brain/05_FOLDER_STRUCTURE.md`
2. **NEVER** use a package version not listed in `brain/06_PINNED_DEPENDENCIES.md`
3. **NEVER** invent an agent class not defined in `brain/07_AGENT_CONTRACTS.md`
4. **NEVER** invent a screen not in `brain/08_ANDROID_CONTRACTS.md`
5. **NEVER** add a database table not in `brain/09_DATABASE_SCHEMA.md`
6. **NEVER** return a JSON shape different from `brain/10_API_RESPONSE_SHAPES.md`
7. **NEVER** use a color not in the design tokens below
8. **NEVER** delete or rename an existing file without explicit user instruction
9. **NEVER** upgrade a locked version — all versions are context7-verified
10. **NEVER** install a package not in `brain/06_PINNED_DEPENDENCIES.md`

---

## Locked Tech Stack

### Backend (Python)
| Role | Package | EXACT Version |
|------|---------|---------------|
| Web framework | fastapi | 0.115.0 |
| ASGI server | uvicorn[standard] | 0.30.6 |
| ORM | sqlalchemy | 2.0.35 |
| Async DB driver | asyncpg | 0.29.0 |
| Migrations | alembic | 1.13.2 |
| pgvector client | pgvector | 0.3.2 |
| AI graph | langgraph | 1.0.8 |
| Langchain Google | langchain-google-genai | 2.0.4 |
| Langchain core | langchain-core | 0.3.15 |
| Embeddings | sentence-transformers | 3.1.1 |
| HTTP async | httpx | 0.27.2 |
| Validation | pydantic | 2.9.2 |
| Settings | pydantic-settings | 2.5.2 |
| Scheduling | apscheduler | 3.10.4 |
| WebSocket | websockets | 13.1 |
| RSS parsing | feedparser | 6.0.11 |
| PDF parsing | pypdf | 4.3.1 |
| Auth | python-jose[cryptography] | 3.3.0 |
| Password hash | passlib[bcrypt] | 1.7.4 |
| CORS | (built into fastapi) | - |
| Test | pytest | 8.3.3 |
| Async test | pytest-asyncio | 0.24.0 |
| HTTP test | httpx | 0.27.2 |

### Android (Kotlin)
| Role | Package | EXACT Version |
|------|---------|---------------|
| Language | kotlin | 2.0.0 |
| Android Gradle | com.android.application | 8.6.1 |
| Compose BOM | androidx.compose:compose-bom | 2024.10.00 |
| Navigation | androidx.navigation:navigation-compose | 2.8.5 |
| Serialization | org.jetbrains.kotlinx:kotlinx-serialization-json | 1.7.3 |
| Room | androidx.room:room-runtime | 2.7.0 |
| Room KTX | androidx.room:room-ktx | 2.7.0 |
| Room compiler | androidx.room:room-compiler | 2.7.0 (via KSP) |
| Hilt | com.google.dagger:hilt-android | 2.51.1 |
| Hilt compiler | com.google.dagger:hilt-android-compiler | 2.51.1 (via KSP) |
| Hilt Navigation | androidx.hilt:hilt-navigation-compose | 1.2.0 |
| Retrofit | com.squareup.retrofit2:retrofit | 2.11.0 |
| OkHttp | com.squareup.okhttp3:okhttp | 4.12.0 |
| Gson converter | com.squareup.retrofit2:converter-gson | 2.11.0 |
| Coroutines | org.jetbrains.kotlinx:kotlinx-coroutines-android | 1.9.0 |
| Lifecycle | androidx.lifecycle:lifecycle-viewmodel-compose | 2.8.6 |
| WorkManager | androidx.work:work-runtime-ktx | 2.9.1 |
| DataStore | androidx.datastore:datastore-preferences | 1.1.1 |
| Coil | io.coil-kt:coil-compose | 2.7.0 |
| Maps | com.google.maps.android:maps-compose | 6.2.1 |
| FCM | com.google.firebase:firebase-messaging-ktx | 24.0.2 |
| minSdk | - | 26 (Android 8.0) |
| targetSdk | - | 34 |
| compileSdk | - | 34 |

---

## Design Tokens (ONLY these colors)

```kotlin
// Color.kt — EXACT values, do not change
val SageGreen900 = Color(0xFF1B4332)
val SageGreen700 = Color(0xFF2D6A4F)
val SageGreen500 = Color(0xFF40916C)
val SageGreen300 = Color(0xFF52B788)
val SoilBrown    = Color(0xFF7C4D26)
val AlertRed     = Color(0xFFD62828)
val AlertGold    = Color(0xFFF4A261)
val AlertBlue    = Color(0xFF4361EE)
val AlertGreen   = Color(0xFF2DC653)
val Surface      = Color(0xFFFFFFFF)
val SurfaceDim   = Color(0xFFF5F5F5)
val OnSurface    = Color(0xFF1C1B1F)
val OnSurfaceVar = Color(0xFF49454F)
```

## Typography (ONLY these)
```kotlin
// Type.kt — headings: Nunito ExtraBold 900, body: Inter
// Heading1: Nunito, 28sp, weight 900
// Heading2: Nunito, 22sp, weight 800  
// Body: Inter, 16sp, weight 400
// BodyMedium: Inter, 14sp, weight 500
// Label: Inter, 12sp, weight 600
// Code: JetBrains Mono, 13sp, weight 400
```

---

## Branch → Responsibility Map
| Branch | Scope | DO NOT TOUCH |
|--------|-------|--------------|
| dev/m1-backend | backend/ folder only | android/ |
| dev/m2-database | migrations/ and models/ only | agents/, routers/ |
| dev/m3-android | android/ folder only | backend/ |
| dev/m4-integrations | backend/app/pipelines/ only | routers/, agents/ logic |
| dev/m5-tests | tests/ folders only | src files |

---

## FastAPI Lifespan Pattern (MANDATORY — never use @app.on_event)
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await init_db()
    scheduler.start()
    yield
    # shutdown
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)
```

## LangGraph Pattern (MANDATORY — use START/END constants)
```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

workflow = StateGraph(AgriState)
workflow.add_node("weather", weather_node)
workflow.add_edge(START, "weather")
workflow.add_edge("weather", END)
checkpointer = MemorySaver()
graph = workflow.compile(checkpointer=checkpointer)
```

## SQLAlchemy Async Pattern (MANDATORY)
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
```

---

## Commit Pattern (run after EACH phase completes)
```bash
git add backend/   # or android/ — never git add .
git status         # review what is staged
git commit -m "feat(phase-X): [description]"
git push origin dev/mY-branch
```

---

## Free Tier Limits (never exceed)
| Service | Free Limit | Agri-SAGE Usage |
|---------|-----------|-----------------|
| Railway | 500 hrs/month, 512MB RAM | 1 FastAPI service |
| Gemini API | 15 req/min, 1M tokens/day | LLM + embeddings |
| Open-Meteo | unlimited (no key needed) | weather pipeline |
| NASA EarthData | unlimited (registration) | satellite pipeline |
| data.gov.in | unlimited (API key) | market prices |
| NBAIR RSS | unlimited | pest alerts |
| Firebase Spark | 1 FCM/device | push notifications |
| GitHub | unlimited public | CI/CD |
