import pytest
from unittest.mock import patch
from uuid import uuid4, UUID
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.value_objects import CastMemberType


class TestCastMember:

    def test_name_is_required(self) -> None:
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'name'"
        ):
            CastMember(type=CastMemberType.ACTOR)

    def test_name_cant_be_empty(self) -> None:
        with pytest.raises(ValueError, match="name cannot be empty"):
            CastMember("", type=CastMemberType.ACTOR)

    def test_name_must_have_less_than_255_characters(self) -> None:
        with pytest.raises(
            ValueError, match="name cannot be longer than 255 characters"
        ):
            CastMember("a" * 256, type=CastMemberType.ACTOR)

    def test_type_is_required(self) -> None:
        with pytest.raises(
            TypeError, match="missing 1 required positional argument: 'type'"
        ):
            CastMember(name="John Doe")

    def test_name_and_type_are_required(self) -> None:
        with pytest.raises(
            TypeError,
            match="missing 2 required positional arguments: 'name' and 'type'",
        ):
            CastMember()

    def test_type_must_be_valid(self) -> None:
        with pytest.raises(ValueError, match="invalid type"):
            CastMember(name="John Doe", type="INVALID")

    def test_create_ast_member_with_id(self) -> None:
        cast_member_id = uuid4()
        cast_member = CastMember(
            id=cast_member_id, name="John Doe", type=CastMemberType.ACTOR
        )

        assert cast_member.id == cast_member_id
        assert cast_member.name == "John Doe"
        assert cast_member.type == CastMemberType.ACTOR


class TestUpdateCastMember:

    def test_update_name(self) -> None:
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        cast_member.update(name="Jane Doe", type=CastMemberType.ACTOR)

        assert cast_member.name == "Jane Doe"
        assert cast_member.type == CastMemberType.ACTOR

    def test_update_type(self) -> None:
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        cast_member.update(name="John Doe", type=CastMemberType.DIRECTOR)

        assert cast_member.name == "John Doe"
        assert cast_member.type == CastMemberType.DIRECTOR

    def test_update_name_and_type(self) -> None:
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        cast_member.update(name="Jane Doe", type=CastMemberType.DIRECTOR)

        assert cast_member.name == "Jane Doe"
        assert cast_member.type == CastMemberType.DIRECTOR

    def test_update_name_and_type_with_invalid_type(self) -> None:
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)

        with pytest.raises(ValueError, match="invalid type"):
            cast_member.update(name="Jane Doe", type="INVALID")

        # assert cast_member.name == "John Doe" # its incorrect to do this?
        # assert cast_member.type == CastMemberType.ACTOR


class TestCastMemberStr:

    def test_cast_member_str(self) -> None:
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)

        assert str(cast_member) == "John Doe - ACTOR"

    def test_cast_member_str_with_director(self) -> None:
        cast_member = CastMember(name="John Doe", type=CastMemberType.DIRECTOR)

        assert str(cast_member) == "John Doe - DIRECTOR"


class TestCastMemberRepr:

    def test_cast_member_repr(self) -> None:
        cast_member_id = uuid4()
        cast_member = CastMember(
            id=cast_member_id, name="John Doe", type=CastMemberType.ACTOR
        )

        assert repr(cast_member) == f"<CastMember John Doe ({cast_member_id})>"

    def test_cast_member_repr_with_director(self) -> None:
        cast_member_id = uuid4()
        cast_member = CastMember(
            id=cast_member_id, name="John Doe", type=CastMemberType.DIRECTOR
        )

        assert repr(cast_member) == f"<CastMember John Doe ({cast_member_id})>"


class TestCastMemberEq:

    def test_cast_member_eq(self) -> None:
        cast_member_id = uuid4()
        cast_member = CastMember(
            id=cast_member_id, name="John Doe", type=CastMemberType.ACTOR
        )

        other_cast_member = CastMember(
            id=cast_member_id, name="Jane Doe", type=CastMemberType.ACTOR
        )

        assert cast_member == other_cast_member

    def test_cast_member_eq_with_different_ids(self) -> None:
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        other_cast_member = CastMember(name="Jane Doe", type=CastMemberType.ACTOR)

        assert cast_member != other_cast_member

    def test_cast_member_eq_with_different_ids_and_types(self) -> None:
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)
        other_cast_member = CastMember(name="Jane Doe", type=CastMemberType.DIRECTOR)

        assert cast_member != other_cast_member

    def test_cast_member_eq_with_same_object(self) -> None:
        cast_member = CastMember(name="John Doe", type=CastMemberType.ACTOR)

        assert cast_member == cast_member
