from __future__ import annotations

import boto3

from app.core.config import settings
from app.services.storage.base import StorageStrategy


class S3StorageStrategy(StorageStrategy):
    def __init__(self) -> None:
        self.client = boto3.client(
            "s3",
            region_name=settings.aws_region,
        )
        self.bucket_name = settings.s3_bucket

    def ensure_bucket_exists(self) -> None:
        # In production, create the bucket with IaC/Terraform/CloudFormation.
        return None

    def upload_bytes(
        self,
        *,
        data: bytes,
        object_key: str,
        content_type: str,
    ) -> None:
        self.client.put_object(
            Bucket=self.bucket_name,
            Key=object_key,
            Body=data,
            ContentType=content_type,
        )

    def get_download_url(self, object_key: str) -> str:
        return self.client.generate_presigned_url(
            "get_object",
            Params={
                "Bucket": self.bucket_name,
                "Key": object_key,
            },
            ExpiresIn=7200,
        )
