from unittest.mock import create_autospec
import pytest

from core.castmember.application.exceptions import CastMemberNotFound
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository
from core.castmember.domain.value_objects import CastMemberType
from core.castmember.application.use_cases.delete_castmember import DeleteCastMember


@pytest.fixture
def mock_castmember_repository() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)


@pytest.fixture
def jhon_castmember() -> CastMember:
    return CastMember(
        name="John Doe",
        type=CastMemberType.DIRECTOR,
    )


@pytest.fixture
def delete_castmember_use_case(
    mock_castmember_repository: CastMemberRepository,
) -> DeleteCastMember:
    return DeleteCastMember(castmember_repository=mock_castmember_repository)


class TestDeleteCastMember:

    def test_delete_castmember(
        self,
        mock_castmember_repository: CastMemberRepository,
        jhon_castmember: CastMember,
        delete_castmember_use_case: DeleteCastMember,
    ) -> None:
        mock_castmember_repository.get_by_id.return_value = jhon_castmember

        input: DeleteCastMember.Input = DeleteCastMember.Input(
            id=jhon_castmember.id,
        )
        delete_castmember_use_case.execute(input=input)

        mock_castmember_repository.get_by_id.assert_called_once_with(
            id=jhon_castmember.id
        )
        mock_castmember_repository.delete.assert_called_once_with(id=jhon_castmember.id)

    def test_delete_castmember_with_invalid_input(
        self,
        mock_castmember_repository: CastMemberRepository,
        jhon_castmember: CastMember,
        delete_castmember_use_case: DeleteCastMember,
    ) -> None:
        mock_castmember_repository.get_by_id.return_value = None

        input: DeleteCastMember.Input = DeleteCastMember.Input(
            id=jhon_castmember.id,
        )
        with pytest.raises(
            CastMemberNotFound,
            match=f"Not possible to delete castmember with id {jhon_castmember.id} because it was not found",
        ):
            delete_castmember_use_case.execute(input=input)

        mock_castmember_repository.get_by_id.assert_called_once_with(
            id=jhon_castmember.id
        )
        mock_castmember_repository.delete.assert_not_called()
