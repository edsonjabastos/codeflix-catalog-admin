from uuid import UUID, uuid4

import pytest

from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from core.genre.application.use_cases.create_genre import CreateGenre
from core.genre.application.exceptions import (
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository
from core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def category_repository_with_categories(
    movie_category, documentary_category
) -> CategoryRepository:
    return InMemoryCategoryRepository(categories=[movie_category, documentary_category])


@pytest.fixture
def genre_repository() -> GenreRepository:
    return InMemoryGenreRepository()


class TestCreateGenre:

    def test_create_genre_with_related_categories(
        self,
        movie_category: Category,
        documentary_category: Category,
        category_repository_with_categories: CategoryRepository,
        genre_repository: GenreRepository,
    ) -> None:
        use_case: CreateGenre = CreateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository_with_categories,
        )

        input: CreateGenre.Input = CreateGenre.Input(
            name="Action",
            categories={movie_category.id, documentary_category.id},
        )

        created_genre_output: CreateGenre.Output = use_case.execute(input=input)

        assert isinstance(created_genre_output.id, UUID)
        created_genre: Genre = genre_repository.get_by_id(created_genre_output.id)
        assert created_genre.name == "Action"
        assert created_genre.categories == {movie_category.id, documentary_category.id}
        assert created_genre.is_active is True

    def test_create_genre_with_related_categories_not_found(
        self,
        genre_repository: GenreRepository,
    ) -> None:
        use_case: CreateGenre = CreateGenre(
            genre_repository=genre_repository,
            category_repository=InMemoryCategoryRepository(categories=[]),
        )

        not_registered_category_id = uuid4()
        input: CreateGenre.Input = CreateGenre.Input(
            name="Action", categories={not_registered_category_id}
        )

        with pytest.raises(RelatedCategoriesNotFound):
            use_case.execute(input=input)

    def test_create_genre_with_invalid_data(
        self,
        movie_category: Category,
        category_repository_with_categories: CategoryRepository,
        genre_repository: GenreRepository,
    ) -> None:
        use_case: CreateGenre = CreateGenre(
            genre_repository=genre_repository,
            category_repository=category_repository_with_categories,
        )

        input: CreateGenre.Input = CreateGenre.Input(
            name="",
            categories={movie_category.id},
        )

        with pytest.raises(InvalidGenre):
            use_case.execute(input=input)

    def test_create_genre_without_related_categories(
        self,
        genre_repository: GenreRepository,
    ) -> None:
        use_case: CreateGenre = CreateGenre(
            genre_repository=genre_repository,
            category_repository=InMemoryCategoryRepository(categories=[]),
        )

        input: CreateGenre.Input = CreateGenre.Input(
            name="Action",
            categories=set(),
        )

        created_genre_output: CreateGenre.Output = use_case.execute(input=input)

        assert isinstance(created_genre_output.id, UUID)
        created_genre: Genre = genre_repository.get_by_id(created_genre_output.id)
        assert created_genre.name == "Action"
        assert created_genre.categories == set()
        assert created_genre.is_active is True