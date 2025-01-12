from typing import Any, List

# from uuid import UUID, uuid4
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
