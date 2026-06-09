from dataclasses import dataclass, field
from uuid import UUID, uuid4
from abc import ABC

from core._shared.domain.notification import Notification
from core._shared.events.event import Event


@dataclass(kw_only=True)
class Entity(ABC):
    id: UUID = field(default_factory=uuid4)
    notification: Notification = field(default_factory=Notification, init=False)
    events: list[Event] = field(default_factory=list, init=False)

    def record_event(self, event: Event) -> None:
        self.events.append(event)

    def pull_events(self) -> list[Event]:
        events, self.events = self.events, []
        return events

    def __eq__(self, other: "Entity") -> bool:

        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
