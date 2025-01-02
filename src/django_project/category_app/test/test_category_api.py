from rest_framework.test import APITestCase
from rest_framework.status import HTTP_200_OK


class CategoryTestCase(APITestCase):
    def test_list_categories(self):
        url = "/api/categories/"
        response = self.client.get(url)

        expected_data = [
            {
                "id": "6fd173e3-9fd2-4443-add0-ee83c27d4936",
                "name": "Movie",
                "description": "Movie category",
                "is_active": True,
            },
            {
                "id": "c8b17960-69c0-4254-a569-3715cfbfc114",
                "name": "Documentary",
                "description": "Documentary category",
                "is_active": True,
            },
        ]

        self.assertEqual(response.status_code, HTTP_200_OK)
        self.assertEqual(response.data, expected_data)
