from unittest.mock import create_autospec
from uuid import uuid4
import pytest
from core.castmember.application.use_cases.list_castmember import (
    CastMemberOutput,
    ListCastMember,
)
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository
from core.castmember.domain.value_objects import CastMemberType


@pytest.fixture
def mock_castmember_repository() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)


@pytest.fixture
def jhon_castmember() -> CastMember:
    return CastMember(
        id=uuid4(),
        name="John Doe",
        type=CastMemberType.DIRECTOR,
    )


@pytest.fixture
def jane_castmember() -> CastMember:
    return CastMember(
        id=uuid4(),
        name="Jane Doe",
        type=CastMemberType.ACTOR,
    )


class TestListCastMember:

    def test_list_castmember(
        self,
        mock_castmember_repository: CastMemberRepository,
        jhon_castmember: CastMember,
        jane_castmember: CastMember,
    ) -> None:
        mock_castmember_repository.list.return_value = [
            jhon_castmember,
            jane_castmember,
        ]
        use_case: ListCastMember = ListCastMember(
            castmember_repository=mock_castmember_repository
        )
        input: ListCastMember.Input = ListCastMember.Input()
        output: ListCastMember.Output = use_case.execute(input=input)

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
        mock_castmember_repository.list.assert_called_once()

    def test_list_castmember_with_empty_list(
        self,
        mock_castmember_repository: CastMemberRepository,
    ) -> None:
        mock_castmember_repository.list.return_value = []
        use_case: ListCastMember = ListCastMember(
            castmember_repository=mock_castmember_repository
        )
        input: ListCastMember.Input = ListCastMember.Input()
        output: ListCastMember.Output = use_case.execute(input=input)

        assert output.data == []
        mock_castmember_repository.list.assert_called_once()
