"""E2E smoke tests for videos with real Keycloak authentication."""

from typing import Any

import pytest
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestVideoE2ESmoke:
    def test_authenticated_create_video_with_relationships(
        self, api_client: APIClient
    ) -> None:
        category_response: Any = api_client.post(
            "/api/categories/",
            data={
                "name": "E2E Movie",
                "description": "E2E category",
                "is_active": True,
            },
        )
        assert category_response.status_code == HTTP_201_CREATED
        category_id: str = category_response.data["id"]

        genre_response: Any = api_client.post(
            "/api/genres/",
            data={
                "name": "E2E Action",
                "is_active": True,
                "categories": [category_id],
            },
        )
        assert genre_response.status_code == HTTP_201_CREATED
        genre_id: str = genre_response.data["id"]

        cast_member_response: Any = api_client.post(
            "/api/cast_members/",
            data={"name": "E2E Actor", "type": "ACTOR"},
        )
        assert cast_member_response.status_code == HTTP_201_CREATED
        cast_member_id: str = cast_member_response.data["id"]

        video_response: Any = api_client.post(
            "/api/videos/",
            data={
                "title": "E2E Test Video",
                "description": "E2E smoke test",
                "launch_year": 2023,
                "duration": "120.00",
                "rating": "AGE_14",
                "categories": [category_id],
                "genres": [genre_id],
                "cast_members": [cast_member_id],
            },
        )
        assert video_response.status_code == HTTP_201_CREATED
        video_id: str = video_response.data["id"]

        get_response: Any = api_client.get(f"/api/videos/{video_id}/")
        assert get_response.status_code == HTTP_200_OK
        assert get_response.data["data"]["id"] == video_id
        assert get_response.data["data"]["title"] == "E2E Test Video"
        assert get_response.data["data"]["categories"] == [category_id]
        assert get_response.data["data"]["genres"] == [genre_id]
        assert get_response.data["data"]["cast_members"] == [cast_member_id]
