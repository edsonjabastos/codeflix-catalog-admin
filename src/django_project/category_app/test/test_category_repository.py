from uuid import uuid4

from django_project.category_app.models import Category as CategoryModel
from django_project.category_app.models import Category
from django_project.category_app.repository import DjangoORMCategoryRepository

import pytest


@pytest.mark.django_db
class TestSave:

    def test_save_category_in_database(self):
        category = Category(
            name="Movie",
            description="Movie category",
        )
        category_repository = DjangoORMCategoryRepository(category_model=CategoryModel)

        assert CategoryModel.objects.count() == 0
        assert category_repository.list() == []
        category_repository.save(category)
        assert CategoryModel.objects.count() == 1

        category_from_database = CategoryModel.objects.get()
        assert category_from_database.id == category.id
        assert category_from_database.name == category.name
        assert category_from_database.description == category.description
        assert category_from_database.is_active == category.is_active


@pytest.mark.django_db
class TestGetById:

    def test_get_category_by_id(self):
        category = Category(
            name="Movie",
            description="Movie category",
        )
        category_repository = DjangoORMCategoryRepository(category_model=CategoryModel)
        category_repository.save(category)

        category_from_database = category_repository.get_by_id(category.id)

        assert category_from_database.id == category.id
        assert category_from_database.name == category.name
        assert category_from_database.description == category.description
        assert category_from_database.is_active == category.is_active

    def test_get_category_by_id_not_found(self):
        category_repository = DjangoORMCategoryRepository(category_model=CategoryModel)
        category = category_repository.get_by_id(uuid4())

        assert category is None


@pytest.mark.django_db
class TestDelete:

    def test_delete_category(self):
        category = Category(
            name="Movie",
            description="Movie category",
        )
        category_repository = DjangoORMCategoryRepository(category_model=CategoryModel)
        category_repository.save(category)

        assert CategoryModel.objects.count() == 1
        category_repository.delete(category.id)
        assert CategoryModel.objects.count() == 0

    def test_delete_category_not_found(self):
        category_repository = DjangoORMCategoryRepository(category_model=CategoryModel)
        category_repository.delete(uuid4())
        assert CategoryModel.objects.count() == 0


@pytest.mark.django_db
class TestList:

    def test_list_categories(self):
        category_repository = DjangoORMCategoryRepository(category_model=CategoryModel)

        assert category_repository.list() == []

        category1 = Category(
            name="Movie",
            description="Movie category",
        )
        category2 = Category(
            name="Documentary",
            description="Documentary category",
        )
        category_repository.save(category1)
        category_repository.save(category2)

        categories = category_repository.list()
        assert len(categories) == 2

        category1_from_database = categories[0]
        assert category1_from_database.id == category1.id
        assert category1_from_database.name == category1.name
        assert category1_from_database.description == category1.description
        assert category1_from_database.is_active == category1.is_active

        category2_from_database = categories[1]
        assert category2_from_database.id == category2.id
        assert category2_from_database.name == category2.name
        assert category2_from_database.description == category2.description
        assert category2_from_database.is_active == category2.is_active


@pytest.mark.django_db
class TestUpdate:

    def test_update_category(self):
        category = Category(
            name="Movie",
            description="Movie category",
        )
        category_repository = DjangoORMCategoryRepository(category_model=CategoryModel)
        category_repository.save(category)

        new_category = Category(
            id=category.id,
            name="Documentary",
            description="Documentary category",
        )
        category_repository.update(new_category)

        category_from_database = CategoryModel.objects.get()
        assert category_from_database.id == new_category.id
        assert category_from_database.name == new_category.name
        assert category_from_database.description == new_category.description
        assert category_from_database.is_active == new_category.is_active

    def test_update_category_not_found(self):
        category = Category(
            id=uuid4(),
            name="Movie",
            description="Movie category",
        )
        category_repository = DjangoORMCategoryRepository(category_model=CategoryModel)
        category_repository.update(category)

        assert CategoryModel.objects.count() == 0

    def test_update_category_with_invalid_id(self):
        category = Category(
            id=uuid4(),
            name="Movie",
            description="Movie category",
        )
        category_repository = DjangoORMCategoryRepository(category_model=CategoryModel)
        category_repository.save(category)

        new_category = Category(
            id=uuid4(),
            name="Documentary",
            description="Documentary category",
        )
        category_repository.update(new_category)

        category_from_database = CategoryModel.objects.get()
        assert category_from_database.id == category.id
        assert category_from_database.id != new_category.id
        assert category_from_database.name == category.name
        assert category_from_database.description == category.description
        assert category_from_database.is_active == category.is_active

    # def test_update_category_with_invalid_name(self):
    #     category = Category(
    #         name="Movie",
    #         description="Movie category",
    #     )
    #     category_repository = DjangoORMCategoryRepository(category_model=CategoryModel)
    #     category_repository.save(category)

    #     new_category = Category(
    #         id=category.id,
    #         name="",
    #         description="Documentary category",
    #     )
    #     category_repository.update(new_category)

    #     category_from_database = CategoryModel.objects.get()
    #     assert category_from_database.id == category.id
    #     assert category_from_database.name == category.name
    #     assert category_from_database.description == category.description
    #     assert category_from_database.is_active == category.is_active
