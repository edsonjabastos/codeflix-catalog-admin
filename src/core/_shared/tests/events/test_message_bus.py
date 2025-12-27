from unittest.mock import create_autospec
from src.core._shared.application.handler import Handler
from src.core._shared.domain.entity import MessageBus
from src.core._shared.events.event import Event


class DummyEvent(Event): ...


class TestMessageBus:
    def test_calls_correct_handler_with_event(self) -> None:
        message_bus: MessageBus = MessageBus()
        dummy_handler: Handler = create_autospec(Handler)
        message_bus.handlers[DummyEvent] = [dummy_handler]

        dummy_event: DummyEvent = DummyEvent()
        message_bus.handle([dummy_event])
        dummy_handler.handle.assert_called_once_with(dummy_event)
