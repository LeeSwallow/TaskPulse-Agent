from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "TaskPulse Agent Backend"
    app_env: str = "local"
    app_version: str = "0.1.0"
    api_prefix: str = "/api"
    grpc_host: str = "127.0.0.1"
    grpc_port: int = 50051
    database_url: str = Field(
        default="postgresql+asyncpg://taskpulse:taskpulse@localhost:5432/taskpulse",
    )
    redis_url: str = "redis://localhost:6379/0"
    pgvector_embedding_dimensions: int = 1536


@lru_cache
def get_settings() -> Settings:
    return Settings()
