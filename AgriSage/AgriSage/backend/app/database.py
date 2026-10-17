from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from .config import settings

engine = create_async_engine(settings.DATABASE_URL, echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_db():
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


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
