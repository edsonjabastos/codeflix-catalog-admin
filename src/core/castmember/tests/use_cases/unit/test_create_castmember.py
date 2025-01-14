import pytest
from unittest.mock import create_autospec
from uuid import UUID
from core.castmember.application.exceptions import InvalidCastMember
from core.castmember.application.use_cases.create_castmember import (
    CreateCastMember,
)
from core.castmember.domain.castmember_repository import CastMemberRepository
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.value_objects import CastMemberType


@pytest.fixture
def mock_castmember_repository() -> CastMemberRepository:
    return create_autospec(CastMemberRepository)


@pytest.fixture
def create_castmember_use_case(
    mock_castmember_repository: CastMemberRepository,
) -> CreateCastMember:
    return CreateCastMember(castmember_repository=mock_castmember_repository)


class TestCreateCastMember:

    def test_create_castmember_with_valid_input(
        self,
        create_castmember_use_case: CreateCastMember,
        mock_castmember_repository: CastMemberRepository,
    ) -> None:
        input: CreateCastMember.Input = CreateCastMember.Input(
            name="John Doe",
            type=CastMemberType.DIRECTOR,
        )

        created_castmember_output: CreateCastMember.Output = (
            create_castmember_use_case.execute(input=input)
        )

        assert isinstance(created_castmember_output.id, UUID)
        mock_castmember_repository.save.assert_called_once()
        mock_castmember_repository.save.assert_called_with(
            CastMember(
                id=created_castmember_output.id,
                name="John Doe",
                type=CastMemberType.DIRECTOR,
            )
        )
        create_castmember_use_case.castmember_repository.save.assert_called_once()

    def test_create_castmember_with_invalid_input_name(
        self,
        create_castmember_use_case: CreateCastMember,
        mock_castmember_repository: CastMemberRepository,
    ) -> None:
        input: CreateCastMember.Input = CreateCastMember.Input(
            name="",
            type=CastMemberType.DIRECTOR,
        )

        with pytest.raises(InvalidCastMember, match="name cannot be empty"):
            create_castmember_use_case.execute(input=input)
        mock_castmember_repository.save.assert_not_called()
        create_castmember_use_case.castmember_repository.save.assert_not_called()

    def test_create_castmember_with_invalid_input_type(
        self,
        create_castmember_use_case: CreateCastMember,
        mock_castmember_repository: CastMemberRepository,
    ) -> None:
        input: CreateCastMember.Input = CreateCastMember.Input(
            name="John Doe",
            type="invalid_type",
        )

        with pytest.raises(InvalidCastMember, match="invalid type"):
            create_castmember_use_case.execute(input=input)
        mock_castmember_repository.save.assert_not_called()
        create_castmember_use_case.castmember_repository.save.assert_not_called()

    def test_create_castmember_with_invalid_input_name_and_type(
        self,
        create_castmember_use_case: CreateCastMember,
        mock_castmember_repository: CastMemberRepository,
    ) -> None:
        input: CreateCastMember.Input = CreateCastMember.Input(
            name="",
            type="invalid_type",
        )

        with pytest.raises(InvalidCastMember, match="name cannot be empty"):
            create_castmember_use_case.execute(input=input)
        mock_castmember_repository.save.assert_not_called()
        create_castmember_use_case.castmember_repository.save.assert_not_called()

    def test_create_castmember_with_invalid_empty_input(
        self,
        create_castmember_use_case: CreateCastMember,
        mock_castmember_repository: CastMemberRepository,
    ) -> None:

        with pytest.raises(
            TypeError,
            match="missing 2 required positional arguments: 'name' and 'type'",
        ):
            input: CreateCastMember.Input = CreateCastMember.Input()
            create_castmember_use_case.execute(input=input)
        mock_castmember_repository.save.assert_not_called()
        create_castmember_use_case.castmember_repository.save.assert_not_called()
