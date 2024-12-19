from typing import List
from core.category.domain.category import Category


class InMemoryCategoryRepository:
    def __init__(self, categories: List[Category] = None) -> None:
        self.categories: List[Category] = []

    def save(self, category: Category) -> None:
        self.categories.append(category)
