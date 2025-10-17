"""Test configuration and fixtures."""

import asyncio
import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.main import app
from app.core.config import settings
from app.db.mongodb import get_database


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def client():
    """Create test client."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def test_db():
    """Create test database."""
    client = AsyncIOMotorClient(settings.TEST_DATABASE_URL)
    db = client[settings.MONGODB_DATABASE]
    yield db
    # Clean up
    await client.drop_database(settings.MONGODB_DATABASE)
    client.close()


@pytest.fixture
def override_get_db(test_db):
    """Override database dependency."""
    def _override_get_db():
        return test_db
    
    app.dependency_overrides[get_database] = _override_get_db
    yield
    app.dependency_overrides.clear()
