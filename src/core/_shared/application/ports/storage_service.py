from abc import ABC, abstractmethod


class StorageService(ABC):
    @abstractmethod
    def store(
        self,
        file_path: str,
        content: bytes,
        content_type: str,
    ) -> None:
        raise NotImplementedError
