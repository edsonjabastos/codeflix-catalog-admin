from abc import ABC, abstractmethod
from core._shared.application.handler import Event


class EventDispatcher(ABC):
    @abstractmethod
    def dispatch(self, event: Event) -> None:
        raise NotImplementedError
