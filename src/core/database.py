# подключение к базе данных
from contextlib import asynccontextmanager

from aiohttp import web
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from src.constants import DB_URL

Base = declarative_base()  # подключение к базе данных


async def init_db(app: web.Application) -> None:
    engine = create_async_engine(DB_URL)  # создали движок
    async with engine.begin() as conn:  # запускаем контекстный менеджер, который
        await conn.run_sync(Base.metadata.create_all)  # создает нашу базу данных


async def close_db(app: web.Application) -> None:
    engine = create_async_engine(DB_URL)
    await engine.dispose()


@asynccontextmanager
async def get_session() -> AsyncSession:  # генератор сессий
    async_engine = create_async_engine(DB_URL)
    async_session = sessionmaker(bind=async_engine, class_=AsyncSession, expire_on_commit=False)

    async with async_session() as session:
        yield session


# engine = create_engine(DB_URL)  # создаем движок (путь)
#
# Session = sessionmaker(bind=engine)
# session = Session()
