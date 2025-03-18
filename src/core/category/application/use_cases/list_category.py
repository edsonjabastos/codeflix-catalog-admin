from dataclasses import dataclass, field
from typing import List
from uuid import UUID
from core.category.domain.category_repository import CategoryRepository


class ListCategory:
    def __init__(self, repository: CategoryRepository):
        self.repository: CategoryRepository = repository

    @dataclass
    class Input:
        order_by: str = "name"
        current_page: int = 1

    @dataclass
    class Output:
        id: UUID
        name: str
        description: str
        is_active: bool

    @dataclass
    class OutputMeta:
        current_page: int
        per_page: int
        total: int

    @dataclass
    class ListOutput:
        data: list["ListCategory.Output"]
        meta: "ListCategory.OutputMeta" = field(
            default_factory="ListCategory.ListOutputMeta"
        )

    def execute(self, input: Input) -> ListOutput:
        categories = self.repository.list()
        sorted_categories: List = sorted(
            [
                self.Output(
                    id=category.id,
                    name=category.name,
                    description=category.description,
                    is_active=category.is_active,
                )
                for category in categories
            ],
            key=lambda category: getattr(category, input.order_by),
        )
        DEFAULT_PAGE_SIZE = 2
        page_offset = (input.current_page - 1) * DEFAULT_PAGE_SIZE
        categories_page = sorted_categories[
            page_offset : page_offset + DEFAULT_PAGE_SIZE
        ]
        return self.ListOutput(
            data=categories_page,
            meta=ListCategory.OutputMeta(
                current_page=input.current_page,
                per_page=DEFAULT_PAGE_SIZE,
                total=len(sorted_categories),
            ),
        )
