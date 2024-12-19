from typing import List
from core.category.application.category_repository import CategoryRepository
from core.category.domain.category import Category


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories: List[Category] = None) -> None:
        self.categories: List[Category] = categories or []

    def save(self, category: Category) -> None:
        self.categories.append(category)
