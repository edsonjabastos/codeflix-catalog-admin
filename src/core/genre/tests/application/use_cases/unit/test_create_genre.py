from uuid import UUID, uuid4
from unittest.mock import create_autospec

import pytest

from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from core.genre.application.use_cases.create_genre import CreateGenre
from core.genre.application.exceptions import (
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository


@pytest.fixture
def mock_genre_repository() -> GenreRepository:
    return create_autospec(GenreRepository)


@pytest.fixture
def movie_category() -> Category:
    return Category(name="Movie")


@pytest.fixture
def documentary_category() -> Category:
    return Category(name="Documentary")


@pytest.fixture
def mock_category_repository_with_categories(
    movie_category, documentary_category
) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository


class TestCreateGenre:

    def test_create_genre_with_related_categories_not_found(
        self,
        mock_empty_category_repository: CategoryRepository,
        mock_genre_repository: GenreRepository,
    ) -> None:
        use_case = CreateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_empty_category_repository,
        )
        not_registered_category_id = uuid4()
        # input = CreateGenre.Input(
        #     name="Action", categories={not_registered_category_id}
        # )
        with pytest.raises(
            RelatedCategoriesNotFound, match="Categories with provided IDs not found: "
        ) as exc_info:
            use_case.execute(
                CreateGenre.Input(
                    name="Action", categories={not_registered_category_id}
                )
            )

        assert str(not_registered_category_id) in str(exc_info.value)

    def test_create_genre_with_invalid_data(self) -> None: ...

    def test_create_genre_with_valid_data(self) -> None: ...

    def test_create_genre_withouth_categories(self) -> None: ...
