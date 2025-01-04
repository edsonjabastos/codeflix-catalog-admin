from dataclasses import dataclass
from uuid import UUID

from core.genre.domain.genre_repository import GenreRepository
from core.genre.domain.genre import Genre
from core.genre.application.exceptions import GenreNotFound


class DeleteGenre:
    def __init__(self, repository: GenreRepository) -> None:
        self.repository: GenreRepository = repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        genre: Genre = self.repository.get_by_id(input.id)

        if genre is None:
            raise GenreNotFound(
                f"Not possible to delete genre with id {input.id} because it was not found"
            )

        self.repository.delete(input.id)
