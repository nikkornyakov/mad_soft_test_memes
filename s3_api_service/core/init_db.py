import contextlib

from fastapi_users.exceptions import UserAlreadyExists

from core.config import app_config
from core.db import get_async_session
from core.user import get_user_db, get_user_manager
from schemas.user import UserCreate

get_async_session_context = contextlib.asynccontextmanager(get_async_session)
get_user_db_context = contextlib.asynccontextmanager(get_user_db)
get_user_manager_context = contextlib.asynccontextmanager(get_user_manager)


async def create_superuser():
    """Функция для создания единственного администратора сервиса."""
    email = app_config.app.superuser_email
    password = app_config.app.superuser_password
    if email is not None and password is not None:
        try:
            async with get_async_session_context() as session:
                async with get_user_db_context(session) as user_db:
                    async with get_user_manager_context(
                        user_db
                    ) as user_manager:
                        await user_manager.create(
                            UserCreate(
                                email=email,
                                password=password,
                                is_superuser=True,
                            )
                        )
        except UserAlreadyExists:
            pass
