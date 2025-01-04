from unittest.mock import create_autospec
from uuid import uuid4

import pytest
from core.genre.domain.genre_repository import GenreRepository
from core.genre.application.use_cases.delete_genre import (
    DeleteGenre,
)
from core.genre.application.exceptions import GenreNotFound
from core.genre.domain.genre import Genre


class TestDeleteGenre:

    def test_delete_genre_from_repository(self) -> None:
        genre: Genre = Genre(name="Movie", is_active=True)
        mock_repository: GenreRepository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = genre

        use_case: DeleteGenre = DeleteGenre(repository=mock_repository)
        input: DeleteGenre.Input = DeleteGenre.Input(id=genre.id)
        use_case.execute(input=input)

        mock_repository.delete.assert_called_once_with(genre.id)

    def test_delete_genre_not_found(self) -> None:
        mock_repository: GenreRepository = create_autospec(GenreRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteGenre(repository=mock_repository)

        with pytest.raises(
            GenreNotFound,
            match="Not possible to delete genre with id .* because it was not found",
        ):
            input: DeleteGenre.Input = DeleteGenre.Input(id=uuid4())
            use_case.execute(input=input)

        mock_repository.delete.assert_not_called()
        assert mock_repository.delete.called is False
        # assert mock_repository.delete.called is True # false positive
