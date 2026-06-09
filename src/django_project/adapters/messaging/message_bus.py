from typing import Type

from core._shared.application.handler import Handler
from core._shared.application.ports.event_publisher import EventPublisher
from core._shared.events.event import Event
from core.video.application.events.integrations_events import (
    AudioVideoMediaUpdatedIntegrationEvent,
)
from django_project.adapters.messaging.publish_handler import (
    PublishAudioVideoMediaUpdatedHandler,
)
from django_project.adapters.messaging.rabbitmq_dispatcher import (
    RabbitMQEventDispatcher,
)


class MessageBus(EventPublisher):
    def __init__(self) -> None:
        self.handlers: dict[Type[Event], list[Handler]] = {
            AudioVideoMediaUpdatedIntegrationEvent: [
                PublishAudioVideoMediaUpdatedHandler(
                    event_dispatcher=RabbitMQEventDispatcher(queue="videos.new")
                )
            ],
        }

    def publish(self, events: list[Event]) -> None:
        for event in events:
            handlers: list[Handler] = self.handlers.get(type(event), [])
            for handler in handlers:
                try:
                    handler.handle(event)
                except Exception as e:
                    print(f"Error handling event {event}: {e}")
