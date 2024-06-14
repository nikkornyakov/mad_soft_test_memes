from pydantic import BaseModel
from pydantic_settings import BaseSettings as Base
from pydantic_settings import SettingsConfigDict

from core.constants import (
    ENCODING,
    PG_URL,
    PREFIX_APP,
    PREFIX_POSTGRES,
    PREFIX_SQLITE,
    SQLITE_URL,
)


class BaseSettings(Base):
    """Базовый класс настроек для считывания параметров из .env файла."""

    model_config = SettingsConfigDict(
        extra='ignore', env_file='.env', env_file_encoding=ENCODING
    )


class SQLiteSettings(BaseSettings, env_prefix=PREFIX_SQLITE):
    """Класс настроек для создания подключения к базе данных SQLite."""

    drivername: str
    memes_database_name: str

    def get_db_url(self) -> str:
        """Метод для получения адреса подключения к базе данных."""
        return SQLITE_URL.format(
            driver=self.drivername, db_name=self.memes_database_name
        )


class PostgresSettings(BaseSettings, env_prefix=PREFIX_POSTGRES):
    """Класс настроек для создания подключения к базе данных PostgreSQL."""

    drivername: str
    user: str
    password: str
    memes_host: str
    port: int
    memes_database_name: str

    def get_db_url(self) -> str:
        """Метод для получения адреса подключения к базе данных."""
        return PG_URL.format(
            driver=self.drivername,
            user=self.user,
            password=self.password,
            host=self.memes_host,
            port=self.port,
            db_name=self.memes_database_name,
        )


class AppSettings(BaseSettings, env_prefix=PREFIX_APP):
    """Класс настроек приложения FastAPI."""

    test_mode: bool
    memes_title: str
    memes_description: str
    superuser_email: str
    superuser_password: str
    secret: str
    s3_api_upload_url: str


class AppConfig(BaseModel):
    """Класс итоговой конфигурации приложения FastAPI."""

    app: AppSettings
    database: SQLiteSettings | PostgresSettings


def create_app_config() -> AppConfig:
    """Функция для создания итоговой конфигурации приложения FastAPI."""

    return AppConfig(
        app=AppSettings(),
        database=(
            SQLiteSettings() if AppSettings().test_mode else PostgresSettings()
        ),
    )


app_config = create_app_config()
