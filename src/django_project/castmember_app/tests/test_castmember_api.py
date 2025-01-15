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
import pytest
from rest_framework.test import APIClient
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.value_objects import CastMemberType
from django_project.castmember_app.repository import DjangoORMCastMemberRepository
from django_project.castmember_app.models import CastMember as CastMemberORM


@pytest.fixture
def chris_castmember() -> CastMember:
    return CastMember(name="Christopher Nolan", type=CastMemberType.DIRECTOR)


@pytest.fixture
def pedro_castmember() -> CastMember:
    return CastMember(name="Pedro Pascal", type=CastMemberType.ACTOR)


@pytest.fixture
def castmember_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.mark.django_db
class TestListAPI:

    def test_list_castmember(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
        pedro_castmember: CastMember,
        chris_castmember: CastMember,
    ) -> None:
        castmember_repository.save(pedro_castmember)
        castmember_repository.save(chris_castmember)

        url: str = "/api/cast_members/"
        response: Any = APIClient().get(url)

        # expected_response: dict[str, List[dict[str, Any]]] = {
        #     "data": [
        #         {
        #             "id": str(castmember_romance.id),
        #             "name": "Romance",
        #             "is_active": True,
        #             "categories": [
        #                 str(castmember_movie.id),
        #                 str(castmember_documentary.id),
        #             ],
        #         },
        #         {
        #             "id": str(castmember_drama.id),
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

        assert response.data["data"][0]["id"] == str(pedro_castmember.id)
        assert response.data["data"][0]["name"] == "Pedro Pascal"
        assert response.data["data"][0]["type"] == "ACTOR"
        assert response.data["data"][1]["id"] == str(chris_castmember.id)
        assert response.data["data"][1]["name"] == "Christopher Nolan"
        assert response.data["data"][1]["type"] == "DIRECTOR"


@pytest.mark.django_db
class TestCreateAPI:

    def test_create_castmember_actor(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
    ) -> None:

        url: str = "/api/cast_members/"
        data: dict[str, Any] = {
            "name": "Pedro Pascal",
            "type": "ACTOR",
        }

        response: Any = APIClient().post(url, data=data)

        assert response.status_code == HTTP_201_CREATED
        assert response.data["id"]

        created_castmember_id: str = response.data["id"]
        created_castmember: CastMemberORM = castmember_repository.get_by_id(
            created_castmember_id
        )

        assert created_castmember.name == "Pedro Pascal"
        assert created_castmember.type == CastMemberType.ACTOR
        assert created_castmember.id == UUID(created_castmember_id)

    def test_create_castmember_director(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
    ) -> None:

        url: str = "/api/cast_members/"
        data: dict[str, Any] = {
            "name": "Christopher Nolan",
            "type": "DIRECTOR",
        }

        response: Any = APIClient().post(url, data=data)

        assert response.status_code == HTTP_201_CREATED
        assert response.data["id"]

        created_castmember_id: str = response.data["id"]
        created_castmember: CastMemberORM = castmember_repository.get_by_id(
            created_castmember_id
        )

        assert created_castmember.name == "Christopher Nolan"
        assert created_castmember.type == CastMemberType.DIRECTOR
        assert created_castmember.id == UUID(created_castmember_id)

    def test_create_castmember_with_invalid_empty_name(
        self,
    ) -> None:

        url: str = "/api/cast_members/"
        data: dict[str, Any] = {
            "name": "",
            "type": "ACTOR",
        }
        response: Any = APIClient().post(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        # assert response.data == {"error": "name cannot be empty"}
        assert response.data == {"name": ["This field may not be blank."]}

    def test_create_castmember_with_invalid_large_name(
        self,
    ) -> None:

        url: str = "/api/cast_members/"
        data: dict[str, Any] = {
            "name": "a" * 256,
            "type": "ACTOR",
        }
        response: Any = APIClient().post(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        # assert response.data == {"error": "name cannot be larger than 255 characters"}
        assert response.data == {
            "name": ["Ensure this field has no more than 255 characters."]
        }

    def test_create_castmember_with_invalid_type(
        self,
    ) -> None:
        invalid_type: str = "INVALID_TYPE"
        url: str = "/api/cast_members/"
        data: dict[str, Any] = {
            "name": "Pedro Pascal",
            "type": invalid_type,
        }
        response: Any = APIClient().post(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {"type": [f'"{invalid_type}" is not a valid choice.']}


@pytest.mark.django_db
class TestDeleteAPI:

    def test_delete_castmember(
        self,
        pedro_castmember: CastMember,
        castmember_repository: DjangoORMCastMemberRepository,
    ) -> None:
        castmember_repository.save(pedro_castmember)

        url: str = f"/api/cast_members/{pedro_castmember.id}/"
        response: Any = APIClient().delete(url)

        assert response.status_code == HTTP_204_NO_CONTENT
        assert response.data is None
        assert castmember_repository.get_by_id(pedro_castmember.id) is None

    def test_delete_castmember_not_found(self) -> None:
        url: str = f"/api/cast_members/{uuid4()}/"
        response: Any = APIClient().delete(url)

        assert response.status_code == HTTP_404_NOT_FOUND
        assert response.data is None

    def test_delete_castmember_with_invalid_uuid(self) -> None:
        url: str = "/api/cast_members/invalid_uuid/"
        response: Any = APIClient().delete(url)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {"id": ["Must be a valid UUID."]}


@pytest.mark.django_db
class TestUpdateAPI:

    def test_when_request_data_is_valid_then_update_castmember(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
        pedro_castmember: CastMember,
    ) -> None:
        castmember_repository.save(pedro_castmember)

        url = f"/api/cast_members/{pedro_castmember.id}/"
        data = {
            "name": "Pedro Delphi",
            "type": "ACTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == HTTP_204_NO_CONTENT
        updated_castmember = castmember_repository.get_by_id(pedro_castmember.id)
        assert updated_castmember.name == "Pedro Delphi"
        assert updated_castmember.type == CastMemberType.ACTOR

    def test_when_empty_name_invalid_then_return_400(
        self,
        pedro_castmember: CastMember,
        castmember_repository: DjangoORMCastMemberRepository,
    ) -> None:
        castmember_repository.save(pedro_castmember)
        url = f"/api/cast_members/{pedro_castmember.id}/"
        data = {
            "name": "",
            "type": "ACTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {"name": ["This field may not be blank."]}

    def test_when_large_name_invalid_then_return_400(
        self,
        pedro_castmember: CastMember,
        castmember_repository: DjangoORMCastMemberRepository,
    ) -> None:
        castmember_repository.save(pedro_castmember)
        url = f"/api/cast_members/{pedro_castmember.id}/"
        data = {
            "name": "a" * 256,
            "type": "ACTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {
            "name": ["Ensure this field has no more than 255 characters."]
        }

    def test_when_invalid_type_then_return_400(
        self,
        castmember_repository: DjangoORMCastMemberRepository,
        pedro_castmember: CastMember,
    ) -> None:
        castmember_repository.save(pedro_castmember)

        invalid_type: str = "INVALID_TYPE"
        url = f"/api/cast_members/{pedro_castmember.id}/"
        data = {
            "name": "Romance",
            "type": invalid_type,
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == HTTP_400_BAD_REQUEST
        assert response.data == {"type": [f'"{invalid_type}" is not a valid choice.']}

    def test_when_castmember_does_not_exist_then_return_404(self) -> None:
        url = f"/api/cast_members/{uuid4()}/"
        data = {
            "name": "John Travolta",
            "type": "ACTOR",
        }
        response = APIClient().put(url, data=data)

        assert response.status_code == HTTP_404_NOT_FOUND
