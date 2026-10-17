from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import init_db
from .routers import auth, farmers, fields, chat, weather, alerts, advisory


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    from .pipelines.knowledge_pipeline import run_knowledge_pipeline
    from .pipelines.scheduler import setup_scheduler
    await run_knowledge_pipeline()
    scheduler = setup_scheduler()
    scheduler.start()
    yield
    scheduler.shutdown()


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
    from datetime import datetime, timezone, timedelta
    tz = timezone(timedelta(hours=5, minutes=30))
    return {
        "status": "ok",
        "version": "1.0.0",
        "timestamp": datetime.now(tz).isoformat(),
    }
