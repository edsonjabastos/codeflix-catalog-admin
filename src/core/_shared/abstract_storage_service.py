from abc import ABC, abstractmethod


class AbstractStorageService(ABC):
    @abstractmethod
    def store(
        self,
        file_path: str,
        content: bytes,
        content_type: str,
    ) -> None:
        """Store a file in the storage service.

        Args:
            file_path (str): The path where the file will be stored.
            content (bytes): The content of the file to be stored.
            content_type (str): The MIME type of the file.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """
        raise NotImplementedError("Method not implemented")
