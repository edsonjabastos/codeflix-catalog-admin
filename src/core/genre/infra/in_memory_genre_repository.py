from typing import List
from uuid import UUID
from core.genre.domain.genre_repository import GenreRepository
from core.genre.domain.genre import Genre


class InMemoryGenreRepository(GenreRepository):
    def __init__(self, genres: List[Genre] = None) -> None:
        self.genres: List[Genre] = genres or []

    def save(self, genre: Genre) -> None:
        self.genres.append(genre)

        return None

    def get_by_id(self, id: UUID) -> Genre | None:

        return next((genre for genre in self.genres if genre.id == id), None)

    def delete(self, id: UUID) -> None:
        genre: Genre = self.get_by_id(id=id)
        if genre:
            self.genres.remove(genre)

        return None

    def update(self, genre: Genre) -> None:
        genre_to_be_updated: Genre = self.get_by_id(id=genre.id)
        if genre_to_be_updated:
            # self.delete(id=genre.id) # alternative way to update
            # self.save(genre)
            genre_to_be_updated_index: int = self.genres.index(genre_to_be_updated)
            self.genres[genre_to_be_updated_index] = genre

        return None

    def list(self) -> List[Genre]:

        return [genre for genre in self.genres]
