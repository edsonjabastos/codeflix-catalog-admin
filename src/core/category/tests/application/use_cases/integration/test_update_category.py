from core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from core.category.domain.category import Category
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository


class TestUpdateCategory:

    def test_can_update_category_name_and_description(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()

        repsitory.save(category)

        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(
            id=category.id, name="New Movies", description="New Movie description"
        )
        use_case.execute(update_category_request)

        updated_category = repsitory.get_by_id(category.id)

        assert updated_category.name == "New Movies"
        assert updated_category.description == "New Movie description"
        assert updated_category.is_active is True
        assert updated_category.id == update_category_request.id

    def test_update_category_name(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()

        repsitory.save(category)

        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(
            id=category.id, name="New Movies"
        )
        use_case.execute(update_category_request)

        updated_category = repsitory.get_by_id(category.id)

        assert updated_category.name == "New Movies"
        assert updated_category.description == "Movie description"
        assert updated_category.is_active is True
        assert updated_category.id == update_category_request.id

    def test_update_category_description(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()

        repsitory.save(category)

        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(
            id=category.id, description="New Movie description"
        )
        use_case.execute(update_category_request)

        updated_category = repsitory.get_by_id(category.id)

        assert updated_category.name == "Movie"
        assert updated_category.description == "New Movie description"
        assert updated_category.is_active is True
        assert updated_category.id == update_category_request.id

    def test_can_deactivate_category(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=True
        )
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()

        repsitory.save(category)

        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(id=category.id, is_active=False)
        use_case.execute(update_category_request)

        updated_category = repsitory.get_by_id(category.id)

        assert updated_category.name == "Movie"
        assert updated_category.description == "Movie description"
        assert updated_category.is_active is False
        assert updated_category.id == update_category_request.id

    def test_can_activate_category(self) -> None:
        category: Category = Category(
            name="Movie", description="Movie description", is_active=False
        )
        repsitory: InMemoryCategoryRepository = InMemoryCategoryRepository()

        repsitory.save(category)

        use_case: UpdateCategory = UpdateCategory(repository=repsitory)
        update_category_request = UpdateCategoryRequest(id=category.id, is_active=True)
        use_case.execute(update_category_request)

        updated_category = repsitory.get_by_id(category.id)

        assert updated_category.name == "Movie"
        assert updated_category.description == "Movie description"
        assert updated_category.is_active is True
        assert updated_category.id == update_category_request.id
