from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.core.models import Base
from src.core.settings import settings

engine = create_async_engine(settings.database_url)

AsyncSessionFactory = async_sessionmaker(engine, class_=AsyncSession)


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
