from core._shared.events.event import Event
from core._shared.domain.entity import Entity


class DummyEvent(Event): ...


class DummyEntity(Entity): ...


class TestRecordEvent:

    def test_record_event(self):
        entity: DummyEntity = DummyEntity()
        event = DummyEvent()
        entity.record_event(event)
        assert entity.events == [event]

    def test_pull_events(self):
        entity: DummyEntity = DummyEntity()
        event = DummyEvent()
        entity.record_event(event)
        pulled = entity.pull_events()
        assert pulled == [event]
        assert entity.events == []
