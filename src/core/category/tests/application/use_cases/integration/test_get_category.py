from uuid import UUID, uuid4

import pytest

from core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
    GetCategoryResponse,
)
from core.category.application.use_cases.exceptions import (
    CategoryNotFound,
)
from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import (
    InMemoryCategoryRepository,
)


class TestGetCategory:

    def test_get_category_by_id(self) -> None:
        category_movie: Category = Category(
            name="Movie",
            description="Movie description",
            is_active=True,
        )
        category_series: Category = Category(
            name="Series",
            description="Series description",
            is_active=True,
        )
        repository: InMemoryCategoryRepository = InMemoryCategoryRepository(
            categories=[category_movie, category_series]
        )
        use_case: GetCategory = GetCategory(repository=repository)
        get_category_request: GetCategoryRequest = GetCategoryRequest(
            id=category_movie.id
        )

        get_category_response: GetCategoryResponse = use_case.execute(
            get_category_request
        )

        assert get_category_response == GetCategoryResponse(
            id=category_movie.id,
            name="Movie",
            description="Movie description",
            is_active=True,
        )

    def test_when_category_does_not_exist(self) -> None:
        category_movie: Category = Category(
            name="Movie",
            description="Movie description",
            is_active=True,
        )
        category_series: Category = Category(
            name="Series",
            description="Series description",
            is_active=True,
        )
        repository: InMemoryCategoryRepository = InMemoryCategoryRepository(
            categories=[category_movie, category_series]
        )
        use_case: GetCategory = GetCategory(repository=repository)
        not_existent_id: UUID = uuid4()
        get_category_request: GetCategoryRequest = GetCategoryRequest(
            id=not_existent_id
        )

        with pytest.raises(CategoryNotFound):
            use_case.execute(get_category_request)
