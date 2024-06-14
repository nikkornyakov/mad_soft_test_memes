from sqlalchemy import Integer
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import (
    Mapped,
    declarative_base,
    declared_attr,
    mapped_column,
    sessionmaker,
)

from core.config import app_config


class PreBase:
    """ "Базовый класс для всех моделей в проекте."""

    @declared_attr
    def __tablename__(cls):
        return f'{cls.__name__.lower()}s'

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)


Base = declarative_base(cls=PreBase)
engine = create_async_engine(url=app_config.database.get_db_url())
AsyncSessionLocal = sessionmaker(engine, class_=AsyncSession)


async def get_async_session():
    """Функция для получения асинхронной сессии."""
    async with AsyncSessionLocal() as async_session:
        yield async_session
