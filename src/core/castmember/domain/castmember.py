from dataclasses import dataclass, field
from uuid import UUID, uuid4

from core.castmember.domain.value_objects import CastMemberType


@dataclass
class CastMember:
    name: str
    type: CastMemberType
    id: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        self.validate()

    def validate(self) -> None:
        if not self.name:
            raise ValueError("name cannot be empty")
        if len(self.name) > 255:
            raise ValueError("name cannot be longer than 255 characters")
        if not isinstance(self.type, CastMemberType):
            raise ValueError("invalid type")

    def update(self, name: str, type: CastMemberType) -> None:
        current_name = self.name
        current_type = self.type
        self.name = name
        self.type = type
        try:
            self.validate()
        except ValueError as e:
            self.name = current_name
            self.type = current_type
            raise e

    def __str__(self) -> str:
        return f"{self.name} - {self.type}"

    def __repr__(self) -> str:
        return f"<CastMember {self.name} ({self.id})>"

    def __eq__(self, other: any) -> bool:
        if not isinstance(other, CastMember):
            return False
        return self.id == other.id
