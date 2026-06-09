from abc import ABC, abstractmethod

from core._shared.events.event import Event


class EventPublisher(ABC):
    @abstractmethod
    def publish(self, events: list[Event]) -> None:
        raise NotImplementedError
