from typing import Set
from uuid import UUID
from dataclasses import dataclass, field

from core.category.domain.category_repository import CategoryRepository
from core.genre.application.exceptions import InvalidGenre, RelatedCategoriesNotFound
from core.genre.domain.genre import Genre
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
        if input.categories and not self.category_repository.exists_by_ids(
            input.categories
        ):
            missing_categories = self.category_repository.find_missing_ids(
                input.categories
            )
            raise RelatedCategoriesNotFound(
                f"Categories with provided IDs not found: {', '.join(str(category_id) for category_id in missing_categories)}"
            )

        try:
            genre: Genre = Genre(
                name=input.name, is_active=input.is_active, categories=input.categories
            )
        except ValueError as error:
            raise InvalidGenre(str(error))

        self.genre_repository.save(genre)

        return self.Output(id=genre.id)
