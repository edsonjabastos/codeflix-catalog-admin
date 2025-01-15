from typing import List
from uuid import UUID

from core.category.domain.category_repository import CategoryRepository
from core.category.domain.category import Category

from django_project.category_app.models import Category as CategoryORM


class DjangoORMCategoryRepository(CategoryRepository):
    def __init__(self, category_orm: CategoryORM | None = None):
        self.category_orm: CategoryORM | None = category_orm or CategoryORM

    def save(self, category: Category) -> None:
        category_orm = CategoryModelMapper.to_model(category)
        category_orm.save()
        # self.category_model.objects.create(
        #     id=category.id,
        #     name=category.name,
        #     description=category.description,
        #     is_active=category.is_active,
        # )

    def get_by_id(self, id: UUID) -> Category | None:
        try:
            category = self.category_orm.objects.get(id=id)
            # return Category(
            #     id=category.id,
            #     name=category.name,
            #     description=category.description,
            #     is_active=category.is_active,
            # )
            return CategoryModelMapper.to_entity(category)
        except self.category_orm.DoesNotExist:
            return None

    def delete(self, id: UUID) -> None:
        self.category_orm.objects.filter(id=id).delete()

    def list(self) -> List[Category]:
        return [
            # Category(
            #     id=category.id,
            #     name=category.name,
            #     description=category.description,
            #     is_active=category.is_active,
            # )
            # for category in self.category_model.objects.all()
            CategoryModelMapper.to_entity(category_model)
            for category_model in self.category_orm.objects.all()
        ]

    def update(self, category: Category) -> None:
        self.category_orm.objects.filter(pk=category.id).update(
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )


class CategoryModelMapper:

    @staticmethod
    def to_entity(category: CategoryORM) -> Category:
        return Category(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )

    @staticmethod
    def to_model(category: Category) -> CategoryORM:
        return CategoryORM(
            id=category.id,
            name=category.name,
            description=category.description,
            is_active=category.is_active,
        )
