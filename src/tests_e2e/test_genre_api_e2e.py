"""E2E smoke tests for genres with real Keycloak authentication."""

from typing import Any

import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestGenreE2ESmoke:
    def test_authenticated_create_and_retrieve_genre(
        self, api_client: APIClient
    ) -> None:
        category_response: Any = api_client.post(
            "/api/categories/",
            data={
                "name": "E2E Category for Genre",
                "description": "Prerequisite category",
                "is_active": True,
            },
        )
        assert category_response.status_code == HTTP_201_CREATED
        category_id: str = category_response.data["id"]

        create_response: Any = api_client.post(
            "/api/genres/",
            data={
                "name": "E2E Drama",
                "is_active": True,
                "categories": [category_id],
            },
        )
        assert create_response.status_code == HTTP_201_CREATED
        genre_id: str = create_response.data["id"]

        get_response: Any = api_client.get(f"/api/genres/{genre_id}/")
        assert get_response.status_code == HTTP_200_OK
        assert get_response.data["data"]["id"] == genre_id
        assert get_response.data["data"]["name"] == "E2E Drama"
        assert get_response.data["data"]["categories"] == [category_id]
