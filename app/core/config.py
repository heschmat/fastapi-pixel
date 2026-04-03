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

    # storage backend selector
    storage_backend: str = Field("minio", env="STORAGE_BACKEND")

    # ───────────────────────
    # MinIO
    # ───────────────────────
    minio_endpoint: str = Field(..., env="MINIO_ENDPOINT")
    minio_public_endpoint: str = Field(..., env="MINIO_PUBLIC_ENDPOINT")
    minio_access_key: str = Field(..., env="MINIO_ACCESS_KEY")
    minio_secret_key: str = Field(..., env="MINIO_SECRET_KEY")
    minio_bucket: str = Field(..., env="MINIO_BUCKET")
    minio_secure: bool = Field(False, env="MINIO_SECURE")

    # ───────────────────────
    # AWS S3
    # ───────────────────────
    aws_region: str = Field("us-east-1", env="AWS_REGION")
    s3_bucket: str = Field("", env="S3_BUCKET")

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
