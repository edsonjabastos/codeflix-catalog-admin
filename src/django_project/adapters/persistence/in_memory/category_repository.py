from typing import List
from uuid import UUID

from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository


class InMemoryCategoryRepository(CategoryRepository):
    def __init__(self, categories: List[Category] = None) -> None:
        self.categories: List[Category] = categories or []

    def save(self, category: Category) -> None:
        self.categories.append(category)

    def get_by_id(self, id: UUID) -> Category | None:
        return next(
            (category for category in self.categories if category.id == id), None
        )

    def delete(self, id: UUID) -> None:
        category: Category = self.get_by_id(id=id)
        if category:
            self.categories.remove(category)

    def update(self, category: Category) -> None:
        category_to_be_updated: Category = self.get_by_id(id=category.id)
        if category_to_be_updated:
            category_to_be_updated_index: int = self.categories.index(
                category_to_be_updated
            )
            self.categories[category_to_be_updated_index] = category

    def list(self) -> List[Category]:
        return [category for category in self.categories]

    def exists_by_ids(self, ids: set[UUID]) -> bool:
        if not ids:
            return True
        existing = {category.id for category in self.categories}
        return ids.issubset(existing)

    def find_missing_ids(self, ids: set[UUID]) -> set[UUID]:
        if not ids:
            return set()
        existing = {category.id for category in self.categories}
        return ids - existing


__all__ = ["InMemoryCategoryRepository"]
