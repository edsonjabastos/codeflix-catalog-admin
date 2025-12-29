from abc import ABC, abstractmethod
from typing import Type
from core._shared.events.event import Event
from core._shared.events.abstract_message_bus import AbstractMessageBus


class Handler(ABC):
    @abstractmethod
    def handle(self, events: list[Event]) -> None: ...
