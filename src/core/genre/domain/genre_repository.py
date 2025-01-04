from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from core.genre.domain.genre import Genre


class GenreRepository(ABC):
    @abstractmethod
    def save(self, genre: Genre) -> Genre:
        raise NotImplementedError

    @abstractmethod
    def update(self, genre: Genre) -> Genre:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Genre]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, genre_id: UUID) -> Genre:
        raise NotImplementedError

    @abstractmethod
    def delete(self, genre_id: UUID) -> None:
        raise NotImplementedError
