from calendar import c
from typing import Any
from uuid import UUID, uuid4
import pytest
from rest_framework.test import APIClient
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_201_CREATED,
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
