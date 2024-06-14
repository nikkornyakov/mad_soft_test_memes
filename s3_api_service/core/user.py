from fastapi import Depends
from fastapi_users import BaseUserManager, FastAPIUsers, IntegerIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import app_config
from core.constants import AUTH_BACKEND_NAME, AUTH_TOKEN_URL, JWT_LIFETIME
from core.db import get_async_session
from models import User


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    """Функция для получения доступа к базе данных через SQLAlchemy."""
    yield SQLAlchemyUserDatabase(session, User)


def get_jwt_strategy() -> JWTStrategy:
    """Функция для получения стратегии хранения токена в виде JWT"""
    return JWTStrategy(
        secret=app_config.app.secret,
        lifetime_seconds=JWT_LIFETIME,
    )


auth_backend = AuthenticationBackend(
    name=AUTH_BACKEND_NAME,
    transport=BearerTransport(tokenUrl=AUTH_TOKEN_URL),
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    """Класс для управления пользователями."""

    pass


async def get_user_manager(user_db=Depends(get_user_db)):
    """Функция для получения класса управления пользователями."""
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](get_user_manager, [auth_backend])

current_user_is_superuser = fastapi_users.current_user(
    active=True, superuser=True
)
