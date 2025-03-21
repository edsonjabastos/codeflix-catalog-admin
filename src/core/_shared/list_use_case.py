from typing import TypeVar, Generic, List, Type
from dataclasses import dataclass, field
from config import DEFAULT_PAGE_SIZE
from dataclasses import asdict

T = TypeVar("T")
R = TypeVar("R")


class ListUseCase(Generic[T, R]):

    def __init__(self, repository):
        self.repository = repository

    @dataclass
    class Input:
        order_by: str = "name"
        current_page: int = 1
        page_size: int = DEFAULT_PAGE_SIZE

    @dataclass
    class OutputMeta:
        current_page: int
        per_page: int
        total: int

    @dataclass
    class ListOutput(Generic[R]):
        data: List[R]
        meta: "ListUseCase.OutputMeta" = field(default_factory="ListUseCase.OutputMeta")

    def execute(
        self, input: "ListUseCase.Input", output_cls: Type[R]
    ) -> "ListUseCase.ListOutput":
        items: List[T] = self.repository.list()

        valid_fields = {
            field.name for field in output_cls.__dataclass_fields__.values()
        }

        sorted_items: List[R] = sorted(
            [
                output_cls(
                    **{k: v for k, v in asdict(item).items() if k in valid_fields}
                )
                for item in items
            ],
            key=lambda obj: getattr(obj, input.order_by),
        )

        page_offset = (input.current_page - 1) * input.page_size
        items_page = sorted_items[page_offset : page_offset + input.page_size]

        return self.ListOutput(
            data=items_page,
            meta=self.OutputMeta(
                current_page=input.current_page,
                per_page=input.page_size,
                total=len(sorted_items),
            ),
        )
