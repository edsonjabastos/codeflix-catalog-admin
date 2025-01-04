from unittest.mock import create_autospec

from core.category.domain.category import Category
from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository

from core.genre.application.use_cases.list_genre import (
    GenreOutput,
    ListGenre,
)
from django_project.category_app.test.test_category_api import category_documentary


class TestListGenre:

    def test_when_no_genres_in_repository_then_return_empty_list(self) -> None:
        mock_repository = create_autospec(GenreRepository)
        mock_repository.list.return_value = []

        use_case = ListGenre(genre_repository=mock_repository)
        request = ListGenre.Input()
        response = use_case.execute(request)

        assert response == ListGenre.Output(data=[])

    def test_when_genres_in_repository_then_return_list_of_genres(self) -> None:
        movies_category = Category(
            name="Movies", description="Movies description", is_active=True
        )
        documentary_category = Category(
            name="Documentary", description="Documentary description", is_active=True
        )
        series_category = Category(
            name="Series", description="Series description", is_active=True
        )
        sports_genre = Genre(
            name="Sports", is_active=True, categories={documentary_category.id}
        )
        romance_genre = Genre(
            name="Romance",
            is_active=True,
            categories={movies_category.id, series_category.id},
        )
        special_genre = Genre(
            name="Special",
            is_active=True,
        )
        mock_repository = create_autospec(GenreRepository)
        mock_repository.list.return_value = [sports_genre, romance_genre, special_genre]

        use_case = ListGenre(genre_repository=mock_repository)
        request = ListGenre.Input()
        response = use_case.execute(request)

        assert response == ListGenre.Output(
            data=[
                GenreOutput(
                    id=sports_genre.id,
                    name=sports_genre.name,
                    is_active=sports_genre.is_active,
                    categories={documentary_category.id},
                ),
                GenreOutput(
                    id=romance_genre.id,
                    name=romance_genre.name,
                    is_active=romance_genre.is_active,
                    categories={movies_category.id, series_category.id},
                ),
                GenreOutput(
                    id=special_genre.id,
                    name=special_genre.name,
                    is_active=special_genre.is_active,
                    categories=set(),
                ),
            ]
        )
