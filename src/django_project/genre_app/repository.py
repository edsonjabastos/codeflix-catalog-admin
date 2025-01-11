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

        return None

    def get_by_id(self, id: UUID) -> Genre:
        try:
            genre_model = GenreModel.objects.get(id=id)
        except GenreModel.DoesNotExist:
            return None
        return Genre(
            id=genre_model.id,
            name=genre_model.name,
            is_active=genre_model.is_active,
            categories={category.id for category in genre_model.categories.all()},
        )

    def delete(self, id: UUID) -> None:
        GenreModel.objects.filter(id=id).delete()

        return None

    def list(self) -> List[Genre]:
        return [
            Genre(
                id=genre_model.id,
                name=genre_model.name,
                is_active=genre_model.is_active,
                categories={category.id for category in genre_model.categories.all()},
            )
            for genre_model in GenreModel.objects.all()
        ]

    def update(self, genre: Genre) -> Genre:
        try:
            genre_model = GenreModel.objects.get(id=genre.id)
        except GenreModel.DoesNotExist:
            return None

        with transaction.atomic():
            GenreModel.objects.filter(id=genre.id).update(
                name=genre.name, is_active=genre.is_active
            )
            genre_model.categories.set(genre.categories)

            return None
