from __future__ import annotations

from abc import ABC, abstractmethod


class StorageStrategy(ABC):
    @abstractmethod
    def ensure_bucket_exists(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def upload_bytes(
        self,
        *,
        data: bytes,
        object_key: str,
        content_type: str,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_download_url(self, object_key: str) -> str:
        raise NotImplementedError
