from typing import Set
from uuid import UUID
from dataclasses import dataclass, field
from core.genre.application.exceptions import RelatedCategoriesNotFound
from core.category.domain.category_repository import CategoryRepository
from core.genre.domain.genre_repository import GenreRepository


class CreateGenre:
    def __init__(
        self, genre_repository: GenreRepository, category_repository: CategoryRepository
    ) -> None:
        self.genre_repository = genre_repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        name: str
        is_active: bool = True
        categories: Set[UUID] = field(default_factory=set)

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        category_ids = {category.id for category in self.category_repository.list()}
        if not input.categories.issubset(category_ids):
            raise RelatedCategoriesNotFound(
                f"Categories with provided IDs not found: {input.categories - category_ids}"
            )