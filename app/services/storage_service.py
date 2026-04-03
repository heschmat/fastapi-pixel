from __future__ import annotations

from app.services.storage.common import (
    build_movie_image_object_key,
    validate_image_upload,
)
from app.services.storage.factory import get_storage_strategy


def ensure_bucket_exists() -> None:
    storage = get_storage_strategy()
    storage.ensure_bucket_exists()


def upload_movie_image_bytes(
    *,
    data: bytes,
    object_key: str,
    content_type: str,
) -> None:
    validate_image_upload(
        data=data,
        content_type=content_type,
    )

    storage = get_storage_strategy()
    storage.upload_bytes(
        data=data,
        object_key=object_key,
        content_type=content_type,
    )


def get_presigned_download_url(object_key: str) -> str:
    storage = get_storage_strategy()
    return storage.get_download_url(object_key)
