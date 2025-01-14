from dataclasses import dataclass
from uuid import UUID

from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository
from core.castmember.application.exceptions import (
    CastMemberNotFound,
    InvalidCastMember,
)


class UpdateCastMember:
    def __init__(self, castmember_repository: CastMemberRepository) -> None:
        self.castmember_repository = castmember_repository

    @dataclass
    class Input:
        id: UUID
        name: str
        type: str

    def execute(self, input: Input) -> None:
        castmember: CastMember = self.castmember_repository.get_by_id(id=input.id)
        if not castmember:
            raise CastMemberNotFound(f"CastMember with id {input.id} not found")

        try:
            castmember.update(name=input.name, type=input.type)
        except ValueError as error:
            raise InvalidCastMember(str(error))

        self.castmember_repository.update(castmember)

        return None
