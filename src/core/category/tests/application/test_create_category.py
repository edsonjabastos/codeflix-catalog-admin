from unittest.mock import MagicMock
from uuid import UUID

import pytest

from core.category.application.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    InvalidCategoryData,
)
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

        category_id: UUID = use_case.execute(create_category_request)

        assert category_id is not None
        assert isinstance(category_id, UUID)
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
            use_case.execute(request=create_category_request)

        assert exc_info.type is InvalidCategoryData
        assert str(exc_info.value) == "name cannot be empty"
        assert mock_repository.save.called is False
