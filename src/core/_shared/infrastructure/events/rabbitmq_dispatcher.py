from core._shared.application.handler import Event
from core.video.application.events.handlers import EventDispatcher


class RabbitMQEventDispatcher(EventDispatcher):
    def __init__(self, queue: str = "videos.new") -> None:
        self.queue: str = queue

    def dispatch(self, event: Event) -> None:
        print(f"Dispatching event {event} to RabbitMQ")
