from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)
from sqlalchemy.exc import SQLAlchemyError

from app.core.config import settings
from app.core.base import Base

print("DATABASE_URL USED BY APP:", settings.database_url_async)
engine = create_async_engine(
    settings.database_url_async,
    echo=settings.environment == "development",
    pool_pre_ping=True,
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

async def get_db() -> AsyncSession:
    try:
        async with AsyncSessionLocal() as session:
            yield session

    except SQLAlchemyError:
        raise
