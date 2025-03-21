from dataclasses import dataclass
from typing import Set
from uuid import UUID
from core._shared.list_use_case import ListUseCase
from core.genre.domain.genre import Genre


class ListGenre(ListUseCase["Genre", "ListGenre.Output"]):

    @dataclass
    class Output:
        id: UUID
        name: str
        is_active: bool
        categories: Set[UUID]

    def execute(self, input: "ListGenre.Input") -> "ListUseCase.ListOutput":
        return super().execute(input, self.Output)
