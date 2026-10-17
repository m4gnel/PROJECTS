import pytest
import asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.main import app
from app.database import get_db
from app.models.base import Base

TEST_DATABASE_URL = "postgresql+asyncpg://postgres:testpassword@localhost:5432/agrisage_test"


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
async def test_engine():
    engine = create_async_engine(TEST_DATABASE_URL, echo=False)
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception:
        pass
    yield engine
    await engine.dispose()


@pytest.fixture
async def test_db(test_engine):
    AsyncTestSession = async_sessionmaker(test_engine, expire_on_commit=False)
    async with AsyncTestSession() as session:
        yield session
        await session.rollback()


@pytest.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as c:
        yield c
