from dataclasses import dataclass

from src.core._shared.domain.entity import Entity


@dataclass(eq=False)
class Category(Entity):
    name: str
    description: str = ""
    is_active: bool = True

    def __post_init__(self):
        self.validate_name()

    def __str__(self) -> str:
        return f"{self.name} - {self.description} ({self.is_active})"

    def __repr__(self) -> str:
        return f"<Category {self.name} ({self.id})>"

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
