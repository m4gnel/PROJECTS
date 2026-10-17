import time
from contextlib import asynccontextmanager
from typing import Callable
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
try:
    import structlog
    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.JSONRenderer()
        ]
    )
    logger = structlog.get_logger("agrisage_backend")
except ImportError:
    import logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger("agrisage_backend")

from backend.config import settings
from backend.database import check_db_connection, engine
from backend.api.v1.auth import router as auth_router
from backend.api.v1.farms import router as farms_router
from backend.api.v1.observations import router as observations_router
from backend.api.v1.diagnose import router as diagnose_router
from backend.api.v1.weather import router as weather_router
from backend.api.v1.risk import router as risk_router
from backend.api.v1.schemes import router as schemes_router
from backend.api.v1.markets import router as markets_router
from backend.api.v1.simulate import router as simulate_router
from backend.api.v1.notifications import router as notifications_router
from backend.api.v1.sync import router as sync_router
from backend.api.v1.expert import router as expert_router
from backend.api.v1.subscriptions import router as subscriptions_router
from backend.api.v1.advisory import router as advisory_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """FastAPI 0.115.0 Lifespan Context Manager."""
    logger.info("app_startup", environment=settings.ENVIRONMENT, version=settings.MODEL_VERSION)
    db_connected = await check_db_connection()
    logger.info("db_connection_check", db_connected=db_connected)
    yield
    logger.info("app_shutdown")
    await engine.dispose()


# Create FastAPI App Instance with Lifespan
app = FastAPI(
    title="Agri-SAGE Backend API",
    description="Scalable Agricultural Guidance Engine — API Services",
    version=settings.MODEL_VERSION,
    docs_url="/docs" if settings.ENVIRONMENT == "development" else None,
    redoc_url="/redoc" if settings.ENVIRONMENT == "development" else None,
    lifespan=lifespan,
)

# CORS Middleware Setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Structlog Request Middleware
@app.middleware("http")
async def log_requests_middleware(request: Request, call_next: Callable):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time_ms = round((time.perf_counter() - start_time) * 1000, 2)

    # Sanitize & Log: NEVER log Authorization headers, passwords, or OTP values
    logger.info(
        "http_request",
        method=request.method,
        path=request.url.path,
        status_code=response.status_code,
        process_time_ms=process_time_ms,
        client_ip=request.client.host if request.client else "unknown"
    )
    return response


# Global 500 Exception Handler (Security SEC-004: Never leak internal tracebacks)
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(
        "unhandled_exception",
        path=request.url.path,
        method=request.method,
        error=str(exc)
    )
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal server error"}
    )


# Health Check Endpoint
@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    db_connected = await check_db_connection()
    return {
        "status": "healthy",
        "service": "agrisage-backend",
        "version": getattr(settings, "MODEL_VERSION", "1.0.0"),
        "environment": getattr(settings, "ENVIRONMENT", "development"),
        "db_connected": db_connected,
    }


# Include Routers under /api/v1 prefix
app.include_router(auth_router, prefix="/api/v1")
app.include_router(farms_router, prefix="/api/v1")
app.include_router(observations_router, prefix="/api/v1")
app.include_router(diagnose_router, prefix="/api/v1")
app.include_router(weather_router, prefix="/api/v1")
app.include_router(risk_router, prefix="/api/v1")
app.include_router(schemes_router, prefix="/api/v1")
app.include_router(markets_router, prefix="/api/v1")
app.include_router(simulate_router, prefix="/api/v1")
app.include_router(notifications_router, prefix="/api/v1")
app.include_router(sync_router, prefix="/api/v1")
app.include_router(expert_router, prefix="/api/v1")
app.include_router(subscriptions_router, prefix="/api/v1")
app.include_router(advisory_router, prefix="/api/v1")
