from unittest.mock import create_autospec
from uuid import uuid4

import pytest
from core.category.domain.category_repository import CategoryRepository
from core.category.application.use_cases.exceptions import CategoryNotFound
from core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from core.category.domain.category import Category


class TestUpdateCategory:

    def test_update_category_name(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        mock_repository: CategoryRepository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case: UpdateCategory = UpdateCategory(repository=mock_repository)
        update_category_request = UpdateCategoryRequest(
            id=category.id, name="New Movies"
        )
        use_case.execute(update_category_request)

        assert category.name == "New Movies"
        assert category.description == "Movie description"
        assert category.is_active is True
        assert category.id == update_category_request.id
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_description(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        mock_repository: CategoryRepository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case: UpdateCategory = UpdateCategory(repository=mock_repository)
        update_category_request = UpdateCategoryRequest(
            id=category.id, description="New Movie description"
        )
        use_case.execute(update_category_request)

        assert category.name == "Movie"
        assert category.description == "New Movie description"
        assert category.is_active is True
        assert category.id == update_category_request.id
        mock_repository.update.assert_called_once_with(category)
        pass

    def test_can_deactivate_category(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        mock_repository: CategoryRepository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case: UpdateCategory = UpdateCategory(repository=mock_repository)
        update_category_request = UpdateCategoryRequest(id=category.id, is_active=False)
        use_case.execute(update_category_request)

        assert category.name == "Movie"
        assert category.description == "Movie description"
        assert category.is_active is False
        assert category.id == update_category_request.id
        mock_repository.update.assert_called_once_with(category)

    def test_can_activate_category(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=False
        )
        mock_repository: CategoryRepository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case: UpdateCategory = UpdateCategory(repository=mock_repository)
        update_category_request = UpdateCategoryRequest(id=category.id, is_active=True)
        use_case.execute(update_category_request)

        assert category.name == "Movie"
        assert category.description == "Movie description"
        assert category.is_active is True
        assert category.id == update_category_request.id
        mock_repository.update.assert_called_once_with(category)

    def test_update_category_not_found(self) -> None:
        mock_repository: CategoryRepository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case: UpdateCategory = UpdateCategory(repository=mock_repository)
        update_category_request = UpdateCategoryRequest(id=str(uuid4()))
        with pytest.raises(CategoryNotFound) as e:
            use_case.execute(update_category_request)
        assert (
            str(e.value)
            == f"Category not found with the given id {update_category_request.id} while updating"
        )

    def test_update_category_with_name_empty(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        mock_repository: CategoryRepository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case: UpdateCategory = UpdateCategory(repository=mock_repository)
        update_category_request = UpdateCategoryRequest(id=category.id, name="")
        with pytest.raises(ValueError) as e:
            use_case.execute(update_category_request)
        assert str(e.value) == "name cannot be empty"

    def test_update_category_with_name_longer_than_255(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        mock_repository: CategoryRepository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case: UpdateCategory = UpdateCategory(repository=mock_repository)
        update_category_request = UpdateCategoryRequest(id=category.id, name="a" * 256)
        with pytest.raises(ValueError) as e:
            use_case.execute(update_category_request)
        assert str(e.value) == "name cannot be longer than 255 characters"

    def test_update_category_name_description_and_is_active(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        mock_repository: CategoryRepository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case: UpdateCategory = UpdateCategory(repository=mock_repository)
        update_category_request = UpdateCategoryRequest(
            id=category.id, name="New Movies", description="New Movie description", is_active=False
        )
        use_case.execute(update_category_request)

        assert category.name == "New Movies"
        assert category.description == "New Movie description"
        assert category.is_active is False
        assert category.id == update_category_request.id
        mock_repository.update.assert_called_once_with(category)
        
