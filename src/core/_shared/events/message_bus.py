from core._shared.events.abstract_message_bus import AbstractMessageBus
from core._shared.events.event import Event
from src.core._shared.application.handler import Handler
from src.core._shared.application.use_cases.list_use_case import Type


class MessageBus(AbstractMessageBus):
    def __init__(self) -> None:
        self.handlers: dict[Type[Event], list[Handler]] = {}

    def handle(self, events: list[Event]) -> None:
        for event in events:
            handlers = self.handlers.get(type(event), [])
            for handler in handlers:
                try:
                    handler.handle(event)
                except Exception as e:
                    print(f"Error handling event {event}: {e}")
