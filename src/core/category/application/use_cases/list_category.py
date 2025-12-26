from dataclasses import dataclass
from uuid import UUID
from src.core._shared.application.use_cases.list_use_case import ListUseCase
from core.category.domain.category import Category


class ListCategory(ListUseCase["Category", "ListCategory.Output"]):

    @dataclass
    class Output:
        id: UUID
        name: str
        description: str
        is_active: bool

    def execute(self, input: "ListCategory.Input") -> "ListUseCase.ListOutput":
        return super().execute(input, self.Output)
