import pytest
from core.castmember.application.exceptions import CastMemberNotFound, InvalidCastMember
from core.castmember.application.use_cases.update_castmember import UpdateCastMember
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
def update_castmember_use_case(
    castmember_repository: CastMemberRepository,
) -> UpdateCastMember:
    return UpdateCastMember(castmember_repository=castmember_repository)


@pytest.fixture
def jhon_castmember() -> CastMember:
    return CastMember(
        name="John Doe",
        type=CastMemberType.DIRECTOR,
    )


@pytest.fixture
def jane_castmember() -> CastMember:
    return CastMember(
        name="Jane Doe",
        type=CastMemberType.ACTOR,
    )


class TestUpdateCastMember:

    def test_update_castmember_with_valid_input(
        self,
        castmember_repository: CastMemberRepository,
        jhon_castmember: CastMember,
        update_castmember_use_case: UpdateCastMember,
    ) -> None:
        castmember_repository.save(jhon_castmember)

        input: UpdateCastMember.Input = UpdateCastMember.Input(
            id=jhon_castmember.id,
            name="John Doe Jr.",
            type=CastMemberType.ACTOR,
        )
        update_castmember_use_case.execute(input=input)

        updated_castmember = castmember_repository.get_by_id(jhon_castmember.id)

        assert updated_castmember.name == "John Doe Jr."
        assert updated_castmember.type == CastMemberType.ACTOR

    def test_update_castmember_with_invalid_input_name(
        self,
        castmember_repository: CastMemberRepository,
        jhon_castmember: CastMember,
        update_castmember_use_case: UpdateCastMember,
    ) -> None:
        castmember_repository.save(jhon_castmember)

        input: UpdateCastMember.Input = UpdateCastMember.Input(
            id=jhon_castmember.id,
            name="",
            type=CastMemberType.ACTOR,
        )

        with pytest.raises(InvalidCastMember, match="name cannot be empty"):
            update_castmember_use_case.execute(input=input)

    def test_update_castmember_with_invalid_input_type(
        self,
        castmember_repository: CastMemberRepository,
        jhon_castmember: CastMember,
        update_castmember_use_case: UpdateCastMember,
    ) -> None:
        castmember_repository.save(jhon_castmember)

        input: UpdateCastMember.Input = UpdateCastMember.Input(
            id=jhon_castmember.id,
            name="John Doe Jr.",
            type="INVALID",
        )

        with pytest.raises(InvalidCastMember, match="invalid type"):
            update_castmember_use_case.execute(input=input)

    def test_update_castmember_with_invalid_large_name(
        self,
        castmember_repository: CastMemberRepository,
        jhon_castmember: CastMember,
        update_castmember_use_case: UpdateCastMember,
    ) -> None:
        castmember_repository.save(jhon_castmember)

        input: UpdateCastMember.Input = UpdateCastMember.Input(
            id=jhon_castmember.id,
            name="a" * 256,
            type=CastMemberType.ACTOR,
        )

        with pytest.raises(
            InvalidCastMember, match="name cannot be longer than 255 characters"
        ):
            update_castmember_use_case.execute(input=input)

    def test_update_castmember_with_invalid_input_id(
        self,
        castmember_repository: CastMemberRepository,
        jhon_castmember: CastMember,
        update_castmember_use_case: UpdateCastMember,
    ) -> None:
        castmember_repository.save(jhon_castmember)

        invalid_id = "INVALID"
        input: UpdateCastMember.Input = UpdateCastMember.Input(
            id=invalid_id,
            name="John Doe Jr.",
            type=CastMemberType.ACTOR,
        )

        with pytest.raises(
            CastMemberNotFound, match=f"CastMember with id {invalid_id} not found"
        ):
            update_castmember_use_case.execute(input=input)
