from dataclasses import dataclass
from uuid import UUID

from core.category.application.use_cases.category_repository import CategoryRepository
from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from core.category.application.use_cases.exceptions import CategoryNotFound


@dataclass
class GetCategoryRequest:
    id: UUID


@dataclass
class GetCategoryResponse:
    id: UUID
    name: str
    description: str
    is_active: bool


class GetCategory:
    def __init__(self, repository: CategoryRepository) -> None:
        self.repository: CategoryRepository = repository

    def execute(self, request: GetCategoryRequest) -> GetCategoryResponse:
        category: Category = self.repository.get_by_id(request.id)

        if category is None:
            raise CategoryNotFound(f"Category with id {request.id} not found")

        return GetCategoryResponse(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
