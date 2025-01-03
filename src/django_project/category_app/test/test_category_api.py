from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK

from core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository


class CategoryTestCase(APITestCase):
    def test_list_categories(self):
        repository = DjangoORMCategoryRepository()
        movie_category = Category(
            name="Movie",
            description="Movie category",
        )
        documentary_category = Category(
            name="Documentary",
            description="Documentary category",
        )
        repository.save(movie_category)
        repository.save(documentary_category)

        url = "/api/categories/"
        response = self.client.get(url)

        expected_data = [
            {
                "id": str(movie_category.id),
                "name": movie_category.name,
                "description": movie_category.description,
                "is_active": movie_category.is_active,
            },
            {
                "id": str(documentary_category.id),
                "name": documentary_category.name,
                "description": documentary_category.description,
                "is_active": documentary_category.is_active,
            },
        ]

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
