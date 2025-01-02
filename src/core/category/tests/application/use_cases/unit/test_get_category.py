from unittest.mock import create_autospec

from core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryResponse,
    GetCategoryRequest,
)
from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import (
    CategoryRepository,
)


class TestGetCategory:

    def test_return_found_category(self) -> None:
        category_movie: Category = Category(
            name="Movie",
            description="Movie description",
            is_active=True,
        )
        mock_repository: CategoryRepository = create_autospec(CategoryRepository)
        mock_repository.get_by_id.return_value = category_movie
        use_case: GetCategory = GetCategory(repository=mock_repository)
        get_category_request: GetCategoryRequest = GetCategoryRequest(
            id=category_movie.id
        )

        created_category_response: GetCategoryResponse = use_case.execute(
            get_category_request
        )

        assert created_category_response == GetCategoryResponse(
            id=category_movie.id,
            name=category_movie.name,
            description=category_movie.description,
            is_active=category_movie.is_active,
        )
