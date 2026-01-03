from urllib.parse import quote_plus

from pydantic import Field, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # ───────────────────────
    # Pydantic config
    # ───────────────────────
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # ───────────────────────
    # Environment
    # ───────────────────────
    environment: str = "development"

    # ───────────────────────
    # Database credentials
    # ───────────────────────
    db_user: str = Field(..., env="DB_USER")
    db_pass: str = Field(..., env="DB_PASS")
    db_name: str = Field(..., env="DB_NAME")
    db_host: str = Field("db", env="DB_HOST")
    db_port: int = Field(5432, env="DB_PORT")

    # ───────────────────────
    # Async database URL (asyncpg)
    # ───────────────────────
    @computed_field
    @property
    def database_url_async(self) -> str:
        password = quote_plus(self.db_pass)
        return (
            f"postgresql+asyncpg://"
            f"{self.db_user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )

    # ───────────────────────
    # Sync database URL (psycopg)
    # ───────────────────────
    @computed_field
    @property
    def database_url_sync(self) -> str:
        password = quote_plus(self.db_pass)
        return (
            f"postgresql+psycopg://"
            f"{self.db_user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
