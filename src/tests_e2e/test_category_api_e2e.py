"""E2E smoke tests for categories with real Keycloak authentication."""

from typing import Any

import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestCategoryE2ESmoke:
    def test_authenticated_create_and_retrieve_category(
        self, api_client: APIClient
    ) -> None:
        create_response: Any = api_client.post(
            "/api/categories/",
            data={
                "name": "E2E Movie",
                "description": "Created during E2E smoke test",
            },
        )
        assert create_response.status_code == HTTP_201_CREATED
        category_id: str = create_response.data["id"]

        get_response: Any = api_client.get(f"/api/categories/{category_id}/")
        assert get_response.status_code == HTTP_200_OK
        assert get_response.data == {
            "data": {
                "id": category_id,
                "name": "E2E Movie",
                "description": "Created during E2E smoke test",
                "is_active": True,
            }
        }
