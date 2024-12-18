import unittest
from uuid import UUID
import uuid
from category import Category


class TestCategory(unittest.TestCase):
    def test_name_is_required(self):
        with self.assertRaisesRegex(
            TypeError, "missing 1 required positional argument: 'name'"
        ):
            Category()

    def test_name_must_have_less_than_255_characters(self):
        with self.assertRaisesRegex(
            ValueError, "name must have less than 256 characters"
        ):
            Category("a" * 256)

    def test_category_must_be_created_with_id_as_uuid(self):
        category = Category("Movie")
        self.assertEqual(type(category.id), UUID)

    def test_created_category_with_default_values(self):
        category = Category("Movie")
        self.assertEqual(category.name, "Movie")
        self.assertEqual(category.description, "")
        self.assertEqual(category.is_active, True)

    def test_category_is_created_as_active_by_default(self):
        category = Category("Movie")
        self.assertTrue(category.is_active)

    def test_category_is_created_with_provided_values(self):
        category_id = uuid.uuid4()
        category = Category(
            id=category_id,
            name="Movie",
            description="Movie description",
            is_active=False,
        )
        self.assertEqual(category.name, "Movie")
        self.assertEqual(category.description, "Movie description")
        self.assertFalse(category.is_active)

    def test_category_str(self):
        category_name = "Movie"
        category_description = "Movie description"
        category_is_active = True
        category = Category(
            name=category_name,
            description=category_description,
            is_active=category_is_active,
        )
        self.assertEqual(
            str(category),
            f"{category_name} - {category_description} ({category_is_active})",
        )

    def test_category_repr(self):
        category_id = uuid.uuid4()
        category_name = "Movie"
        category = Category(id=category_id, name=category_name)
        self.assertEqual(
            repr(category), f"<Category {category_name} ({category_id})>"
        )

if __name__ == "__main__":
    unittest.main()
