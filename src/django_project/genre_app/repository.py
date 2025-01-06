from typing import List
from uuid import UUID
from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository
from django_project.genre_app.models import Genre as GenreModel

from django.db import transaction


class DjangoORMGenreRepository(GenreRepository):

    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            genre_model = GenreModel.objects.create(
                id=genre.id, name=genre.name, is_active=genre.is_active
            )
            genre_model.categories.set(genre.categories)

    def update(self, genre: Genre) -> Genre:
        raise NotImplementedError

    def list(self) -> List[Genre]:
        raise NotImplementedError

    def get_by_id(self, id: UUID) -> Genre:
        raise NotImplementedError

    def delete(self, id: UUID) -> None:
        raise NotImplementedError
