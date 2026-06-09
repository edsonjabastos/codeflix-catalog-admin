from abc import ABC, abstractmethod

from core._shared.events.event import Event


class Handler(ABC):
    @abstractmethod
    def handle(self, event: Event) -> None: ...
