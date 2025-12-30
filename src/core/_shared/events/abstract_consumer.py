from abc import ABC, abstractmethod


class AbstractConsumer(ABC):
    @abstractmethod
    def on_message(self, message: bytes): ...

    @abstractmethod
    def start(self): ...

    @abstractmethod
    def stop(self): ...
