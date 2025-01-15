from dataclasses import dataclass, field
from uuid import UUID, uuid4

from core.castmember.domain.value_objects import CastMemberType
from src.core._shared.entity import Entity


@dataclass(eq=False)
class CastMember(Entity):
    name: str
    type: CastMemberType

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.name:
            self.notification.add_error("name cannot be empty")
        if len(self.name) > 255:
            self.notification.add_error("name cannot be longer than 255 characters")
        if not self.type in CastMemberType:
            self.notification.add_error("invalid type")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def update(self, name: str, type: CastMemberType) -> None:
        self.name = name
        self.type = type

        self.validate()

    def __str__(self) -> str:
        return f"{self.name} - {self.type}"

    def __repr__(self) -> str:
        return f"<CastMember {self.name} ({self.id})>"
