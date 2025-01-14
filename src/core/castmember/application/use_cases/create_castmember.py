from uuid import UUID
from dataclasses import dataclass
from core.castmember.application.exceptions import (
    InvalidCastMember,
)
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository


class CreateCastMember:
    def __init__(self, castmember_repository: CastMemberRepository) -> None:
        self.castmember_repository = castmember_repository

    @dataclass
    class Input:
        name: str
        type: str

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        try:
            castmember: CastMember = CastMember(name=input.name, type=input.type)
        except ValueError as error:
            raise InvalidCastMember(str(error))

        self.castmember_repository.save(castmember)

        return self.Output(id=castmember.id)
