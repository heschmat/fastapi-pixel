from __future__ import annotations

from uuid import uuid4

from app.core.exceptions import ValidationError


ALLOWED_IMAGE_TYPES = {
    "image/jpeg": ".jpg",
    "image/png": ".png",
    "image/webp": ".webp",
}

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB


def guess_extension(content_type: str) -> str:
    ext = ALLOWED_IMAGE_TYPES.get(content_type)
    if not ext:
        raise ValidationError("Unsupported image type")
    return ext


def validate_image_upload(
    *,
    data: bytes,
    content_type: str,
) -> None:
    if content_type not in ALLOWED_IMAGE_TYPES:
        raise ValidationError("Unsupported image type")

    if len(data) > MAX_IMAGE_SIZE:
        raise ValidationError("Image too large")


def build_movie_image_object_key(
    *,
    movie_id: int,
    uploaded_by_user_id: int,
    content_type: str,
) -> str:
    ext = guess_extension(content_type)
    return f"movie-images/{uuid4().hex}{ext}"
