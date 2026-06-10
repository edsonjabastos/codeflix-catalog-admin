from abc import ABC, abstractmethod


class ChecksumService(ABC):
    @abstractmethod
    def compute(self, file_path: str, base_path: str, algorithm: str = "sha256") -> str:
        raise NotImplementedError
