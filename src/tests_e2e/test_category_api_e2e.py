from typing import Any
import pytest
from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)


@pytest.mark.django_db
class TestUserCanCreateAndEditCategory:

    def test_user_can_create_and_edit_category(self):
        api_client: APIClient = APIClient()

        # list categories
        list_response: Any = api_client.get("/api/categories/")
        assert list_response.status_code == HTTP_200_OK
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
        assert create_response.status_code == HTTP_201_CREATED
        assert create_response.data == {
            "id": created_category_id,
        }

        # check created category in list
        list_response: Any = api_client.get("/api/categories/")
        assert list_response.status_code == HTTP_200_OK
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
        assert get_response.status_code == HTTP_200_OK
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
        assert edit_response.status_code == HTTP_204_NO_CONTENT
        assert edit_response.data is None

        # check edited category in list
        list_response: Any = api_client.get("/api/categories/")
        assert list_response.status_code == HTTP_200_OK
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
        assert get_response.status_code == HTTP_200_OK
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
        assert list_response.status_code == HTTP_200_OK
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
        assert create_response.status_code == HTTP_201_CREATED
        assert create_response.data == {
            "id": created_category_id,
        }

        # check created category in list
        list_response: Any = api_client.get("/api/categories/")
        assert list_response.status_code == HTTP_200_OK
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
        assert get_response.status_code == HTTP_200_OK
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
        assert delete_response.status_code == HTTP_204_NO_CONTENT
        assert delete_response.data is None

        # check deleted category in list
        list_response: Any = api_client.get("/api/categories/")
        assert list_response.status_code == HTTP_200_OK
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
        assert create_response.status_code == HTTP_400_BAD_REQUEST
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
        assert create_response.status_code == HTTP_201_CREATED
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
        assert edit_response.status_code == HTTP_400_BAD_REQUEST
        assert edit_response.data == {
            "name": ["This field may not be blank."],
            "is_active": ["Must be a valid boolean."],
        }

    def test_user_can_partial_edit_category(self):
        api_client: APIClient = APIClient()

        # create category
        create_response: Any = api_client.post(
            "/api/categories/",
            data={
                "name": "Movie",
                "description": "Movie description",
            },
        )
        created_category_id: str = create_response.data["id"]
        assert create_response.status_code == HTTP_201_CREATED
        assert create_response.data == {
            "id": created_category_id,
        }

        # check created category in list
        list_response: Any = api_client.get("/api/categories/")
        assert list_response.status_code == HTTP_200_OK
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

        # partial edit name created category
        edit_response: Any = api_client.patch(
            f"/api/categories/{created_category_id}/",
            data={
                "name": "Series",
            },
        )
        assert edit_response.status_code == HTTP_204_NO_CONTENT
        assert edit_response.data is None

        # check edited category in list
        list_response: Any = api_client.get("/api/categories/")
        assert list_response.status_code == HTTP_200_OK
        assert list_response.data == {
            "data": [
                {
                    "id": created_category_id,
                    "name": "Series",
                    "description": "Movie description",
                    "is_active": True,
                }
            ]
        }

        # get edited category
        get_response: Any = api_client.get(f"/api/categories/{created_category_id}/")
        assert get_response.status_code == HTTP_200_OK
        assert get_response.data == {
            "data": {
                "id": created_category_id,
                "name": "Series",
                "description": "Movie description",
                "is_active": True,
            }
        }

        # partial edit description created category
        edit_response: Any = api_client.patch(
            f"/api/categories/{created_category_id}/",
            data={
                "description": "Series description",
            },
        )
        assert edit_response.status_code == HTTP_204_NO_CONTENT
        assert edit_response.data is None

        # check edited category in list
        get_response: Any = api_client.get(f"/api/categories/{created_category_id}/")
        assert get_response.status_code == HTTP_200_OK
        assert get_response.data == {
            "data": {
                "id": created_category_id,
                "name": "Series",
                "description": "Series description",
                "is_active": True,
            }
        }

        # partial edit is_active created category
        edit_response: Any = api_client.patch(
            f"/api/categories/{created_category_id}/",
            data={
                "is_active": False,
            },
        )
        assert edit_response.status_code == HTTP_204_NO_CONTENT
        assert edit_response.data is None

        # check edited category in list
        get_response: Any = api_client.get(f"/api/categories/{created_category_id}/")
        assert get_response.status_code == HTTP_200_OK
        assert get_response.data == {
            "data": {
                "id": created_category_id,
                "name": "Series",
                "description": "Series description",
                "is_active": False,
            }
        }
