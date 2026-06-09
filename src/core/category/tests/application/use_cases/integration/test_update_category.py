from uuid import uuid4
import pytest
from core.category.application.use_cases.exceptions import CategoryNotFound
from core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestUpdateCategory:

    def test_can_update_category_name_and_description(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()

        repsitory.save(category)

        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(
            id=category.id, name="New Movies", description="New Movie description"
        )
        use_case.execute(update_category_request)

        updated_category = repsitory.get_by_id(category.id)

        assert updated_category.name == "New Movies"
        assert updated_category.description == "New Movie description"
        assert updated_category.is_active is True
        assert updated_category.id == update_category_request.id

    def test_update_category_name(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()

        repsitory.save(category)

        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(
            id=category.id, name="New Movies"
        )
        use_case.execute(update_category_request)

        updated_category = repsitory.get_by_id(category.id)

        assert updated_category.name == "New Movies"
        assert updated_category.description == "Movie description"
        assert updated_category.is_active is True
        assert updated_category.id == update_category_request.id

    def test_update_category_description(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()

        repsitory.save(category)

        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(
            id=category.id, description="New Movie description"
        )
        use_case.execute(update_category_request)

        updated_category = repsitory.get_by_id(category.id)

        assert updated_category.name == "Movie"
        assert updated_category.description == "New Movie description"
        assert updated_category.is_active is True
        assert updated_category.id == update_category_request.id

    def test_can_deactivate_category(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()

        repsitory.save(category)

        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(id=category.id, is_active=False)
        use_case.execute(update_category_request)

        updated_category = repsitory.get_by_id(category.id)

        assert updated_category.name == "Movie"
        assert updated_category.description == "Movie description"
        assert updated_category.is_active is False
        assert updated_category.id == update_category_request.id

    def test_can_activate_category(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=False
        )
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()

        repsitory.save(category)

        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(id=category.id, is_active=True)
        use_case.execute(update_category_request)

        updated_category = repsitory.get_by_id(category.id)

        assert updated_category.name == "Movie"
        assert updated_category.description == "Movie description"
        assert updated_category.is_active is True
        assert updated_category.id == update_category_request.id

    def test_category_not_found(self) -> None:
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()
        not_found_id = uuid4()
        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(id=str(not_found_id))

        with pytest.raises(CategoryNotFound) as e:
            use_case.execute(update_category_request)
        assert (
            str(e.value)
            == f"Category not found with the given id {not_found_id} while updating"
        )

    def test_update_category_name_to_empty(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()

        repsitory.save(category)

        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(id=category.id, name="")

        with pytest.raises(ValueError) as e:
            use_case.execute(update_category_request)
        assert str(e.value) == "name cannot be empty"

    def test_update_category_name_to_long(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()

        repsitory.save(category)

        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(
            id=category.id, name="a" * 256
        )

        with pytest.raises(ValueError) as e:
            use_case.execute(update_category_request)
        assert str(e.value) == "name cannot be longer than 255 characters"

    def test_update_category_name_description_and_is_active(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()

        repsitory.save(category)

        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(
            id=category.id, name="New Movies", description="New Movie description", is_active=False
        )

        use_case.execute(update_category_request)

        updated_category = repsitory.get_by_id(category.id)

        assert updated_category.name == "New Movies"
        assert updated_category.description == "New Movie description"
        assert updated_category.is_active is False
        assert updated_category.id == update_category_request.id
