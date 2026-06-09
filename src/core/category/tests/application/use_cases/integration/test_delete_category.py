from uuid import uuid4
from core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestDeleteCategory:
    def test_delete_category_from_repository(self) -> None:
        category_movie = Category(
            id=uuid4(), name="Movie", description="Movie description", is_active=True
        )
        category_series = Category(
            id=uuid4(), name="Series", description="Series description", is_active=True
        )
        repository = InMemoryCategoryRepository(
            categories=[category_movie, category_series]
        )

        use_case = DeleteCategory(repository=repository)
        request = DeleteCategoryRequest(id=category_movie.id)

        assert repository.get_by_id(category_movie.id) is not None
        response = use_case.execute(request)

        assert repository.get_by_id(category_movie.id) is None
        assert response is None
