from unittest.mock import create_autospec
from core._shared.events.event import Event
from src.core._shared.domain.entity import Entity
from src.core._shared.events.abstract_message_bus import AbstractMessageBus


class DummyEvent(Event): ...


class DummyEntity(Entity): ...


class TestDispactch:

    def test_dispatch(self):
        mock_message_bus: AbstractMessageBus = create_autospec(AbstractMessageBus)
        entity: DummyEntity = DummyEntity(message_bus=mock_message_bus)
        entity.dispatch(DummyEvent())
        assert entity.events == [DummyEvent()]
        mock_message_bus.handle.assert_called_once_with(entity.events)
