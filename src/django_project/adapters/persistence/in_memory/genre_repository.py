from typing import List
from uuid import UUID

from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository


class InMemoryGenreRepository(GenreRepository):
    def __init__(self, genres: List[Genre] = None) -> None:
        self.genres: List[Genre] = genres or []

    def save(self, genre: Genre) -> None:
        self.genres.append(genre)

    def get_by_id(self, id: UUID) -> Genre | None:
        return next((genre for genre in self.genres if genre.id == id), None)

    def delete(self, id: UUID) -> None:
        genre: Genre = self.get_by_id(id=id)
        if genre:
            self.genres.remove(genre)

    def update(self, genre: Genre) -> None:
        genre_to_be_updated: Genre = self.get_by_id(id=genre.id)
        if genre_to_be_updated:
            genre_to_be_updated_index: int = self.genres.index(genre_to_be_updated)
            self.genres[genre_to_be_updated_index] = genre

    def list(self) -> List[Genre]:
        return [genre for genre in self.genres]

    def exists_by_ids(self, ids: set[UUID]) -> bool:
        if not ids:
            return True
        existing = {genre.id for genre in self.genres}
        return ids.issubset(existing)

    def find_missing_ids(self, ids: set[UUID]) -> set[UUID]:
        if not ids:
            return set()
        existing = {genre.id for genre in self.genres}
        return ids - existing


__all__ = ["InMemoryGenreRepository"]
