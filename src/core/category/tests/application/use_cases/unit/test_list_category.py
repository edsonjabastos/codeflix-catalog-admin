from unittest.mock import create_autospec
from core.category.domain.category_repository import CategoryRepository
from core.category.application.use_cases.list_category import ListCategory
from core.category.domain.category import Category


class TestListCategory:

    def test_when_no_categories_in_repository_then_return_empty_list(self) -> None:
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = []

        use_case = ListCategory(repository=mock_repository)
        request = ListCategory.Input()
        response = use_case.execute(request)
        default_meta = ListCategory.OutputMeta(current_page=1, per_page=2, total=0)

        assert response == ListCategory.ListOutput(data=[], meta=default_meta)

    def test_when_categories_in_repository_then_return_list_of_categories(self) -> None:
        category_movies = Category(
            name="Movies", description="Movies description", is_active=True
        )
        category_series = Category(
            name="Series", description="Series description", is_active=True
        )
        mock_repository = create_autospec(CategoryRepository)
        mock_repository.list.return_value = [category_movies, category_series]

        use_case = ListCategory(repository=mock_repository)
        request = ListCategory.Input()
        response = use_case.execute(request)
        total = len(mock_repository.list())
        meta = ListCategory.OutputMeta(current_page=1, per_page=2, total=total)

        assert response == ListCategory.ListOutput(
            data=[
                ListCategory.Output(
                    id=category_movies.id,
                    name=category_movies.name,
                    description=category_movies.description,
                    is_active=category_movies.is_active,
                ),
                ListCategory.Output(
                    id=category_series.id,
                    name=category_series.name,
                    description=category_series.description,
                    is_active=category_series.is_active,
                ),
            ],
            meta=meta,
        )
