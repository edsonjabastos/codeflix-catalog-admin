import pytest
from uuid import UUID
import uuid
from core.category.domain.category import Category
from unittest.mock import patch


class TestCategory:

    def test_name_is_required(self) -> None:
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Category()

    def test_name_must_have_less_than_255_characters(self) -> None:
        with pytest.raises(
            ValueError, match="name cannot be longer than 255 characters"
        ):
            Category("a" * 256)

    def test_category_must_be_created_with_id_as_uuid(self) -> None:
        category = Category("Movie")

        assert isinstance(category.id, UUID)

    def test_created_category_with_default_values(self) -> None:
        category = Category("Movie")

        assert category.name == "Movie"
        assert category.description == ""
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self) -> None:
        category = Category("Movie")
        assert category.is_active is True

    def test_category_is_created_with_provided_values(self) -> None:
        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="Movie",
            description="Movie description",
            is_active=False,
        )

        assert category.id == category_id
        assert category.name == "Movie"
        assert category.description == "Movie description"
        assert category.is_active is False

    def test_category_str(self) -> None:
        category_name = "Movie"
        category_description = "Movie description"
        category_is_active = True
        category = Category(
            name=category_name,
            description=category_description,
            is_active=category_is_active,
        )

        assert (
            str(category)
            == f"{category_name} - {category_description} ({category_is_active})"
        )

    def test_category_repr(self) -> None:
        category_id = uuid.uuid4()
        category_name = "Movie"
        category = Category(id=category_id, name=category_name)

        assert repr(category) == f"<Category {category_name} ({category_id})>"

    def test_cannot_create_category_with_empty_name(self) -> None:
        with pytest.raises(ValueError, match="name cannot be empty"):
            Category("")

    def test_description_must_have_less_than_1024_characters(self) -> None:
        with pytest.raises(
            ValueError, match="description cannot be longer than 1024 characters"
        ):
            Category("Movie", "a" * 1025)

    def test_name_and_description_are_invalid(self) -> None:
        with pytest.raises(
            ValueError,
            match="^name cannot be empty, description cannot be longer than 1024 characters$",
        ) as exc_info:
            Category("", "a" * 1025)



class TestUpdateCategory:

    def test_update_category(self) -> None:
        category = Category("Movie")

        category.update_category("Documentary", "Documentary description")

        assert category.name == "Documentary"
        assert category.description == "Documentary description"

    def test_update_category_with_invalid_name(self) -> None:
        category = Category("Movie")

        with pytest.raises(
            ValueError, match="name cannot be longer than 255 characters"
        ):
            category.update_category("a" * 256, "Documentary description")

    def test_cannot_update_category_with_empty_name(self) -> None:
        category = Category("Movie")

        with pytest.raises(ValueError, match="name cannot be empty"):
            category.update_category("", "Documentary description")

    def test_validate_name_called_on_update(self) -> None:
        category = Category("Movie")

        with patch.object(category, "validate_name") as mock_validate_name:
            category.update_category("Documentary", "Documentary description")
            mock_validate_name.assert_called_once()


class TestActivateCategory:

    def test_activate_inactive_category(self) -> None:
        category = Category("Movie", is_active=False)

        category.activate()

        assert category.is_active is True

    def test_activate_active_category(self) -> None:
        category = Category("Movie", is_active=True)

        category.activate()

        assert category.is_active is True

    def test_validate_name_called_on_activate(self) -> None:
        category = Category("Movie", is_active=False)

        with patch.object(category, "validate_name") as mock_validate_name:
            category.activate()
            mock_validate_name.assert_called_once()


class TestDeactivateCategory:

    def test_deactivate_active_category(self) -> None:
        category = Category("Movie", is_active=True)

        category.deactivate()

        assert category.is_active is False

    def test_deactivate_inactive_category(self) -> None:
        category = Category("Movie", is_active=False)

        category.deactivate()

        assert category.is_active is False

    def test_validate_name_called_on_deactivate(self) -> None:
        category = Category("Movie", is_active=True)

        with patch.object(category, "validate_name") as mock_validate_name:
            category.deactivate()
            mock_validate_name.assert_called_once()


class TestEquality:

    def test_when_categories_have_same_id_and_class(self) -> None:
        category_id = uuid.uuid4()
        category1 = Category(id=category_id, name="Movie")
        category2 = Category(id=category_id, name="Movie")

        assert category1 == category2

    def test_equality_with_different_class(self) -> None:
        class FakeCategory: ...

        common_id = uuid.uuid4()
        category = Category(id=common_id, name="Movie")
        fake_category = FakeCategory()
        fake_category.id = common_id

        assert category != fake_category
