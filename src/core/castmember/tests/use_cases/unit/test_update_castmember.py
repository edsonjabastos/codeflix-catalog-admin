from unittest.mock import create_autospec
from uuid import uuid4
import pytest
from core.castmember.application.exceptions import CastMemberNotFound, InvalidCastMember
from core.castmember.application.use_cases.update_castmember import UpdateCastMember
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository
from core.castmember.domain.value_objects import CastMemberType


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
def jane_castmember() -> CastMember:
    return CastMember(
        name="Jane Doe",
        type=CastMemberType.ACTOR,
    )


@pytest.fixture
def update_castmember_use_case(
    mock_castmember_repository: CastMemberRepository,
) -> UpdateCastMember:
    return UpdateCastMember(castmember_repository=mock_castmember_repository)


class TestUpdateCastMember:

    def test_update_castmember_with_valid_input(
        self,
        mock_castmember_repository: CastMemberRepository,
        jhon_castmember: CastMember,
        update_castmember_use_case: UpdateCastMember,
    ) -> None:
        mock_castmember_repository.get_by_id.return_value = jhon_castmember

        input: UpdateCastMember.Input = UpdateCastMember.Input(
            id=jhon_castmember.id,
            name="John Doe Jr.",
            type=CastMemberType.ACTOR,
        )
        update_castmember_use_case.execute(input=input)

        mock_castmember_repository.get_by_id.assert_called_once_with(
            id=jhon_castmember.id
        )
        assert jhon_castmember.name == "John Doe Jr."
        assert jhon_castmember.type == CastMemberType.ACTOR
        update_castmember_use_case.castmember_repository.update.assert_called_once()

    def test_update_castmember_with_invalid_input_name(
        self,
        mock_castmember_repository: CastMemberRepository,
        jhon_castmember: CastMember,
        update_castmember_use_case: UpdateCastMember,
    ) -> None:
        mock_castmember_repository.get_by_id.return_value = jhon_castmember

        input: UpdateCastMember.Input = UpdateCastMember.Input(
            id=jhon_castmember.id,
            name="",
            type=CastMemberType.ACTOR,
        )
        with pytest.raises(InvalidCastMember):
            update_castmember_use_case.execute(input=input)
        mock_castmember_repository.get_by_id.assert_called_once_with(jhon_castmember.id)
        mock_castmember_repository.save.assert_not_called()
        update_castmember_use_case.castmember_repository.update.assert_not_called()

    def test_update_castmember_with_invalid_input_type(
        self,
        mock_castmember_repository: CastMemberRepository,
        jhon_castmember: CastMember,
    ) -> None:
        mock_castmember_repository.get_by_id.return_value = jhon_castmember
        use_case: UpdateCastMember = UpdateCastMember(
            castmember_repository=mock_castmember_repository
        )
        input: UpdateCastMember.Input = UpdateCastMember.Input(
            id=jhon_castmember.id,
            name="John Doe Jr.",
            type="invalid",
        )
        with pytest.raises(InvalidCastMember):
            use_case.execute(input=input)
        mock_castmember_repository.get_by_id.assert_called_once_with(jhon_castmember.id)
        mock_castmember_repository.save.assert_not_called()

    def test_update_castmember_not_found(
        self,
        mock_castmember_repository: CastMemberRepository,
        update_castmember_use_case: UpdateCastMember,
    ) -> None:
        mock_castmember_repository.get_by_id.return_value = None
        input: UpdateCastMember.Input = UpdateCastMember.Input(
            id=uuid4(),
            name="John Doe Jr.",
            type=CastMemberType.ACTOR,
        )
        with pytest.raises(CastMemberNotFound):
            update_castmember_use_case.execute(input=input)
        mock_castmember_repository.get_by_id.assert_called_once_with(input.id)
        mock_castmember_repository.save.assert_not_called()
        update_castmember_use_case.castmember_repository.update.assert_not_called()
