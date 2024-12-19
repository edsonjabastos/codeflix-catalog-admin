from uuid import UUID

import pytest

from core.category.application.create_category import (
    InvalidCategoryData,
    create_category,
)


class TestCreateCategory:

    def test_create_category_with_valid_data(self) -> None:
        category_id = create_category(
            name="Movie", description="Movie description", is_active=True
        )

        assert category_id is not None
        assert isinstance(category_id, UUID)

    def test_create_category_with_invalid_data(self) -> None:
        with pytest.raises(
            InvalidCategoryData, match="name cannot be empty"
        ) as exc_info:
            create_category(name="")

        assert exc_info.type is InvalidCategoryData
        assert str(exc_info.value) == "name cannot be empty"
