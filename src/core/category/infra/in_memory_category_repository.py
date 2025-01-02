from typing import List
from uuid import UUID
from core.category.application.use_cases.category_repository import CategoryRepository
from core.category.domain.category import Category


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories: List[Category] = None) -> None:
        self.categories: List[Category] = categories or []

    def save(self, category: Category) -> None:
        self.categories.append(category)

        return None

    def get_by_id(self, id: UUID) -> Category | None:

        return next(
            (category for category in self.categories if category.id == id), None
        )

    def delete(self, id: UUID) -> None:
        category: Category = self.get_by_id(id=id)
        if category:
            self.categories.remove(category)

        return None

    def update(self, category: Category) -> None:
        category_to_be_updated: Category = self.get_by_id(id=category.id)
        if category_to_be_updated:
            # self.delete(id=category.id) # alternative way to update
            # self.save(category)
            category_to_be_updated_index: int = self.categories.index(
                category_to_be_updated
            )
            self.categories[category_to_be_updated_index] = category

        return None
