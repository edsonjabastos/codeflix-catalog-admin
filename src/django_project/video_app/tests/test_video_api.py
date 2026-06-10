import pytest
from decimal import Decimal
from typing import Any
from uuid import uuid4

from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.test import APIClient

from core.castmember.domain.castmember import CastMember
from core.category.domain.category import Category
from core.genre.domain.genre import Genre
from core.video.domain.value_objects import Rating
from django_project.adapters.persistence.django.castmember_repository import (
    DjangoORMCastMemberRepository,
)
from django_project.adapters.persistence.django.category_repository import (
    DjangoORMCategoryRepository,
)
from django_project.adapters.persistence.django.genre_repository import (
    DjangoORMGenreRepository,
)
from django_project.adapters.persistence.django.video_repository import (
    DjangoORMVideoRepository,
)


@pytest.mark.django_db
class TestCreateVideoAPI:

    def test_create_video_with_valid_data(
        self,
        api_client: APIClient,
        category_movie: Category,
        genre_action: Genre,
        cast_member_actor: CastMember,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
        cast_member_repository: DjangoORMCastMemberRepository,
        video_repository: DjangoORMVideoRepository,
    ) -> None:
        category_repository.save(category_movie)
        genre_repository.save(genre_action)
        cast_member_repository.save(cast_member_actor)

        data: dict[str, Any] = {
            "title": "Test Video",
            "description": "A test video description",
            "launch_year": 2023,
            "duration": "90.5",
            "rating": "L",
            "published": False,
            "categories": [str(category_movie.id)],
            "genres": [str(genre_action.id)],
            "cast_members": [str(cast_member_actor.id)],
        }

        response: Any = api_client.post("/api/videos/", data=data)

        assert response.status_code == HTTP_201_CREATED
        assert response.data["id"]

        created_video_id: str = response.data["id"]
        created_video = video_repository.get_by_id(created_video_id)

        assert created_video.title == "Test Video"
        assert created_video.description == "A test video description"
        assert created_video.launch_year == 2023
        assert created_video.duration == Decimal("90.5")
        assert created_video.rating == Rating.L
        assert created_video.published is False
        assert category_movie.id in created_video.categories
        assert genre_action.id in created_video.genres
        assert cast_member_actor.id in created_video.cast_members

    def test_create_video_with_invalid_data(self, api_client: APIClient) -> None:
        data: dict[str, Any] = {
            "title": "",
            "description": "",
        }
        response: Any = api_client.post("/api/videos/", data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_create_video_with_nonexistent_category(
        self,
        api_client: APIClient,
        genre_action: Genre,
        cast_member_actor: CastMember,
        genre_repository: DjangoORMGenreRepository,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        genre_repository.save(genre_action)
        cast_member_repository.save(cast_member_actor)

        nonexistent_category_id = uuid4()

        data: dict[str, Any] = {
            "title": "Test Video",
            "description": "A test video description",
            "launch_year": 2023,
            "duration": "90.5",
            "rating": "L",
            "published": False,
            "categories": [str(nonexistent_category_id)],
            "genres": [str(genre_action.id)],
            "cast_members": [str(cast_member_actor.id)],
        }

        response: Any = api_client.post("/api/videos/", data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            "error": (
                f"Categories with provided IDs not found: {nonexistent_category_id}"
            )
        }

    def test_create_video_with_nonexistent_genre(
        self,
        api_client: APIClient,
        category_movie: Category,
        cast_member_actor: CastMember,
        category_repository: DjangoORMCategoryRepository,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        category_repository.save(category_movie)
        cast_member_repository.save(cast_member_actor)

        nonexistent_genre_id = uuid4()

        data: dict[str, Any] = {
            "title": "Test Video",
            "description": "A test video description",
            "launch_year": 2023,
            "duration": "90.5",
            "rating": "L",
            "published": False,
            "categories": [str(category_movie.id)],
            "genres": [str(nonexistent_genre_id)],
            "cast_members": [str(cast_member_actor.id)],
        }

        response: Any = api_client.post("/api/videos/", data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            "error": f"Genres with provided IDs not found: {nonexistent_genre_id}"
        }

    def test_create_video_with_nonexistent_cast_member(
        self,
        api_client: APIClient,
        category_movie: Category,
        genre_action: Genre,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
    ) -> None:
        category_repository.save(category_movie)
        genre_repository.save(genre_action)

        nonexistent_cast_member_id = uuid4()

        data: dict[str, Any] = {
            "title": "Test Video",
            "description": "A test video description",
            "launch_year": 2023,
            "duration": "90.5",
            "rating": "L",
            "published": False,
            "categories": [str(category_movie.id)],
            "genres": [str(genre_action.id)],
            "cast_members": [str(nonexistent_cast_member_id)],
        }

        response: Any = api_client.post("/api/videos/", data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            "error": (
                f"Cast members with provided IDs not found: {nonexistent_cast_member_id}"
            )
        }

    def test_create_video_with_invalid_rating(
        self,
        api_client: APIClient,
        category_movie: Category,
        genre_action: Genre,
        cast_member_actor: CastMember,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        category_repository.save(category_movie)
        genre_repository.save(genre_action)
        cast_member_repository.save(cast_member_actor)

        data: dict[str, Any] = {
            "title": "Test Video",
            "description": "A test video description",
            "launch_year": 2023,
            "duration": "90.5",
            "rating": "INVALID_RATING",
            "published": False,
            "categories": [str(category_movie.id)],
            "genres": [str(genre_action.id)],
            "cast_members": [str(cast_member_actor.id)],
        }

        response: Any = api_client.post("/api/videos/", data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
