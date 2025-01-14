from uuid import UUID, uuid4

import pytest

from core.castmember.application.use_cases.create_castmember import CreateCastMember
from core.castmember.application.exceptions import InvalidCastMember
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository
from core.castmember.domain.value_objects import CastMemberType
from core.castmember.infra.in_memory_castmember_repository import (
    InMemoryCastMemberRepository,
)


@pytest.fixture
def castmember_repository() -> CastMemberRepository:
    return InMemoryCastMemberRepository()


@pytest.fixture
def create_castmember_use_case(
    castmember_repository: CastMemberRepository,
) -> CreateCastMember:
    return CreateCastMember(castmember_repository=castmember_repository)


class TestCreateCastMember:

    def test_create_castmember_with_valid_input(
        self,
        create_castmember_use_case: CreateCastMember,
        castmember_repository: CastMemberRepository,
    ) -> None:
        input: CreateCastMember.Input = CreateCastMember.Input(
            name="John Doe",
            type=CastMemberType.DIRECTOR,
        )

        created_castmember_output: CreateCastMember.Output = (
            create_castmember_use_case.execute(input=input)
        )

        assert isinstance(created_castmember_output.id, UUID)
        created_castmember: CastMember = castmember_repository.get_by_id(
            created_castmember_output.id
        )
        assert created_castmember.name == "John Doe"
        assert created_castmember.type == CastMemberType.DIRECTOR
        assert castmember_repository.list() == [created_castmember]

    def test_create_castmember_with_invalid_input_name(
        self,
        create_castmember_use_case: CreateCastMember,
        castmember_repository: CastMemberRepository,
    ) -> None:
        input: CreateCastMember.Input = CreateCastMember.Input(
            name="",
            type=CastMemberType.DIRECTOR,
        )

        with pytest.raises(InvalidCastMember) as exc_info:
            create_castmember_use_case.execute(input=input)

        assert str(exc_info.value) == "name cannot be empty"
        assert castmember_repository.list() == []

    def test_create_castmember_with_invalid_input_type(
        self,
        create_castmember_use_case: CreateCastMember,
        castmember_repository: CastMemberRepository,
    ) -> None:
        input: CreateCastMember.Input = CreateCastMember.Input(
            name="John Doe",
            type="invalid",
        )

        with pytest.raises(InvalidCastMember) as exc_info:
            create_castmember_use_case.execute(input=input)

        assert str(exc_info.value) == "invalid type"
        assert castmember_repository.list() == []
