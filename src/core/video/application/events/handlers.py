from core._shared.application.handler import Handler
from core._shared.events.event_dispatcher import EventDispatcher
from core.video.application.events.integrations_events import (
    AudioVideoMediaUpdatedIntegrationEvent,
)


class PublishAudioVideoMediaUpdatedHandler(Handler):
    def __init__(self, event_dispatcher: EventDispatcher) -> None:
        self.event_dispatcher: EventDispatcher = event_dispatcher

    def handle(self, event: AudioVideoMediaUpdatedIntegrationEvent) -> None:
        print(f"Publishing event {event}")
        self.event_dispatcher.dispatch(event)
