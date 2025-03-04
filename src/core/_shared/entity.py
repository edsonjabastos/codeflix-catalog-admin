from dataclasses import dataclass, field
from uuid import UUID, uuid4
from abc import ABC

from core._shared.notification import Notification


@dataclass(kw_only=True)
class Entity(ABC):
    id: UUID = field(default_factory=uuid4)
    notification: Notification = field(default_factory=Notification)

    def __eq__(self, other: "Entity") -> bool:
        print(other, self.__class__)
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
