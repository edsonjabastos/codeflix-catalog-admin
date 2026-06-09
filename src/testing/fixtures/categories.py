import pytest

from core.category.domain.category import Category
from django_project.adapters.persistence.django.category_repository import (
    DjangoORMCategoryRepository,
)


@pytest.fixture
def category_movie() -> Category:
    return Category(name="Movie", description="Movie description")


@pytest.fixture
def category_documentary() -> Category:
    return Category(name="Documentary", description="Documentary description")


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()
