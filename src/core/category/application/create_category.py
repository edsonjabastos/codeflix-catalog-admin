from uuid import UUID

from core.category.domain.category import Category
from core.category.tests.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class InvalidCategoryData(Exception):
    pass


def create_category(
    repository: InMemoryCategoryRepository,
    name: str,
    description: str = "",
    is_active: bool = True,
) -> UUID:
    try:
        category = Category(name=name, description=description, is_active=is_active)
    except ValueError as error:
        raise InvalidCategoryData(error)

    repository.save(category)

    return category.id
