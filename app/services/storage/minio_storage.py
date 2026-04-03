from __future__ import annotations

from datetime import timedelta
from io import BytesIO

from minio import Minio

from app.core.config import settings
from app.services.storage.base import StorageStrategy


class MinioStorageStrategy(StorageStrategy):
    def __init__(self) -> None:
        self.client = Minio(
            endpoint=settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
        )

        self.public_client = Minio(
            endpoint=settings.minio_public_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=settings.minio_secure,
            region="us-east-1",
        )

        self.bucket_name = settings.minio_bucket

    def ensure_bucket_exists(self) -> None:
        found = self.client.bucket_exists(self.bucket_name)
        if not found:
            self.client.make_bucket(self.bucket_name)

    def upload_bytes(
        self,
        *,
        data: bytes,
        object_key: str,
        content_type: str,
    ) -> None:
        stream = BytesIO(data)
        self.client.put_object(
            bucket_name=self.bucket_name,
            object_name=object_key,
            data=stream,
            length=len(data),
            content_type=content_type,
        )

    def get_download_url(self, object_key: str) -> str:
        return self.public_client.presigned_get_object(
            self.bucket_name,
            object_key,
            expires=timedelta(hours=2),
        )
