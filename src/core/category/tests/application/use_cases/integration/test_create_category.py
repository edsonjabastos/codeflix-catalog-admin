from unittest.mock import MagicMock

import pytest

from core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
    CreateCategoryResponse,
)
from core.category.application.use_cases.exceptions import InvalidCategoryData
from core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestCreateCategory:

    def test_create_category_with_valid_data(self) -> None:
        repository: InMemoryCategoryRepository = InMemoryCategoryRepository()
        use_case: CreateCategory = CreateCategory(repository=repository)
        create_category_request: CreateCategoryRequest = CreateCategoryRequest(
            name="Movie",
            description="Movie description",
            is_active=True,
        )

        create_category_response: CreateCategoryResponse = use_case.execute(
            create_category_request
        )
        persisted_category = repository.categories[0]

        assert create_category_response is not None
        assert isinstance(create_category_response, CreateCategoryResponse)
        assert len(repository.categories) == 1

        assert persisted_category.name == "Movie"
        assert persisted_category.description == "Movie description"
        assert persisted_category.is_active is True
        assert persisted_category.id == create_category_response.id

    def test_create_category_with_invalid_data(self) -> None:
        magic_mocked_repository: MagicMock = MagicMock(
            InMemoryCategoryRepository()
        )
        use_case: CreateCategory = CreateCategory(repository=magic_mocked_repository)
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
        assert len(magic_mocked_repository.categories) == 0
        magic_mocked_repository.save.assert_not_called()
        # magic_mocked_repository.save.assert_called_once()
