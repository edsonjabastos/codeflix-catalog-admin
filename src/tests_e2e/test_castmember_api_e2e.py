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
class TestUserCanCreateAndEditCastMember:
    def test_user_can_create_and_edit_castmember(self):
        api_client: APIClient = APIClient()

        # list castmembers
        list_response: Any = api_client.get("/api/cast_members/")
        assert list_response.status_code == HTTP_200_OK
        assert list_response.data == {
            "data": [],
            "meta": {"current_page": 1, "per_page": 2, "total": 0},
        }

        # create castmember
        create_response: Any = api_client.post(
            "/api/cast_members/",
            data={
                "name": "Jackie Chan",
                "type": "ACTOR",
            },
        )
        created_castmember_id: str = create_response.data["id"]
        assert create_response.status_code == HTTP_201_CREATED
        assert create_response.data == {
            "id": created_castmember_id,
        }

        # check created castmember in list
        list_response: Any = api_client.get("/api/cast_members/")
        assert list_response.status_code == HTTP_200_OK
        assert list_response.data == {
            "data": [
                {
                    "id": created_castmember_id,
                    "name": "Jackie Chan",
                    "type": "ACTOR",
                }
            ],
            "meta": {"current_page": 1, "per_page": 2, "total": 1},
        }

        # get created castmember
        # get_response: Any = api_client.get(f"/api/cast_members/{created_castmember_id}/")
        # assert get_response.status_code == HTTP_200_OK
        # assert get_response.data == {
        #     "data": {
        #         "id": created_castmember_id,
        #         "name": "Jackie Chan",
        #         "type": "ACTOR",
        #     }
        # }

        # edit created castmember
        edit_response: Any = api_client.put(
            f"/api/cast_members/{created_castmember_id}/",
            data={
                "name": "Jackie Chan",
                "type": "DIRECTOR",
            },
        )
        assert edit_response.status_code == HTTP_204_NO_CONTENT
        assert edit_response.data is None

        # check edited castmember in list
        list_response: Any = api_client.get("/api/cast_members/")
        assert list_response.status_code == HTTP_200_OK
        assert list_response.data == {
            "data": [
                {
                    "id": created_castmember_id,
                    "name": "Jackie Chan",
                    "type": "DIRECTOR",
                }
            ],
            "meta": {"current_page": 1, "per_page": 2, "total": 1},
        }

        # get edited castmember
        # get_response: Any = api_client.get(f"/api/cast_members/{created_castmember_id}/")
        # assert get_response.status_code == HTTP_200_OK
        # assert get_response.data == {
        #     "data": {
        #         "id": created_castmember_id,
        #         "name": "Jackie Chan",
        #         "type": "DIRECTOR",
        #     }
        # }

    def test_user_can_create_and_delete_castmember(self):
        api_client: APIClient = APIClient()

        # list castmembers
        list_response: Any = api_client.get("/api/cast_members/")
        assert list_response.status_code == HTTP_200_OK
        assert list_response.data == {
            "data": [],
            "meta": {"current_page": 1, "per_page": 2, "total": 0},
        }

        # create castmember
        create_response: Any = api_client.post(
            "/api/cast_members/",
            data={
                "name": "Robert Downey Jr.",
                "type": "ACTOR",
            },
        )
        created_castmember_id: str = create_response.data["id"]
        assert create_response.status_code == HTTP_201_CREATED
        assert create_response.data == {
            "id": created_castmember_id,
        }

        # check created castmember in list
        list_response: Any = api_client.get("/api/cast_members/")
        assert list_response.status_code == HTTP_200_OK
        assert list_response.data == {
            "data": [
                {
                    "id": created_castmember_id,
                    "name": "Robert Downey Jr.",
                    "type": "ACTOR",
                }
            ],
            "meta": {"current_page": 1, "per_page": 2, "total": 1},
        }

        # get created castmember
        # get_response: Any = api_client.get(f"/api/cast_members/{created_castmember_id}/")
        # assert get_response.status_code == HTTP_200_OK
        # assert get_response.data == {
        #     "data": {
        #         "id": created_castmember_id,
        #         "name": "Movie",
        #         "description": "Movie description",
        #         "is_active": True,
        #     }
        # }

        # delete created castmember
        delete_response: Any = api_client.delete(
            f"/api/cast_members/{created_castmember_id}/"
        )
        assert delete_response.status_code == HTTP_204_NO_CONTENT
        assert delete_response.data is None

        # check deleted castmember in list
        list_response: Any = api_client.get("/api/cast_members/")
        assert list_response.status_code == HTTP_200_OK
        assert list_response.data == {
            "data": [],
            "meta": {"current_page": 1, "per_page": 2, "total": 0},
        }

    def test_user_cannot_create_castmember_and_edit_incorrectly(self):
        api_client: APIClient = APIClient()

        # create castmember with incorrect data
        create_response: Any = api_client.post(
            "/api/cast_members/",
            data={
                "name": "",
                "type": "incorrect",
            },
        )
        assert create_response.status_code == HTTP_400_BAD_REQUEST
        assert create_response.data == {
            "name": ["This field may not be blank."],
            "type": ['"incorrect" is not a valid choice.'],
        }

        # create castmember
        create_response: Any = api_client.post(
            "/api/cast_members/",
            data={
                "name": "Emma Watson",
                "type": "ACTOR",
            },
        )
        created_castmember_id: str = create_response.data["id"]
        assert create_response.status_code == HTTP_201_CREATED
        assert create_response.data == {
            "id": created_castmember_id,
        }

        # edit created castmember with incorrect data
        edit_response: Any = api_client.put(
            f"/api/cast_members/{created_castmember_id}/",
            data={
                "name": "a" * 256,
                "type": "incorrect",
            },
        )
        assert edit_response.status_code == HTTP_400_BAD_REQUEST
        assert edit_response.data == {
            "name": ["Ensure this field has no more than 255 characters."],
            "type": ['"incorrect" is not a valid choice.'],
        }
