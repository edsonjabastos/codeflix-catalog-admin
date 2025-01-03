from typing import Any
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

from core.category.domain.category import Category
from django_project.category_app.repository import DjangoORMCategoryRepository


@pytest.fixture
def category_movie():
    return Category(
        name="Movie",
        description="Movie description",
    )


@pytest.fixture
def category_documentary():
    return Category(
        name="Documentary",
        description="Documentary description",
    )


@pytest.fixture
def category_repository() -> DjangoORMCategoryRepository:
    return DjangoORMCategoryRepository()


@pytest.mark.django_db
class TestCategoryListAPI:

    def test_list_categories(
        self,
        category_movie: Category,
        category_documentary: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)
        category_repository.save(category_documentary)

        url: str = "/api/categories/"
        response: Any = APIClient().get(url)

        expected_data = {
            "data": [
                {
                    "id": str(category_movie.id),
                    "name": category_movie.name,
                    "description": category_movie.description,
                    "is_active": category_movie.is_active,
                },
                {
                    "id": str(category_documentary.id),
                    "name": category_documentary.name,
                    "description": category_documentary.description,
                    "is_active": category_documentary.is_active,
                },
            ]
        }

        assert response.status_code == HTTP_200_OK
        assert len(response.data["data"]) == 2
        assert response.data == expected_data


@pytest.mark.django_db
class TestCategoryRetrieveAPI:

    def test_retrieve_category_bad_request(self) -> None:
        url: str = "/api/categories/123/"
        response: Any = APIClient().get(url)

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_retrieve_category_not_found(self) -> None:
        non_existent_id: UUID = uuid4()
        url: str = f"/api/categories/{non_existent_id}/"
        response: Any = APIClient().get(url)

        assert response.status_code == HTTP_404_NOT_FOUND

    def test_retrieve_category(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url: str = f"/api/categories/{category_movie.id}/"
        response: Any = APIClient().get(url)

        expected_data = {
            "data": {
                "id": str(category_movie.id),
                "name": category_movie.name,
                "description": category_movie.description,  # + " false positive test",
                "is_active": category_movie.is_active,
            }
        }

        assert response.status_code == HTTP_200_OK
        assert response.data == expected_data


@pytest.mark.django_db
class TestCategoryCreateAPI:

    def test_create_category_with_invalid_data(self) -> None:
        url: str = "/api/categories/"
        data: dict = {
            "name": "",
            "description": "Movie description",
        }
        response: Any = APIClient().post(url, data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_create_category(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        url: str = "/api/categories/"
        data: dict = {
            "name": category_movie.name,
            "description": category_movie.description,
        }
        response: Any = APIClient().post(url, data)

        assert response.status_code == HTTP_201_CREATED
        created_category_id: UUID = UUID(response.data["id"])

        assert category_repository.get_by_id(created_category_id) == Category(
            id=UUID(response.data["id"]),
            name=category_movie.name,
            description=category_movie.description,
            is_active=category_movie.is_active,
        )

        assert category_repository.list() == [
            Category(
                id=UUID(response.data["id"]),
                name=category_movie.name,
                description=category_movie.description,
                is_active=category_movie.is_active,
            )
        ]


@pytest.mark.django_db
class TestCategoryUpdateAPI:

    def test_update_category_with_invalid_data(self) -> None:
        url: str = "/api/categories/123/"
        data: dict = {
            "name": "",
            "description": "Movie description",
        }
        response: Any = APIClient().put(url, data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["This field may not be blank."],
            "id": ["Must be a valid UUID."],
            "is_active": ["This field is required."],
        }

    def test_update_category_bad_request(self) -> None:
        url: str = "/api/categories/123/"
        data: dict = {
            "id": "123",
            "name": "Movie",
            "description": "Movie description",
            "is_active": True,
        }
        response: Any = APIClient().put(url, data)

        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_update_category_not_found(self) -> None:
        non_existent_id: UUID = uuid4()
        url: str = f"/api/categories/{non_existent_id}/"
        data: dict = {
            "id": str(non_existent_id),
            "name": "Movie",
            "description": "Movie description",
            "is_active": True,
        }
        response: Any = APIClient().put(url, data)

        assert response.status_code == HTTP_404_NOT_FOUND

    def test_update_category(
        self,
        category_movie: Category,
        category_repository: DjangoORMCategoryRepository,
    ) -> None:
        category_repository.save(category_movie)

        url: str = f"/api/categories/{category_movie.id}/"
        data: dict = {
            "id": str(category_movie.id),
            "name": "Movie updated",
            "description": "Movie description updated",
            "is_active": False,
        }
        response: Any = APIClient().put(url, data)

        assert response.status_code == HTTP_204_NO_CONTENT

        assert category_repository.get_by_id(category_movie.id) == Category(
            id=category_movie.id,
            name="Movie updated",
            description="Movie description updated",
            is_active=False,
        )

        assert category_repository.list() == [
            Category(
                id=category_movie.id,
                name="Movie updated",
                description="Movie description updated",
                is_active=False,
            )
        ]
