from dataclasses import dataclass
from typing import Set
from uuid import UUID

from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository


class UpdateGenre:
    def __init__(
        self, genre_repository: GenreRepository, category_repository: CategoryRepository
    ):
        self.genre_repository = genre_repository
        self.category_repository = category_repository

    @dataclass
    class Input:
        id: UUID
        name: str
        is_active: bool
        categories: Set[UUID]

    def execute(self, input: Input) -> None:
        genre_to_update: Genre = self.genre_repository.get_by_id(id=input.id)

        if genre_to_update is None:
            raise GenreNotFound(
                f"Not possible to update genre with id {input.id} because it was not found"
            )

        current_name: str = genre_to_update.name

        if input.name is not None:
            current_name = input.name

        try:
            genre_to_update.update_name(name=current_name)
        except ValueError as error:
            raise InvalidGenre(str(error))

        if input.is_active is True:
            genre_to_update.activate()

        if input.is_active is False:
            genre_to_update.deactivate()

        registered_category_ids: Set[UUID] = {
            category.id for category in self.category_repository.list()
        }

        if not input.categories.issubset(registered_category_ids):
            missing_categories = input.categories - registered_category_ids
            raise RelatedCategoriesNotFound(
                f"Categories with provided IDs not found: {', '.join(str(missing_category_id) for missing_category_id in missing_categories)}"
            )

        # categories_to_remove = list(genre_to_update.categories - input.categories)
        # for category_id in categories_to_remove:
        #     genre_to_update.remove_category(category_id=category_id)

        genre_to_update.categories.clear()

        for category_id in input.categories:
            genre_to_update.add_category(category_id=category_id)

        self.genre_repository.update(genre=genre_to_update)
