from typing import Any, List

from uuid import UUID, uuid4
import pytest
from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
import pytest
from rest_framework.test import APIClient
from core.category.domain.category import Category
from core.genre.domain.genre import Genre
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.models import Genre as GenreModel
from django_project.genre_app.repository import DjangoORMGenreRepository


@pytest.fixture
def category_movie() -> Category:
    return Category(name="Movie", description="Movie category", is_active=True)


@pytest.fixture
def category_documentary() -> Category:
    return Category(
        name="Documentary", description="Documentary category", is_active=True
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.fixture
def genre_romance(category_movie: Category, category_documentary: Category) -> Genre:
    return Genre(
        name="Romance",
        is_active=True,
        categories={category_movie.id, category_documentary.id},
    )


@pytest.fixture
def genre_drama() -> Genre:
    return Genre(name="Drama", is_active=True, categories=set())


@pytest.fixture
def genre_repository() -> DjangoORMGenreRepository:
    return DjangoORMGenreRepository()


@pytest.mark.django_db
class TestListAPI:

    def test_list_genres_and_categories(
        self,
        genre_romance: Genre,
        genre_drama: Genre,
        genre_repository: DjangoORMGenreRepository,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)
        genre_repository.save(genre_drama)

        url: str = "/api/genres/"
        response: Any = APIClient().get(url)

        # expected_response: dict[str, List[dict[str, Any]]] = {
        #     "data": [
        #         {
        #             "id": str(genre_romance.id),
        #             "name": "Romance",
        #             "is_active": True,
        #             "categories": [
        #                 str(category_movie.id),
        #                 str(category_documentary.id),
        #             ],
        #         },
        #         {
        #             "id": str(genre_drama.id),
        #             "name": "Drama",
        #             "is_active": True,
        #             "categories": [],
        #         },
        #     ]
        # }

        assert response.status_code == HTTP_200_OK
        # assert response.data == expected_response

        assert response.data["data"]
        assert len(response.data["data"]) == 2

        assert response.data["data"][0]["id"] == str(genre_romance.id)
        assert response.data["data"][0]["name"] == "Romance"
        assert response.data["data"][0]["is_active"] is True
        assert set(response.data["data"][0]["categories"]) == {
            str(category_documentary.id),
            str(category_movie.id),
        }
        assert response.data["data"][1]["id"] == str(genre_drama.id)
        assert response.data["data"][1]["name"] == "Drama"
        assert response.data["data"][1]["is_active"] is True
        assert response.data["data"][1]["categories"] == []


@pytest.mark.django_db
class TestCreateAPI:

    def test_create_genre(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url: str = "/api/genres/"
        data: dict[str, Any] = {
            "name": "Romance",
            "is_active": True,
            "categories": [str(category_movie.id), str(category_documentary.id)],
        }
        response: Any = APIClient().post(url, data=data)

        assert response.status_code == HTTP_201_CREATED
        assert response.data["id"]

        created_genre_id: str = response.data["id"]
        created_genre: GenreModel = genre_repository.get_by_id(created_genre_id)

        assert created_genre.name == "Romance"
        assert created_genre.is_active is True
        assert created_genre.categories == {
            category_movie.id,
            category_documentary.id,
        }

    def test_create_genre_with_invalid_category(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        non_registered_category_id: str = uuid4()

        url: str = "/api/genres/"
        data: dict[str, Any] = {
            "name": "Romance",
            "is_active": True,
            "categories": [str(category_movie.id), str(non_registered_category_id)],
        }
        response: Any = APIClient().post(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            "error": f"Categories with provided IDs not found: {non_registered_category_id}"
        }

    def test_create_genre_with_invalid_empty_name(
        self, category_movie: Category, category_repository: DjangoORMCategoryRepository
    ) -> None:
        category_repository.save(category_movie)

        url: str = "/api/genres/"
        data: dict[str, Any] = {
            "name": "",
            "is_active": True,
            "categories": [str(category_movie.id)],
        }
        response: Any = APIClient().post(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        # assert response.data == {"error": "name cannot be empty"}
        assert response.data == {"name": ["This field may not be blank."]}

    def test_create_genre_with_invalid_large_name(
        self, category_movie: Category, category_repository: DjangoORMCategoryRepository
    ) -> None:
        category_repository.save(category_movie)

        url: str = "/api/genres/"
        data: dict[str, Any] = {
            "name": "a" * 256,
            "is_active": True,
            "categories": [str(category_movie.id)],
        }
        response: Any = APIClient().post(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        # assert response.data == {"error": "name cannot be larger than 255 characters"}
        assert response.data == {
            "name": ["Ensure this field has no more than 255 characters."]
        }

    def test_create_genre_with_invalid_uuid_category(
        self, category_movie: Category, category_repository: DjangoORMCategoryRepository
    ) -> None:
        category_repository.save(category_movie)

        url: str = "/api/genres/"
        data: dict[str, Any] = {
            "name": "Romance",
            "is_active": True,
            "categories": ["invalid_uuid"],
        }
        response: Any = APIClient().post(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {"categories": {0: ["Must be a valid UUID."]}}


@pytest.mark.django_db
class TestDeleteAPI:

    def test_delete_genre(
        self,
        genre_romance: Genre,
        genre_repository: DjangoORMGenreRepository,
    ) -> None:
        genre_repository.save(genre_romance)

        url: str = f"/api/genres/{genre_romance.id}/"
        response: Any = APIClient().delete(url)

        assert response.status_code == HTTP_204_NO_CONTENT
        assert response.data is None
        assert genre_repository.get_by_id(genre_romance.id) is None

    def test_delete_genre_not_found(self) -> None:
        url: str = f"/api/genres/{uuid4()}/"
        response: Any = APIClient().delete(url)

        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.data is None

    def test_delete_genre_with_invalid_uuid(self) -> None:
        url: str = "/api/genres/invalid_uuid/"
        response: Any = APIClient().delete(url)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {"id": ["Must be a valid UUID."]}


@pytest.mark.django_db
class TestUpdateAPI:
    def test_when_request_data_is_valid_then_update_genre(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Drama",
            "is_active": True,
            "categories": [category_documentary.id],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == HTTP_204_NO_CONTENT
        updated_genre = genre_repository.get_by_id(genre_romance.id)
        assert updated_genre.name == "Drama"
        assert updated_genre.is_active is True
        assert updated_genre.categories == {category_documentary.id}

    def test_when_request_data_is_invalid_then_return_400(
        self,
        genre_drama: Genre,
    ) -> None:
        url = f"/api/genres/{str(genre_drama.id)}/"
        data = {
            "name": "",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_related_categories_do_not_exist_then_return_400(
        self,
        category_repository: DjangoORMCategoryRepository,
        category_movie: Category,
        category_documentary: Category,
        genre_repository: DjangoORMGenreRepository,
        genre_romance: Genre,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)
        genre_repository.save(genre_romance)

        url = f"/api/genres/{str(genre_romance.id)}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [uuid4()],  # non-existent category
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert "Categories with provided IDs not found" in response.data["error"]

    def test_when_genre_does_not_exist_then_return_404(self) -> None:
        url = f"/api/genres/{str(uuid4())}/"
        data = {
            "name": "Romance",
            "is_active": True,
            "categories": [],
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == HTTP_404_NOT_FOUND
