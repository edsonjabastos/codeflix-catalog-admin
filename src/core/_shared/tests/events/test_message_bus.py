from unittest.mock import create_autospec
from core._shared.application.handler import Handler
from core._shared.domain.entity import MessageBus
from core._shared.events.event import Event


class DummyEvent(Event): ...


class TestMessageBus:
    def test_calls_correct_handler_with_event(self) -> None:
        message_bus: MessageBus = MessageBus()
        dummy_handler: Handler = create_autospec(Handler)
        message_bus.handlers[DummyEvent] = [dummy_handler]

        dummy_event: DummyEvent = DummyEvent()
        message_bus.handle([dummy_event])
        dummy_handler.handle.assert_called_once_with(dummy_event)

    def test_calls_multiple_handlers_with_event(self) -> None:
        message_bus: MessageBus = MessageBus()
        dummy_handler_1: Handler = create_autospec(Handler)
        dummy_handler_2: Handler = create_autospec(Handler)
        message_bus.handlers[DummyEvent] = [dummy_handler_1, dummy_handler_2]

        dummy_event: DummyEvent = DummyEvent()
        message_bus.handle([dummy_event])
        dummy_handler_1.handle.assert_called_once_with(dummy_event)
        dummy_handler_2.handle.assert_called_once_with(dummy_event)