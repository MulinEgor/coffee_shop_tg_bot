from contextlib import asynccontextmanager
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncSession,
    async_sessionmaker,
)

from src.core.settings import settings
from src.core.models import Base


engine = create_async_engine(
    settings.database_url
)

AsyncSessionFactory = async_sessionmaker(
    engine,
    class_=AsyncSession
)


async def create_all_tables():
    """
    Создает все таблицы в базе данных.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@asynccontextmanager
async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Асинхронный контекстный менеджер для получения сессии.
    """
    session = AsyncSessionFactory()
    try:
        yield session
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
    