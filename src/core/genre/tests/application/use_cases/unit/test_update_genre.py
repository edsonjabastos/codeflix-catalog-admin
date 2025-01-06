from uuid import UUID, uuid4
from unittest.mock import create_autospec

import pytest

from core.category.domain.category import Category
from core.category.domain.category_repository import CategoryRepository
from core.genre.application.use_cases.update_genre import UpdateGenre
from core.genre.application.exceptions import (
    GenreNotFound,
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
def action_genre(movie_category: Category) -> Genre:
    return Genre(name="Action", is_active=True, categories={movie_category.id})


@pytest.fixture
def sport_genre(movie_category: Category, documentary_category: Category) -> Genre:
    return Genre(
        name="Sport",
        is_active=True,
        categories={documentary_category.id, movie_category.id},
    )


@pytest.fixture
def sci_fi_genre() -> Genre:
    return Genre(
        name="Sci-fi",
        is_active=True,
    )


@pytest.fixture
def mock_category_repository_with_categories(
    movie_category, documentary_category
) -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = [movie_category, documentary_category]
    return repository


@pytest.fixture
def update_genre_use_case(
    mock_genre_repository: GenreRepository,
    mock_category_repository_with_categories: CategoryRepository,
) -> UpdateGenre:
    return UpdateGenre(
        genre_repository=mock_genre_repository,
        category_repository=mock_category_repository_with_categories,
    )


@pytest.fixture
def mock_empty_category_repository() -> CategoryRepository:
    repository = create_autospec(CategoryRepository)
    repository.list.return_value = []
    return repository


class TestUpdateGenre:

    def test_update_to_a_valid_genre_replacing_category(
        self,
        documentary_category: Category,
        mock_category_repository_with_categories: CategoryRepository,
        action_genre: Genre,  # action_genre has movie_category in its categories
        mock_genre_repository: GenreRepository,
    ) -> None:

        mock_genre_repository.get_by_id.return_value = action_genre

        update_genre_input = UpdateGenre.Input(
            id=action_genre.id,
            name="Action and Adventure",
            is_active=False,
            categories={documentary_category.id},  # change to documentary_category
        )
        update_genre_use_case: UpdateGenre = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )
        update_genre_use_case.execute(input=update_genre_input)

        mock_genre_repository.update.assert_called_once_with(genre=action_genre)
        assert action_genre.name == "Action and Adventure"
        assert action_genre.is_active is False
        assert action_genre.categories == {documentary_category.id}

    def test_update_to_a_valid_genre_adding_category(
        self,
        documentary_category: Category,
        mock_category_repository_with_categories: CategoryRepository,
        sci_fi_genre: Genre,  # sci_fi_genre has no category in its categories
        mock_genre_repository: GenreRepository,
    ) -> None:

        mock_genre_repository.get_by_id.return_value = sci_fi_genre

        update_genre_input = UpdateGenre.Input(
            id=sci_fi_genre.id,
            name="Sci-fi",
            is_active=True,
            categories={documentary_category.id},  # add documentary_category
        )
        update_genre_use_case: UpdateGenre = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )
        update_genre_use_case.execute(input=update_genre_input)

        mock_genre_repository.update.assert_called_once_with(genre=sci_fi_genre)
        assert sci_fi_genre.name == "Sci-fi"
        assert sci_fi_genre.is_active is True
        assert sci_fi_genre.categories == {documentary_category.id}

    def test_update_to_a_valid_genre_removing_category(
        self,
        mock_category_repository_with_categories: CategoryRepository,
        sport_genre: Genre,  # sport_genre has movie_category and documentary_category in its categories
        mock_genre_repository: GenreRepository,
    ) -> None:

        mock_genre_repository.get_by_id.return_value = sport_genre

        update_genre_input: UpdateGenre.Input = UpdateGenre.Input(
            id=sport_genre.id,
            name="Sport",
            is_active=True,
            categories=set(),  # remove all categories
        )
        update_genre_use_case: UpdateGenre = UpdateGenre(
            genre_repository=mock_genre_repository,
            category_repository=mock_category_repository_with_categories,
        )
        update_genre_use_case.execute(input=update_genre_input)

        mock_genre_repository.update.assert_called_once_with(genre=sport_genre)
        assert sport_genre.name == "Sport"
        assert sport_genre.is_active is True
        assert sport_genre.categories == set()

    def test_update_genre_with_invalid_genre(
        self,
        action_genre: Genre,
        mock_genre_repository: GenreRepository,
        update_genre_use_case: UpdateGenre,
    ) -> None:
        mock_genre_repository.get_by_id.return_value = action_genre
        update_genre_input: UpdateGenre.Input = UpdateGenre.Input(
            id=action_genre.id,
            name="",  # invalid name
            is_active=False,
            categories={},
        )

        with pytest.raises(InvalidGenre, match="name cannot be empty"):
            update_genre_use_case.execute(input=update_genre_input)

    def test_update_genre_with_invalid_long_name(
        self,
        action_genre: Genre,
        mock_genre_repository: GenreRepository,
        update_genre_use_case: UpdateGenre,
    ) -> None:
        mock_genre_repository.get_by_id.return_value = action_genre
        update_genre_input: UpdateGenre.Input = UpdateGenre.Input(
            id=action_genre.id,
            name="a" * 256,  # invalid name
            is_active=False,
            categories={},
        )

        with pytest.raises(
            InvalidGenre, match="name cannot be longer than 255 characters"
        ):
            update_genre_use_case.execute(input=update_genre_input)

    def test_update_genre_not_found(
        self,
        mock_genre_repository: GenreRepository,
        update_genre_use_case: UpdateGenre,
    ) -> None:
        mock_genre_repository.get_by_id.return_value = None
        update_genre_input: UpdateGenre.Input = UpdateGenre.Input(
            id=uuid4(),
            name="Action and Adventure",
            is_active=False,
            categories=set(),
        )

        with pytest.raises(
            GenreNotFound,
            match="Not possible to update genre with id .* because it was not found",
        ):
            update_genre_use_case.execute(input=update_genre_input)

    def test_update_genre_with_invalid_related_categories(
        self,
        sci_fi_genre: Genre,
        mock_genre_repository: GenreRepository,
        update_genre_use_case: UpdateGenre,
    ) -> None:
        mock_genre_repository.get_by_id.return_value = sci_fi_genre
        update_genre_input: UpdateGenre.Input = UpdateGenre.Input(
            id=sci_fi_genre.id,
            name="Sci-fi",
            is_active=True,
            categories={uuid4()},  # non-existent category
        )

        with pytest.raises(
            RelatedCategoriesNotFound,
            match="Categories with provided IDs not found: .*",
        ):
            update_genre_use_case.execute(input=update_genre_input)
