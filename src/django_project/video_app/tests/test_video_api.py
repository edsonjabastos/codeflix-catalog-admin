import pytest
from typing import Any, Set
from uuid import UUID, uuid4
from decimal import Decimal
from rest_framework.test import APIClient
from core.video.domain.value_objects import Rating
from core.video.domain.video import Video
from core.category.domain.category import Category
from core.genre.domain.genre import Genre
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.value_objects import CastMemberType
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.repository import DjangoORMGenreRepository
from django_project.castmember_app.repository import DjangoORMCastMemberRepository
from django_project.video_app.repository import DjangoORMVideoRepository

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)


@pytest.fixture
def category_movie() -> Category:
    return Category(name="Movie", description="Movie category", is_active=True)


@pytest.fixture
def category_documentary() -> Category:
    return Category(name="Documentary", description="Documentary category", is_active=True)


@pytest.fixture
def genre_action() -> Genre:
    return Genre(name="Action", is_active=True, categories=set())


@pytest.fixture
def genre_drama() -> Genre:
    return Genre(name="Drama", is_active=True, categories=set())


@pytest.fixture
def cast_member_actor() -> CastMember:
    return CastMember(name="Actor Name", type=CastMemberType.ACTOR)


@pytest.fixture
def cast_member_director() -> CastMember:
    return CastMember(name="Director Name", type=CastMemberType.DIRECTOR)


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.fixture
def video_repository() -> DjangoORMVideoRepository:
    return DjangoORMVideoRepository()


@pytest.mark.django_db
class TestCreateVideoAPI:

    def test_create_video_with_valid_data(
        self,
        category_movie: Category,
        genre_action: Genre,
        cast_member_actor: CastMember,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
        cast_member_repository: DjangoORMCastMemberRepository,
        video_repository: DjangoORMVideoRepository,
    ) -> None:
        # Save related entities first
        category_repository.save(category_movie)
        genre_repository.save(genre_action)
        cast_member_repository.save(cast_member_actor)

        url: str = "/api/videos/"
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
        
        response: Any = APIClient().post(url, data=data)
        
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

    def test_create_video_with_invalid_data(self) -> None:
        url: str = "/api/videos/"
        data: dict[str, Any] = {
            # Missing required fields
            "title": "",
            "description": "",
        }
        
        response: Any = APIClient().post(url, data=data)
        
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_create_video_with_nonexistent_category(
        self,
        genre_action: Genre,
        cast_member_actor: CastMember,
        genre_repository: DjangoORMGenreRepository,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        # Save related entities except category
        genre_repository.save(genre_action)
        cast_member_repository.save(cast_member_actor)
        
        nonexistent_category_id = uuid4()
        
        url: str = "/api/videos/"
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
        
        response: Any = APIClient().post(url, data=data)
        
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_create_video_with_nonexistent_genre(
        self,
        category_movie: Category,
        cast_member_actor: CastMember,
        category_repository: DjangoORMCategoryRepository,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        # Save related entities except genre
        category_repository.save(category_movie)
        cast_member_repository.save(cast_member_actor)
        
        nonexistent_genre_id = uuid4()
        
        url: str = "/api/videos/"
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
        
        response: Any = APIClient().post(url, data=data)
        
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_create_video_with_nonexistent_cast_member(
        self,
        category_movie: Category,
        genre_action: Genre,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
    ) -> None:
        # Save related entities except cast member
        category_repository.save(category_movie)
        genre_repository.save(genre_action)
        
        nonexistent_cast_member_id = uuid4()
        
        url: str = "/api/videos/"
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
        
        response: Any = APIClient().post(url, data=data)
        
        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "error" in response.data

    def test_create_video_with_invalid_rating(
        self,
        category_movie: Category,
        genre_action: Genre,
        cast_member_actor: CastMember,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
        cast_member_repository: DjangoORMCastMemberRepository,
    ) -> None:
        # Save related entities
        category_repository.save(category_movie)
        genre_repository.save(genre_action)
        cast_member_repository.save(cast_member_actor)
        
        url: str = "/api/videos/"
        data: dict[str, Any] = {
            "title": "Test Video",
            "description": "A test video description",
            "launch_year": 2023,
            "duration": "90.5",
            "rating": "INVALID_RATING",  # Invalid rating value
            "published": False,
            "categories": [str(category_movie.id)],
            "genres": [str(genre_action.id)],
            "cast_members": [str(cast_member_actor.id)],
        }
        
        response: Any = APIClient().post(url, data=data)
        
        assert response.status_code == HTTP_400_BAD_REQUEST