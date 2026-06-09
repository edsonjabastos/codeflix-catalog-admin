from uuid import uuid4
from core.genre.application.use_cases.delete_genre import (
    DeleteGenre,
)
from core.genre.domain.genre import Genre
from core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository


class TestDeleteGenre:
    def test_delete_genre_from_repository(self) -> None:
        genre_movie: Genre = Genre(name="Movie", is_active=True)
        genre_series: Genre = Genre(name="Series", is_active=True)
        repository: InMemoryGenreRepository = InMemoryGenreRepository(
            genres=[genre_movie, genre_series]
        )

        use_case: DeleteGenre = DeleteGenre(repository=repository)
        input: DeleteGenre.Input = DeleteGenre.Input(id=genre_movie.id)

        assert repository.get_by_id(genre_movie.id) == genre_movie
        assert repository.get_by_id(genre_series.id) == genre_series

        response = use_case.execute(input=input)

        assert repository.get_by_id(genre_movie.id) is None
        assert response is None
        assert repository.list() == [genre_series]
