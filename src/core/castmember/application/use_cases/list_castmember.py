from dataclasses import dataclass
from uuid import UUID
from src.core._shared.application.use_cases.list_use_case import ListUseCase
from core.castmember.domain.castmember import CastMember


class ListCastMember(ListUseCase["CastMember", "ListCastMember.Output"]):

    @dataclass
    class Output:
        id: UUID
        name: str
        type: str

    def execute(self, input: "ListCastMember.Input") -> "ListUseCase.ListOutput":
        return super().execute(input, self.Output)
