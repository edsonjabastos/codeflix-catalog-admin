from unittest.mock import create_autospec

from core.category.domain.category import Category
from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository

from core.genre.application.use_cases.list_genre import (
    ListGenre,
)


class TestListGenre:

    def test_when_no_genres_in_repository_then_return_empty_list(self) -> None:
        mock_repository: GenreRepository = create_autospec(GenreRepository)
        mock_repository.list.return_value = []

        use_case: ListGenre = ListGenre(repository=mock_repository)
        request: ListGenre.Input = ListGenre.Input()
        response: ListGenre.Output = use_case.execute(request)

        assert response == ListGenre.ListOutput(
            data=[], meta=ListGenre.OutputMeta(current_page=1, per_page=2, total=0)
        )

    def test_when_genres_in_repository_then_return_list_of_genres(self) -> None:
        movies_category: Category = Category(
            name="Movies", description="Movies description", is_active=True
        )
        documentary_category: Category = Category(
            name="Documentary", description="Documentary description", is_active=True
        )
        series_category: Category = Category(
            name="Series", description="Series description", is_active=True
        )
        sports_genre: Genre = Genre(
            name="Sports", is_active=True, categories={documentary_category.id}
        )
        romance_genre: Genre = Genre(
            name="Romance",
            is_active=True,
            categories={movies_category.id, series_category.id},
        )
        special_genre: Genre = Genre(
            name="Special",
            is_active=True,
        )
        mock_repository: GenreRepository = create_autospec(GenreRepository)
        mock_repository.list.return_value = [sports_genre, romance_genre, special_genre]

        use_case: ListGenre = ListGenre(repository=mock_repository)
        input: ListGenre.Input = ListGenre.Input()
        response: ListGenre.Output = use_case.execute(input)

        assert response == ListGenre.ListOutput(
            data=[
                # ListGenre.Output(
                #     id=sports_genre.id,
                #     name=sports_genre.name,
                #     is_active=sports_genre.is_active,
                #     categories={documentary_category.id},
                # ),
                ListGenre.Output(
                    id=romance_genre.id,
                    name=romance_genre.name,
                    is_active=romance_genre.is_active,
                    categories={movies_category.id, series_category.id},
                ),
                ListGenre.Output(
                    id=special_genre.id,
                    name=special_genre.name,
                    is_active=special_genre.is_active,
                    categories=set(),
                ),
            ],
            meta=ListGenre.OutputMeta(current_page=1, per_page=2, total=3),
        )
