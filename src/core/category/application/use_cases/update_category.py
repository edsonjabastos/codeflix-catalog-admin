from dataclasses import dataclass
from os import name

from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from core.category.application.use_cases.exceptions import CategoryNotFound


@dataclass
class UpdateCategoryRequest:
    id: str
    name: str | None = None
    description: str | None = None
    is_active: bool | None = None


class UpdateCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository: CategoryRepository = repository

    def execute(self, input: UpdateCategoryRequest):
        category: Category = self.repository.get_by_id(input.id)

        if category is None:
            raise CategoryNotFound(
                f"Category not found with the given id {input.id} while updating"
            )

        current_name: str = category.name
        current_description: str = category.description

        if input.name is not None:
            current_name = input.name

        if input.description is not None:
            current_description = input.description

        if input.is_active is True:
            category.activate()

        if input.is_active is False:
            category.deactivate()

        try:
            category.validate_name()
        except ValueError as e:
            raise ValueError(e)

        category.update_category(
            name=current_name,
            description=current_description,
        )

        self.repository.update(category=category)
