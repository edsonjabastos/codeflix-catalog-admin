from dataclasses import dataclass
from os import name

from core.category.application.use_cases.category_repository import CategoryRepository
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

    def execute(self, request: UpdateCategoryRequest):
        category = self.repository.get_by_id(request.id)

        if category is None:
            raise CategoryNotFound(
                f"Category not found with the given id {request.id} while updating"
            )

        current_name = category.name
        current_description = category.description

        if request.name is not None:
            current_name = request.name

        if request.description is not None:
            current_description = request.description

        if request.is_active is True:
            category.activate()

        if request.is_active is False:
            category.deactivate()

        try:
            category.validate_name()
        except ValueError as e:
            raise ValueError(e)

        category.update_category(
            name=current_name,
            description=current_description,
        )

        self.repository.update(category)
