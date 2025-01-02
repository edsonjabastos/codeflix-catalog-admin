from core.category.application.use_cases.list_category import (
    CategoryOutput,
    ListCategory,
    ListCategoryRequest,
    ListCategoryResponse,
)
from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestListCategory:
    
    def test_return_empty_list_when_no_categories_in_repository(self) -> None:
        repository: InMemoryCategoryRepository = InMemoryCategoryRepository()

        use_case: ListCategory = ListCategory(repository=repository)
        request: ListCategoryRequest = ListCategoryRequest()
        response: ListCategoryResponse = use_case.execute(request)

        assert response == ListCategoryResponse(data=[])

    def test_return_list_of_categories_when_categories_in_repository(self) -> None:
        category_movies = Category(
            name="Movies", description="Movies description", is_active=True
        )
        category_series = Category(
            name="Series", description="Series description", is_active=True
        )
        repository: InMemoryCategoryRepository = InMemoryCategoryRepository(
            categories=[category_movies, category_series]
        )

        use_case: ListCategory = ListCategory(repository=repository)
        request: ListCategoryRequest = ListCategoryRequest()
        response: ListCategoryResponse = use_case.execute(request)

        assert response == ListCategoryResponse(
            data=[
                CategoryOutput(
                    id=category_movies.id,
                    name=category_movies.name,
                    description=category_movies.description,
                    is_active=category_movies.is_active,
                ),
                CategoryOutput(
                    id=category_series.id,
                    name=category_series.name,
                    description=category_series.description,
                    is_active=category_series.is_active,
                ),
            ]
        )
