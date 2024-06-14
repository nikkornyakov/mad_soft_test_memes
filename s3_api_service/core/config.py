import boto3
from botocore.exceptions import ClientError
from pydantic import BaseModel
from pydantic_settings import BaseSettings as Base
from pydantic_settings import SettingsConfigDict

from core.constants import (
    ENCODING,
    NOT_FOUND_CODE,
    PG_URL,
    PREFIX_APP,
    PREFIX_POSTGRES,
    PREFIX_S3,
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
    users_database_name: str

    def get_db_url(self) -> str:
        """Метод для получения адреса подключения к базе данных."""
        return SQLITE_URL.format(
            driver=self.drivername, db_name=self.users_database_name
        )


class PostgresSettings(BaseSettings, env_prefix=PREFIX_POSTGRES):
    """Класс настроек для создания подключения к базе данных PostgreSQL."""

    drivername: str
    user: str
    password: str
    users_host: str
    port: int
    users_database_name: str

    def get_db_url(self) -> str:
        """Метод для получения адреса подключения к базе данных."""
        return PG_URL.format(
            driver=self.drivername,
            user=self.user,
            password=self.password,
            host=self.users_host,
            port=self.port,
            db_name=self.users_database_name,
        )


class S3Storage(BaseSettings, env_prefix=PREFIX_S3):
    """Класс настроек для подключения к S3-совместимому хранилищу."""

    url: str
    region: str
    access_key: str
    secret_key: str
    bucket_name: str

    def get_client(self) -> boto3.client:
        """Метод для создания сессии для работы с S3-совместимым хранилищем."""
        return boto3.client(
            's3',
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=self.url,
            region_name=self.region,
        )

    def create_bucket_and_or_get_bucket_name(self) -> str:
        """
        Метод для создания бакета и/или получения
        названия бакета в S3-совместимом хранилище.
        """
        client = self.get_client()
        try:
            client.head_bucket(Bucket=self.bucket_name)
        except ClientError as error:
            if error.response['Error']['Code'] == NOT_FOUND_CODE:
                client.create_bucket(
                    Bucket=self.bucket_name, ACL='public-read'
                )
        return self.bucket_name


class AppSettings(BaseSettings, env_prefix=PREFIX_APP):
    """Класс настроек приложения FastAPI."""

    test_mode: bool
    s3_title: str
    s3_description: str
    superuser_email: str
    superuser_password: str
    secret: str


class AppConfig(BaseModel):
    """Класс итоговой конфигурации приложения FastAPI."""

    app: AppSettings
    database: SQLiteSettings | PostgresSettings
    storage_client: S3Storage


def create_app_config() -> AppConfig:
    """Функция для создания итоговой конфигурации приложения FastAPI."""
    return AppConfig(
        app=AppSettings(),
        database=(
            SQLiteSettings() if AppSettings().test_mode else PostgresSettings()
        ),
        storage_client=S3Storage(),
    )


app_config = create_app_config()
