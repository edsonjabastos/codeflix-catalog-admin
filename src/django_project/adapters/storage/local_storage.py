from pathlib import Path

from core._shared.application.ports.storage_service import StorageService


class LocalStorage(StorageService):
    def __init__(self, bucket: str) -> None:
        self.bucket = Path(bucket)

        if not self.bucket.exists():
            self.bucket.mkdir(parents=True)

    def store(
        self,
        file_path: str,
        content: bytes,
        content_type: str,
    ) -> None:
        full_path = self.bucket / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "wb") as f:
            f.write(content)
