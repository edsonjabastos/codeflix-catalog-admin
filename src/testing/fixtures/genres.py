import pytest

from core.category.domain.category import Category
from core.genre.domain.genre import Genre
from django_project.adapters.persistence.django.genre_repository import (
    DjangoORMGenreRepository,
)


@pytest.fixture
def genre_romance(
    category_movie: Category, category_documentary: Category
) -> Genre:
    return Genre(
        name="Romance",
        is_active=True,
        categories={category_movie.id, category_documentary.id},
    )


@pytest.fixture
def genre_drama() -> Genre:
    return Genre(name="Drama", is_active=True, categories=set())


@pytest.fixture
def genre_action() -> Genre:
    return Genre(name="Action", is_active=True, categories=set())


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()
