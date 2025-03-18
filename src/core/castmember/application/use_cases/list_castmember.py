from typing import List
from uuid import UUID
from dataclasses import dataclass

from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository


class ListCastMember:
    def __init__(self, castmember_repository: CastMemberRepository) -> None:
        self.castmember_repository = castmember_repository

    @dataclass
    class Input:
        order_by: str = "name"
        current_page: int = 1

    @dataclass
    class Output:
        id: UUID
        name: str
        type: str

    @dataclass
    class OutputMeta:
        current_page: int
        per_page: int
        total: int

    @dataclass
    class ListOutput:
        data: List["ListCastMember.Output"]
        meta: "ListCastMember.OutputMeta"

    def execute(self, input: Input) -> Output:
        castmembers: List[CastMember] = self.castmember_repository.list()
        sorted_castmembers: List = sorted(
            [
                self.Output(
                    id=castmember.id,
                    name=castmember.name,
                    type=castmember.type,
                )
                for castmember in castmembers
            ],
            key=lambda castmember: getattr(castmember, input.order_by),
        )
        DEFAULT_PAGE_SIZE = 2
        page_offset = (input.current_page - 1) * DEFAULT_PAGE_SIZE
        castmembers_page = sorted_castmembers[
            page_offset : page_offset + DEFAULT_PAGE_SIZE
        ]
        return self.ListOutput(
            data=castmembers_page,
            meta=ListCastMember.OutputMeta(
                current_page=input.current_page,
                per_page=DEFAULT_PAGE_SIZE,
                total=len(sorted_castmembers),
            ),
        )
