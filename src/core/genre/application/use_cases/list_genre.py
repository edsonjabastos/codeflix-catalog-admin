from dataclasses import dataclass, field
from typing import List, Set
from uuid import UUID
from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository


class ListGenre:
    def __init__(self, genre_repository: GenreRepository):
        self.genre_repository = genre_repository

    @dataclass
    class Input:
        order_by: str = "name"
        current_page: int = 1

    @dataclass
    class Output:
        id: UUID
        name: str
        is_active: bool
        categories: Set[UUID]

    @dataclass
    class OutputMeta:
        current_page: int
        per_page: int
        total: int

    @dataclass
    class ListOutput:
        data: List["ListGenre.Output"]
        meta: "ListGenre.OutputMeta" = field(default_factory="ListGenre.ListOutputMeta")

    def execute(self, input: Input) -> Output:
        genres: List[Genre] = self.genre_repository.list()
        sorted_genres: List = sorted(
            [
                self.Output(
                    id=genre.id,
                    name=genre.name,
                    is_active=genre.is_active,
                    categories=genre.categories,
                )
                for genre in genres
            ],
            key=lambda genre: getattr(genre, input.order_by),
        )
        DEFAULT_PAGE_SIZE = 2
        page_offset = (input.current_page - 1) * DEFAULT_PAGE_SIZE
        genres_page = sorted_genres[page_offset : page_offset + DEFAULT_PAGE_SIZE]
        return self.ListOutput(
            data=genres_page,
            meta=ListGenre.OutputMeta(
                current_page=input.current_page,
                per_page=DEFAULT_PAGE_SIZE,
                total=len(sorted_genres),
            ),
        )
