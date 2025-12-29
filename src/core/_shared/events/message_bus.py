from core._shared.events.abstract_message_bus import AbstractMessageBus
from core._shared.events.event import Event
from core._shared.application.handler import Handler
from core._shared.application.use_cases.list_use_case import Type
from core.video.application.events.integrations_events import (
    AudioVideoMediaUpdatedIntegrationEvent,
)
from core._shared.infrastructure.events.rabbitmq_dispatcher import (
    RabbitMQEventDispatcher,
)
from core.video.application.events.handlers import (
    PublishAudioVideoMediaUpdatedHandler,
)


class MessageBus(AbstractMessageBus):
    def __init__(self) -> None:
        self.handlers: dict[Type[Event], list[Handler]] = {
            AudioVideoMediaUpdatedIntegrationEvent: [
                PublishAudioVideoMediaUpdatedHandler(
                    event_dispatcher=RabbitMQEventDispatcher(queue="videos.new")
                )
            ],
        }

    def handle(self, events: list[Event]) -> None:
        for event in events:
            handlers: list[Handler] = self.handlers.get(type(event), [])
            for handler in handlers:
                try:
                    handler.handle(event)
                except Exception as e:
                    print(f"Error handling event {event}: {e}")
