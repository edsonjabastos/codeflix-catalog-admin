import uuid


class Category:
    def __init__(
        self,
        name,
        id: uuid.UUID = None,
        description: str = "",
        is_active=True,
    ):
        self.id = id or uuid.uuid4()
        self.name = name
        self.description = description
        self.is_active = is_active

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
            raise ValueError("name cannot be empty")
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255 characters")

    def activate(self) -> None:
        self.is_active = True

        self.validate_name()

    def deactivate(self) -> None:
        self.is_active = False

        self.validate_name()