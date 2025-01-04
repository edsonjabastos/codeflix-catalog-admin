from typing import Any, Set
from uuid import UUID, uuid4
from dataclasses import dataclass, field


@dataclass
class Genre:
    name: str
    is_active: bool = True
    categories: Set[UUID] = field(default_factory=set)
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self):
        self.validate_name()

    def __str__(self) -> str:
        return f"{self.name} - ({self.is_active}) - {len(self.categories)} categories"

    def __repr__(self) -> str:
        return f"<Genre {self.name} ({self.id})>"

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Genre):
            return False
        return self.id == other.id

    def update_name(self, name: str) -> None:
        self.name = name

        self.validate_name()

    def validate_name(self) -> None:
        if not self.name:
            raise ValueError("name cannot be empty")
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255 characters")

    def activate(self) -> None:
        self.is_active = True

        self.validate_name()

    def deactivate(self) -> None:
        self.is_active = False

        self.validate_name()

    def add_category(self, category_id: UUID) -> None:
        self.categories.add(category_id)

    def remove_category(self, category_id: UUID) -> None:
        self.categories.remove(category_id)

        self.validate_name()
