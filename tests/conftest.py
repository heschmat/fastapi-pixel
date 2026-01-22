"""
Add a fixture that clears tables before each golden test.
"""
import pytest
import pytest_asyncio
from sqlalchemy import text

from app.core.database import engine


# @pytest.fixture(autouse=True)
# @pytest.fixture()
@pytest_asyncio.fixture
async def clean_db():
    async with engine.begin() as conn:
        await conn.execute(
            text("TRUNCATE users, movies, reviews RESTART IDENTITY CASCADE")
        )
    yield
