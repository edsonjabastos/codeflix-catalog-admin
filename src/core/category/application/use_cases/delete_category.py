from dataclasses import dataclass
from uuid import UUID

from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from core.category.application.use_cases.exceptions import CategoryNotFound


@dataclass
class DeleteCategoryRequest:
    id: UUID


class DeleteCategory:
    def __init__(self, repository: InMemoryCategoryRepository) -> None:
        self.repository: InMemoryCategoryRepository = repository

    def execute(self, request: DeleteCategoryRequest) -> None:
        category: Category = self.repository.get_by_id(request.id)

        if category is None:
            raise CategoryNotFound(
                f"Not possible to delete category with id {request.id} because it was not found"
            )

        self.repository.delete(request.id)
