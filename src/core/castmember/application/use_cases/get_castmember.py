from dataclasses import dataclass
from uuid import UUID

from core.castmember.application.exceptions import CastMemberNotFound
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository
from core.castmember.domain.value_objects import CastMemberType


class GetCastMember:
    def __init__(self, castmember_repository: CastMemberRepository) -> None:
        self.repository: CastMemberRepository = castmember_repository

    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        id: UUID
        name: str
        type: CastMemberType

    def execute(self, input: Input) -> Output:
        castmember: CastMember = self.repository.get_by_id(input.id)

        if castmember is None:
            raise CastMemberNotFound(f"Cast member with id {input.id} not found")

        return GetCastMember.Output(
            id=castmember.id,
            name=castmember.name,
            type=castmember.type,
        )
