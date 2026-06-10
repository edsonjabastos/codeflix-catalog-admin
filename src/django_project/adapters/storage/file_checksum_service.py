import hashlib
from pathlib import Path

from core._shared.application.ports.checksum_service import ChecksumService


class FileChecksumService(ChecksumService):
    def compute(
        self, file_path: str, base_path: str, algorithm: str = "sha256"
    ) -> str:
        hash_func = hashlib.new(algorithm)
        full_path = str(Path(base_path) / file_path)
        with open(full_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_func.update(chunk)
        return hash_func.hexdigest()
