from __future__ import annotations

from app.core.logging_utils import get_logger
from app.core.config import settings
from app.core.exceptions import ValidationError
from app.services.storage.base import StorageStrategy
from app.services.storage.minio_storage import MinioStorageStrategy
from app.services.storage.s3_storage import S3StorageStrategy

logger = get_logger(__name__)

def get_storage_strategy() -> StorageStrategy:
    backend = settings.storage_backend.lower()
    logger.info("Using storage backend", extra={"storage_backend": backend})

    if backend == "minio":
        return MinioStorageStrategy()

    if backend == "s3":
        return S3StorageStrategy()

    raise ValidationError(f"Unsupported storage backend: {backend}")
