from typing import List
from uuid import UUID
from dataclasses import dataclass

from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository


@dataclass
class CastMemberOutput:
    id: UUID
    name: str
    type: str


class ListCastMember:
    def __init__(self, castmember_repository: CastMemberRepository) -> None:
        self.castmember_repository = castmember_repository

    @dataclass
    class Input: ...

    @dataclass
    class Output:
        data: List[CastMemberOutput]

    def execute(self, input: Input) -> Output:
        castmembers: List[CastMember] = self.castmember_repository.list()
        return self.Output(
            data=[
                CastMemberOutput(
                    id=castmember.id,
                    name=castmember.name,
                    type=castmember.type,
                )
                for castmember in castmembers
            ]
        )
