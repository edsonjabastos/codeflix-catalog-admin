import uuid
from uuid import UUID, uuid4
from dataclasses import dataclass, field

from src.core.category.domain.notification import Notification


@dataclass
class Category:
    name: str
    description: str = ""
    is_active: bool = True
    id: UUID = field(default_factory=uuid4)

    notification: Notification = field(default_factory=Notification)

    def __post_init__(self):
        self.validate_name()

    def __str__(self) -> str:
        return f"{self.name} - {self.description} ({self.is_active})"

    def __repr__(self) -> str:
        return f"<Category {self.name} ({self.id})>"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def update_category(self, name: str, description: str) -> None:
        self.name = name
        self.description = description

        self.validate_name()

    def validate_name(self) -> None:
        if not self.name:
            # raise ValueError("name cannot be empty")
            self.notification.add_error("name cannot be empty")

        if len(self.name) > 255:
            # raise ValueError("name cannot be longer than 255 characters")
            self.notification.add_error("name cannot be longer than 255 characters")

        if len(self.description) > 1024:
            # raise ValueError("description cannot be longer than 1024 characters")
            self.notification.add_error(
                "description cannot be longer than 1024 characters"
            )

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def activate(self) -> None:
        self.is_active = True

        self.validate_name()

    def deactivate(self) -> None:
        self.is_active = False

        self.validate_name()
