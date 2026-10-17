# AGRI-SAGE — MASTER RULES FOR AI CODING AGENT
## READ THIS FIRST. EVERY SESSION.

## 10 RULES NEVER BREAK
1. NEVER hallucinate agricultural facts — only use retrieved knowledge
2. NEVER invent pesticide product names — only use names from CIB&RC data
3. NEVER present simulation output without label "modelled estimate"
4. NEVER recommend treatment when confidence_state is UNCERTAIN/INSUFFICIENT_DATA/CONFLICTING_EVIDENCE
5. NEVER say farmer is eligible for scheme — say "appears to meet listed criteria"
6. NEVER commit to main branch directly — use your dev/mX-branch
7. NEVER use paid API or tool — stack is 100% free
8. NEVER skip Critic Agent safety checks — all 8 must pass
9. NEVER expose raw error details in API response — only {"detail":"Internal server error"}
10. NEVER modify tests to make them pass — fix the implementation

## EXACT VERSIONS (USE THESE)
### Backend Python
fastapi==0.115.0 | uvicorn[standard]==0.34.0 | sqlalchemy[asyncio]==2.0.36
asyncpg==0.30.0 | alembic==1.14.0 | pgvector==0.4.0
pydantic==2.11.0 | pydantic-settings==2.7.0 | httpx==0.28.0
python-jose[cryptography]==3.3.0 | passlib[bcrypt]==1.7.4 | python-multipart==0.0.18
structlog==24.4.0 | sentence-transformers==3.3.0 | onnxruntime==1.20.0
torch==2.5.1 | torchvision==0.20.1 | langgraph==1.0.8
PyMuPDF==1.24.0 | beautifulsoup4==4.12.3 | Pillow==11.0.0
python-magic==0.4.27 | boto3==1.35.0 | firebase-admin==6.6.0
apscheduler==3.10.4 | razorpay==1.4.2
pytest==8.3.0 | pytest-asyncio==0.24.0 | bandit==1.8.0 | pip-audit==2.8.0

### Android Kotlin
kotlin=2.0.21 | ksp=2.0.21-1.0.28 | compose-bom=2024.12.01
navigation-compose=2.8.5 | room=2.7.0 (KSP NOT kapt) | hilt=2.53
camerax=1.4.0 | onnxruntime-android=1.20.0 | work-runtime-ktx=2.10.0
firebase-messaging-ktx=24.1.0 | coil-compose=2.7.0 | retrofit=2.11.0

## CRITICAL API CHANGES
### LangGraph 1.0.8
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
builder.add_edge(START, 'first_node')
builder.compile(checkpointer=MemorySaver())

### FastAPI 0.115.0 — lifespan MANDATORY
@asynccontextmanager
async def lifespan(app): yield
app = FastAPI(lifespan=lifespan)  # NOT on_startup

### sentence-transformers 3.3.0
model.encode(f'query: {text}', normalize_embeddings=True, convert_to_numpy=True)

### pgvector 0.4.0 — HNSW NOT IVFFlat
USING hnsw (embedding vector_cosine_ops) WITH (m=16, ef_construction=64)

### Pillow 11.0.0
Image.Resampling.LANCZOS  # NOT Image.LANCZOS

### Room 2.7.0 — KSP NOT kapt
ksp("androidx.room:room-compiler:2.7.0")

## CONFIDENCE STATES (exactly 7)
CONFIRMED | LIKELY | POSSIBLE | UNCERTAIN | INSUFFICIENT_DATA | CONFLICTING_EVIDENCE | OUT_OF_SCOPE

## TEAM BRANCHES
M1(Lead/Backend): dev/m1-backend | M2(Agents): dev/m2-agents
M3(Android): dev/m3-android | M4(Data): dev/m4-data | M5(QA): dev/m5-tests

## DEMO DEADLINE: OCTOBER 1, 2026 — 50% implementation with working demo
