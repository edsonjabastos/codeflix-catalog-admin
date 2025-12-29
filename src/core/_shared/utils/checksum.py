import hashlib
from config import TMP_BUCKET
from pathlib import Path

def get_file_checksum(file_path: str, algorithm: str = "sha256") -> str:
    """Calculate the checksum of a file using the specified algorithm."""
    hash_func = hashlib.new(algorithm)
    full_path = str(Path(TMP_BUCKET) / file_path)
    with open(full_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_func.update(chunk)
    return hash_func.hexdigest()