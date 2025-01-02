from unittest.mock import create_autospec
from uuid import uuid4

import pytest
from core.category.application.use_cases.category_repository import CategoryRepository
from core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from core.category.application.use_cases.exceptions import CategoryNotFound
from core.category.domain.category import Category


class TestDeleteCategory:

    def test_delete_category_from_repository(self) -> None:
        category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        mock_repository: CategoryRepository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category

        use_case: DeleteCategory = DeleteCategory(repository=mock_repository)
        use_case.execute(DeleteCategoryRequest(id=category.id))

        mock_repository.delete.assert_called_once_with(category.id)

    def test_delete_category_not_found(self) -> None:
        mock_repository: CategoryRepository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = None

        use_case = DeleteCategory(repository=mock_repository)

        with pytest.raises(CategoryNotFound):
            use_case.execute(DeleteCategoryRequest(id=uuid4()))

        mock_repository.delete.assert_not_called()
        assert mock_repository.delete.called is False
        # assert mock_repository.delete.called is True # false positive
