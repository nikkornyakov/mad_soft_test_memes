from contextlib import asynccontextmanager

from fastapi import FastAPI

from api.routers import main_router
from core.config import app_config
from core.init_db import create_superuser


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Функция, которая выполняется во время старта приложения."""
    await create_superuser()
    yield


app = FastAPI(
    title=app_config.app.memes_title,
    description=app_config.app.memes_description,
    lifespan=lifespan,
)
app.include_router(main_router)
