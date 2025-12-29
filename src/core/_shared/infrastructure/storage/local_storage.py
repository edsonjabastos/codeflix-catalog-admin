from pathlib import Path
from config import TMP_BUCKET
from core._shared.infrastructure.storage.abstract_storage_service import AbstractStorageService


class LocalStorage(AbstractStorageService):
    

    def __init__(self, bucket: str = TMP_BUCKET) -> None:
        self.bucket = Path(bucket)

        if not self.bucket.exists():
            self.bucket.mkdir(parents=True)

    def store(
        self,
        file_path: str,
        content: bytes,
        content_type: str,
    ) -> None:
        """Store a file in the local storage.

        Args:
            file_path (str): The path where the file will be stored.
            content (bytes): The content of the file to be stored.
            content_type (str): The MIME type of the file.
        """
        full_path = self.bucket / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        with open(full_path, "wb") as f:
            f.write(content)
