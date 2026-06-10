from dataclasses import dataclass
from typing import Set
from uuid import UUID

from core.genre.application.exceptions import GenreNotFound
from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository


class GetGenre:
    def __init__(self, repository: GenreRepository) -> None:
        self.repository: GenreRepository = repository

    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        id: UUID
        name: str
        is_active: bool
        categories: Set[UUID]

    def execute(self, input: Input) -> Output:
        genre: Genre = self.repository.get_by_id(input.id)

        if genre is None:
            raise GenreNotFound(f"Genre with id {input.id} not found")

        return GetGenre.Output(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            categories=genre.categories,
        )
