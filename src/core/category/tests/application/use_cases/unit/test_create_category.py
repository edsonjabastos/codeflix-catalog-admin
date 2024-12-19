from uuid import UUID

from unittest.mock import MagicMock
import pytest


from core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryResponse,
)
from core.category.application.use_cases.exceptions import InvalidCategoryData
from core.category.application.use_cases.create_category import CreateCategoryRequest
from core.category.infra.in_memory_category_repository import (
    CategoryRepository,
)


class TestCreateCategory:

    def test_create_category_with_valid_data(self) -> None:
        mock_repository: MagicMock = MagicMock(CategoryRepository)
        use_case: CreateCategory = CreateCategory(repository=mock_repository)
        create_category_request: CreateCategoryRequest = CreateCategoryRequest(
            name="Movie",
            description="Movie description",
            is_active=True,
        )

        created_category_response: CreateCategoryResponse = use_case.execute(
            create_category_request
        )

        assert created_category_response is not None
        assert isinstance(created_category_response, CreateCategoryResponse)
        assert isinstance(created_category_response.id, UUID)
        assert mock_repository.save.called is True

    def test_create_category_with_invalid_data(self) -> None:
        mock_repository: MagicMock = MagicMock(CategoryRepository)
        use_case: CreateCategory = CreateCategory(repository=mock_repository)
        create_category_request: CreateCategoryRequest = CreateCategoryRequest(
            name="",
            description="Movie description",
            is_active=True,
        )

        with pytest.raises(
            InvalidCategoryData, match="name cannot be empty"
        ) as exc_info:
            use_case.execute(
                request=create_category_request
            )

        assert exc_info.type is InvalidCategoryData
        assert str(exc_info.value) == "name cannot be empty"
        assert mock_repository.save.called is False
