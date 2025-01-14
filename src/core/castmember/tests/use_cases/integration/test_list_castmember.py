import pytest
from core.castmember.application.use_cases.list_castmember import (
    CastMemberOutput,
    ListCastMember,
)
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
def list_castmember_use_case(
    castmember_repository: CastMemberRepository,
) -> ListCastMember:
    return ListCastMember(castmember_repository=castmember_repository)


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


class TestListCastMember:

    def test_list_castmember(
        self,
        list_castmember_use_case: ListCastMember,
        jhon_castmember: CastMember,
        jane_castmember: CastMember,
    ) -> None:
        list_castmember_use_case.castmember_repository.save(jhon_castmember)
        list_castmember_use_case.castmember_repository.save(jane_castmember)

        input: ListCastMember.Input = ListCastMember.Input()

        output: ListCastMember.Output = list_castmember_use_case.execute(input=input)

        assert len(output.data) == 2
        assert output.data == [
            CastMemberOutput(
                id=jhon_castmember.id,
                name=jhon_castmember.name,
                type=jhon_castmember.type,
            ),
            CastMemberOutput(
                id=jane_castmember.id,
                name=jane_castmember.name,
                type=jane_castmember.type,
            ),
        ]

    def test_list_castmember_empty_list(
        self, list_castmember_use_case: ListCastMember
    ) -> None:
        input: ListCastMember.Input = ListCastMember.Input()

        output: ListCastMember.Output = list_castmember_use_case.execute(input=input)

        assert output.data == []
