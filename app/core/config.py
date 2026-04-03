from urllib.parse import quote_plus

from pydantic import computed_field
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
    db_user: str
    db_pass: str
    db_name: str
    db_host: str = "db"
    db_port: int = 5432

    # storage backend selector
    storage_backend: str = "minio"

    # ───────────────────────
    # MinIO
    # ───────────────────────
    minio_endpoint: str
    minio_public_endpoint: str
    minio_access_key: str
    minio_secret_key: str
    minio_bucket: str
    minio_secure: bool = False

    # ───────────────────────
    # AWS S3
    # ───────────────────────
    aws_region: str = "us-east-1"
    s3_bucket: str = ""

    # ───────────────────────
    # JWT
    # ───────────────────────
    SECRET_KEY: str = "CHANGE_ME"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

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
            f"postgresql+psycopg2://"
            f"{self.db_user}:{password}@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()
