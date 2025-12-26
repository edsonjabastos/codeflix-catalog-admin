from dataclasses import dataclass, field
from uuid import UUID, uuid4
from abc import ABC

from src.core._shared.domain.notification import Notification
from core._shared.events.abstract_message_bus import AbstractMessageBus
from core._shared.events.event import Event
from core._shared.events.message_bus import MessageBus


@dataclass(kw_only=True)
class Entity(ABC):
    id: UUID = field(default_factory=uuid4)
    notification: Notification = field(default_factory=Notification, init=False)
    events: list[Event] = field(default_factory=list, init=False)
    message_bus: AbstractMessageBus = field(default_factory=MessageBus)

    def dispatch(self, event: Event) -> None:
        self.events.append(event)
        self.message_bus.handle(events=self.events)

    def __eq__(self, other: "Entity") -> bool:

        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id
