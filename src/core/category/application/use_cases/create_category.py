from dataclasses import dataclass
from uuid import UUID

from core.category.domain.category_repository import CategoryRepository
from core.category.application.use_cases.exceptions import InvalidCategoryData
from core.category.domain.category import Category


@dataclass
class CreateCategoryRequest:
    name: str
    description: str = ""
    is_active: bool = True


@dataclass
class CreateCategoryResponse:
    id: UUID


class CreateCategory:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository: CategoryRepository = repository

    def execute(self, request: CreateCategoryRequest) -> CreateCategoryResponse:
        try:
            category = Category(
                name=request.name,
                description=request.description,
                is_active=request.is_active,
            )
        except ValueError as error:
            raise InvalidCategoryData(error)

        self.repository.save(category)

        category_response = CreateCategoryResponse(id=category.id)
        return category_response
