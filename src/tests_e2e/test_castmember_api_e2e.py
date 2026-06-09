"""E2E smoke tests for cast members with real Keycloak authentication."""

from typing import Any

import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCastMemberE2ESmoke:
    def test_authenticated_create_and_retrieve_castmember(
        self, api_client: APIClient
    ) -> None:
        create_response: Any = api_client.post(
            "/api/cast_members/",
            data={
                "name": "E2E Actor",
                "type": "ACTOR",
            },
        )
        assert create_response.status_code == HTTP_201_CREATED
        cast_member_id: str = create_response.data["id"]

        get_response: Any = api_client.get(f"/api/cast_members/{cast_member_id}/")
        assert get_response.status_code == HTTP_200_OK
        assert get_response.data == {
            "data": {
                "id": cast_member_id,
                "name": "E2E Actor",
                "type": "ACTOR",
            }
        }
