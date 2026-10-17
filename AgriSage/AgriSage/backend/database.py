from typing import AsyncGenerator
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import declarative_base

from backend.config import settings

# Create async database engine
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=(settings.ENVIRONMENT == "development" and settings.LOG_LEVEL == "DEBUG"),
    future=True,
    pool_pre_ping=True,
)

# Create sessionmaker for async database sessions
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Declarative base class for ORM models
Base = declarative_base()


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """FastAPI dependency that yields an async database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_db_connection() -> bool:
    """Utility to verify database connectivity for health checks."""
    try:
        async with AsyncSessionLocal() as session:
            result = await session.execute(text("SELECT 1"))
            return result.scalar() == 1
    except Exception:
        return False


async def init_db():
    """Initializes vector and uuid extensions and verifies HNSW index on startup."""
    async with engine.begin() as conn:
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector;"))
        await conn.execute(text("CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"))
        await conn.execute(text("""
            DO $$ BEGIN
                IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_schema = 'agents' AND table_name = 'kau_documents') THEN
                    CREATE INDEX IF NOT EXISTS idx_kau_hnsw
                    ON agents.kau_documents USING hnsw (embedding vector_cosine_ops)
                    WITH (m = 16, ef_construction = 64);
                END IF;
            END $$;
        """))

