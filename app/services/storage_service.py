from __future__ import annotations

from io import BytesIO
from uuid import uuid4
from datetime import timedelta
from urllib.parse import urlparse, urlunparse

from minio import Minio
from minio.error import S3Error

from app.core.config import settings
from app.core.exceptions import ValidationError


ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


def get_minio_client() -> Minio:
    return Minio(
        endpoint=settings.minio_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
    )


def get_public_minio_client() -> Minio:
    return Minio(
        endpoint=settings.minio_public_endpoint,
        access_key=settings.minio_access_key,
        secret_key=settings.minio_secret_key,
        secure=settings.minio_secure,
        region="us-east-1",
    )


def ensure_bucket_exists() -> None:
    client = get_minio_client()
    bucket = settings.minio_bucket

    found = client.bucket_exists(bucket)
    if not found:
        client.make_bucket(bucket)


def guess_extension(content_type: str) -> str:
    ext = ALLOWED_IMAGE_TYPES.get(content_type)
    if not ext:
        raise ValidationError("Unsupported image type")
    return ext


def build_movie_image_object_key(
    *,
    movie_id: int,
    uploaded_by_user_id: int,
    content_type: str,
) -> str:
    ext = guess_extension(content_type)
    # return f"movies/{movie_id}/users/{uploaded_by_user_id}/{uuid4().hex}{ext}"
    return f"movie-images/{uuid4().hex}{ext}"


def upload_movie_image_bytes(
    *,
    data: bytes,
    object_key: str,
    content_type: str,
) -> None:
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError("Unsupported image type")

    if len(data) > MAX_IMAGE_SIZE:
        raise ValidationError("Image too large")

    client = get_minio_client()

    stream = BytesIO(data)
    client.put_object(
        bucket_name=settings.minio_bucket,
        object_name=object_key,
        data=stream,
        length=len(data),
        content_type=content_type,
    )


def get_presigned_download_url(object_key: str) -> str:
    client = get_public_minio_client()
    return client.presigned_get_object(
        settings.minio_bucket,
        object_key,
        expires=timedelta(hours=2),
    )
