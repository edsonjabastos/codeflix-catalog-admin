import pytest

from core.castmember.domain.castmember import CastMember
from core.castmember.domain.value_objects import CastMemberType
from django_project.adapters.persistence.django.castmember_repository import (
    DjangoORMCastMemberRepository,
)


@pytest.fixture
def chris_castmember() -> CastMember:
    return CastMember(name="Christopher Nolan", type=CastMemberType.DIRECTOR)


@pytest.fixture
def pedro_castmember() -> CastMember:
    return CastMember(name="Pedro Pascal", type=CastMemberType.ACTOR)


@pytest.fixture
def cast_member_actor() -> CastMember:
    return CastMember(name="Actor Name", type=CastMemberType.ACTOR)


@pytest.fixture
def cast_member_director() -> CastMember:
    return CastMember(name="Director Name", type=CastMemberType.DIRECTOR)


@pytest.fixture
def castmember_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()


@pytest.fixture
def cast_member_repository() -> DjangoORMCastMemberRepository:
    return DjangoORMCastMemberRepository()
