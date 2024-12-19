import unittest
import pytest
from uuid import UUID
import uuid
from category import Category


class TestCategory:
    def test_name_is_required(self):
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            Category("a" * 256)

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category("Movie")

        assert isinstance(category.id, UUID)

    def test_created_category_with_default_values(self):
        category = Category("Movie")

        assert category.name == "Movie"
        assert category.description == ""
        assert category.is_active is True

    def test_category_is_created_as_active_by_default(self):
        category = Category("Movie")
        assert category.is_active is True

    def test_category_is_created_with_provided_values(self):
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

    def test_category_str(self):
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

    def test_category_repr(self):
        category_id = uuid.uuid4()
        category_name = "Movie"
        category = Category(id=category_id, name=category_name)

        assert repr(category) == f"<Category {category_name} ({category_id})>"


class TestUpdateCategory:
    def test_update_category(self):
        category = Category("Movie")

        category.update_category("Documentary", "Documentary description")

        assert category.name == "Documentary"
        assert category.description == "Documentary description"

    def test_update_category_with_invalid_name_and_raise_exception(self):
        category = Category("Movie")

        with pytest.raises(ValueError, match="name must have less than 256 characters"):
            category.update_category("a" * 256, "Documentary description")