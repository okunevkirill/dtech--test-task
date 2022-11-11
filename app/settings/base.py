__all__ = [
    "get_settings",
    "Settings",
]

from functools import lru_cache

from dotenv import find_dotenv
from pydantic.env_settings import BaseSettings
from pydantic.types import PositiveInt, SecretStr, StrictStr
from pathlib import Path


class Settings(BaseSettings):
    # app
    APP_PROTOCOL: StrictStr = "http"
    APP_PORT: PositiveInt = 8000
    APP_HOST: StrictStr = "localhost"
    APP_SECRET_KEY: SecretStr
    # tokens
    JWT_ALGORITHM: StrictStr = "HS256"
    JWT_SECRET_KEY: SecretStr
    ACCESS_TOKEN_EXPIRE_MINUTES: PositiveInt = 30
    REFRESH_TOKEN_EXPIRE_MINUTES: PositiveInt = 43200
    # -------------------------------------------------------------------------
    # PostgresSQL
    POSTGRES_HOST: StrictStr
    POSTGRES_PORT: PositiveInt
    POSTGRES_USER: StrictStr
    POSTGRES_PASSWORD: SecretStr
    POSTGRES_DATABASE_NAME: StrictStr
    POSTGRES_DATA_VOLUME: Path

    class Config:
        env_file_encoding = "utf-8"


@lru_cache
def get_settings(env_file: str = ".env") -> Settings:
    """Create settings instance."""
    return Settings(_env_file=find_dotenv(env_file))
