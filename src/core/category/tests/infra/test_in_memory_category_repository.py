from uuid import uuid4, UUID

import pytest
from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestSaveInMemoryCategoryRepository:

    def test_can_save_category(self) -> None:
        repository = InMemoryCategoryRepository()
        category = Category("Movie")

        repository.save(category)

        assert len(repository.categories) == 1
        assert repository.categories[0] == category

    def test_can_save_multiple_categories(self) -> None:
        repository = InMemoryCategoryRepository()
        category_movie = Category("Movie")
        category_series = Category("Series")

        repository.save(category_movie)
        repository.save(category_series)

        assert len(repository.categories) == 2
        assert repository.categories[0] == category_movie
        assert repository.categories[1] == category_series


class TestGetByIdInMemoryCategoryRepository:

    def test_can_get_category_by_id(self) -> None:
        repository = InMemoryCategoryRepository()
        category = Category("Movie")
        repository.save(category)

        category_found = repository.get_by_id(category.id)

        assert category_found == category

    def test_return_none_when_category_not_found(self) -> None:
        repository = InMemoryCategoryRepository()

        category_found = repository.get_by_id("123e4567-e89b-12d3-a456-426614174000")

        assert category_found is None


class TestDeleteInMemoryCategoryRepository:

    def test_can_delete_category(self) -> None:
        repository = InMemoryCategoryRepository()
        category = Category("Movie")
        repository.save(category)

        repository.delete(category.id)

        assert len(repository.categories) == 0
        assert repository.get_by_id(category.id) is None

    def test_do_nothing_when_category_not_found(self) -> None:
        repository = InMemoryCategoryRepository()
        id: UUID = uuid4()
        
        assert repository.get_by_id(id) is None

        
