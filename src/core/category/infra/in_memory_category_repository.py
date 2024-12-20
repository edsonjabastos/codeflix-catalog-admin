from typing import List
from uuid import UUID
from core.category.application.use_cases.category_repository import CategoryRepository
from core.category.domain.category import Category
from core.category.application.use_cases.exceptions import CategoryNotFound


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories: List[Category] = None) -> None:
        self.categories: List[Category] = categories or []

    def save(self, category: Category) -> None:
        self.categories.append(category)

    def get_by_id(self, id: UUID) -> Category | None:
        for category in self.categories:
            if category.id == id:
                return category

        return None
