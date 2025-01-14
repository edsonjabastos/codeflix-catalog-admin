from dataclasses import dataclass
from uuid import UUID

from core.castmember.application.exceptions import (
    CastMemberNotFound,
)
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository


class DeleteCastMember:
    def __init__(self, castmember_repository: CastMemberRepository) -> None:
        self.repository: CastMemberRepository = castmember_repository

    @dataclass
    class Input:
        id: UUID

    def execute(self, input: Input) -> None:
        castmember: CastMember = self.repository.get_by_id(input.id)

        if castmember is None:
            raise CastMemberNotFound(
                f"Not possible to delete castmember with id {input.id} because it was not found"
            )

        self.repository.delete(input.id)
