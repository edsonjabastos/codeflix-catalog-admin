from dataclasses import dataclass
from typing import List, Set
from uuid import UUID
from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository


@dataclass
class GenreOutput:
    id: UUID
    name: str
    is_active: bool
    categories: Set[UUID]


class ListGenre:
    def __init__(self, genre_repository: GenreRepository):
        self.genre_repository = genre_repository

    @dataclass
    class Input: ...

    @dataclass
    class Output:
        data: List[GenreOutput]

    def execute(self, input: Input) -> Output:
        genres: List[Genre] = self.genre_repository.list()
        return self.Output(
            data=[
                GenreOutput(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=genre.categories,
                )
                for genre in genres
            ]
        )
