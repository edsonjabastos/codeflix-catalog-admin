from typing import Any
import pytest
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestUserCanCreateAndEditCategory:
    def test_user_can_create_and_edit_category(self):
        api_client: APIClient = APIClient()

        # list categories
        list_response: Any = api_client.get("/api/categories/")
        assert list_response.status_code == 200
        assert list_response.data == {"data": []}

        # create category
        create_response: Any = api_client.post(
            "/api/categories/",
            data={
                "name": "Movie",
                "description": "Movie description",
            },
        )
        created_category_id: str = create_response.data["id"]
        assert create_response.status_code == 201
        assert create_response.data == {
            "id": created_category_id,
        }

        # check created category in list
        list_response: Any = api_client.get("/api/categories/")
        assert list_response.status_code == 200
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                }
            ]
        }

        # get created category
        get_response: Any = api_client.get(f"/api/categories/{created_category_id}/")
        assert get_response.status_code == 200
        assert get_response.data == {
            "data": {
                "id": created_category_id,
                "name": "Movie",
                "description": "Movie description",
                "is_active": True,
            }
        }

        # edit created category
        edit_response: Any = api_client.put(
            f"/api/categories/{created_category_id}/",
            data={
                "name": "Series",
                "description": "Series description",
                "is_active": False,
            },
        )
        assert edit_response.status_code == 204
        assert edit_response.data == None

        # check edited category in list
        list_response: Any = api_client.get("/api/categories/")
        assert list_response.status_code == 200
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Series",
                    "description": "Series description",
                    "is_active": False,
                }
            ]
        }

        # get edited category
        get_response: Any = api_client.get(f"/api/categories/{created_category_id}/")
        assert get_response.status_code == 200
        assert get_response.data == {
            "data": {
                "id": created_category_id,
                "name": "Series",
                "description": "Series description",
                "is_active": False,
            }
        }

    def test_user_can_create_and_delete_category(self):
        api_client: APIClient = APIClient()

        # list categories
        list_response: Any = api_client.get("/api/categories/")
        assert list_response.status_code == 200
        assert list_response.data == {"data": []}

        # create category
        create_response: Any = api_client.post(
            "/api/categories/",
            data={
                "name": "Movie",
                "description": "Movie description",
            },
        )
        created_category_id: str = create_response.data["id"]
        assert create_response.status_code == 201
        assert create_response.data == {
            "id": created_category_id,
        }

        # check created category in list
        list_response: Any = api_client.get("/api/categories/")
        assert list_response.status_code == 200
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Movie",
                    "description": "Movie description",
                    "is_active": True,
                }
            ]
        }

        # get created category
        get_response: Any = api_client.get(f"/api/categories/{created_category_id}/")
        assert get_response.status_code == 200
        assert get_response.data == {
            "data": {
                "id": created_category_id,
                "name": "Movie",
                "description": "Movie description",
                "is_active": True,
            }
        }

        # delete created category
        delete_response: Any = api_client.delete(
            f"/api/categories/{created_category_id}/"
        )
        assert delete_response.status_code == 204
        assert delete_response.data == None

        # check deleted category in list
        list_response: Any = api_client.get("/api/categories/")
        assert list_response.status_code == 200
        assert list_response.data == {"data": []}


    def test_user_cannot_create_category_and_edit_incorrectly(self):
        api_client: APIClient = APIClient()

        # create category with incorrect data
        create_response: Any = api_client.post(
            "/api/categories/",
            data={
                "name": "",
                "description": "Movie description",
                "is_active": "incorrect",
            },
        )
        assert create_response.status_code == 400
        assert create_response.data == {
            "name": ["This field may not be blank."],
            "is_active": ["Must be a valid boolean."],
        }

        # create category
        create_response: Any = api_client.post(
            "/api/categories/",
            data={
                "name": "Movie",
                "description": "Movie description",
            },
        )
        created_category_id: str = create_response.data["id"]
        assert create_response.status_code == 201
        assert create_response.data == {
            "id": created_category_id,
        }

        # edit created category with incorrect data
        edit_response: Any = api_client.put(
            f"/api/categories/{created_category_id}/",
            data={
                "name": "",
                "description": "Series description",
                "is_active": "incorrect",
            },
        )
        assert edit_response.status_code == 400
        assert edit_response.data == {
            "name": ["This field may not be blank."],
            "is_active": ["Must be a valid boolean."],
        }