import pytest

from core.castmember.application.exceptions import CastMemberNotFound
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository
from core.castmember.domain.value_objects import CastMemberType
from core.castmember.application.use_cases.delete_castmember import DeleteCastMember
from core.castmember.infra.in_memory_castmember_repository import (
    InMemoryCastMemberRepository,
)


@pytest.fixture
def castmember_repository() -> CastMemberRepository:
    return InMemoryCastMemberRepository()


@pytest.fixture
def jhon_castmember() -> CastMember:
    return CastMember(
        name="John Doe",
        type=CastMemberType.DIRECTOR,
    )


@pytest.fixture
def delete_castmember_use_case(
    castmember_repository: CastMemberRepository,
) -> DeleteCastMember:
    return DeleteCastMember(castmember_repository=castmember_repository)


class TestDeleteCastMember:

    def test_delete_castmember(
        self,
        castmember_repository: CastMemberRepository,
        jhon_castmember: CastMember,
        delete_castmember_use_case: DeleteCastMember,
    ) -> None:
        castmember_repository.save(jhon_castmember)

        input: DeleteCastMember.Input = DeleteCastMember.Input(
            id=jhon_castmember.id,
        )
        delete_castmember_use_case.execute(input=input)

        deleted_castmember = castmember_repository.get_by_id(jhon_castmember.id)

        assert deleted_castmember is None
        assert len(castmember_repository.list()) == 0

    def test_delete_castmember_with_invalid_input(
        self,
        castmember_repository: CastMemberRepository,
        jhon_castmember: CastMember,
        delete_castmember_use_case: DeleteCastMember,
    ) -> None:
        castmember_repository.save(jhon_castmember)
        assert len(castmember_repository.list()) == 1

        input: DeleteCastMember.Input = DeleteCastMember.Input(
            id="invalid-id",
        )

        with pytest.raises(CastMemberNotFound):
            delete_castmember_use_case.execute(input=input)

        assert len(castmember_repository.list()) == 1
        assert castmember_repository.get_by_id(jhon_castmember.id) == jhon_castmember
