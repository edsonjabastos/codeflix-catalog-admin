from typing import List
from uuid import UUID
from core.genre.domain.genre import Genre
from core.genre.domain.genre_repository import GenreRepository
from django_project.genre_app.models import Genre as GenreORM

from django.db import transaction


class DjangoORMGenreRepository(GenreRepository):
    def __init__(self, genre_orm: GenreORM | None = None):
        self.genre_orm: GenreORM | None = genre_orm or GenreORM

    def save(self, genre: Genre) -> None:
        with transaction.atomic():
            # genre_model = GenreORM.objects.create(
            #     id=genre.id, name=genre.name, is_active=genre.is_active
            # )
            # genre_model.categories.set(genre.categories)
            genre_model = GenreModelMapper.to_model(genre)
            genre_model.save()

        return None

    def get_by_id(self, id: UUID) -> Genre:
        try:
            genre_model = self.genre_orm.objects.get(id=id)
        except GenreORM.DoesNotExist:
            return None
        # return Genre(
        #     id=genre_model.id,
        #     name=genre_model.name,
        #     is_active=genre_model.is_active,
        #     categories={category.id for category in genre_model.categories.all()},
        # )
        return GenreModelMapper.to_entity(genre_model)

    def delete(self, id: UUID) -> None:
        self.genre_orm.objects.filter(id=id).delete()

        return None

    def list(self) -> List[Genre]:
        return [
            # Genre(
            #     id=genre_model.id,
            #     name=genre_model.name,
            #     is_active=genre_model.is_active,
            #     categories={category.id for category in genre_model.categories.all()},
            # )
            # for genre_model in GenreORM.objects.all()
            GenreModelMapper.to_entity(genre_model)
            for genre_model in self.genre_orm.objects.all()
        ]

    def update(self, genre: Genre) -> Genre:
        try:
            self.genre_orm.objects.get(id=genre.id)
        except self.genre_orm.DoesNotExist:
            return None

        with transaction.atomic():
            self.genre_orm.objects.filter(id=genre.id).update(
                name=genre.name, is_active=genre.is_active
            )
            self.genre_orm.objects.filter(id=genre.id).first().categories.set(
                genre.categories
            )

        return None


class GenreModelMapper:
    @staticmethod
    def to_entity(genre: GenreORM) -> Genre:
        return Genre(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
            categories={category.id for category in genre.categories.all()},
        )

    @staticmethod
    def to_model(genre: Genre) -> GenreORM:
        genre_model: GenreORM = GenreORM(
            id=genre.id,
            name=genre.name,
            is_active=genre.is_active,
        )
        genre_model.categories.set(genre.categories)

        return genre_model
