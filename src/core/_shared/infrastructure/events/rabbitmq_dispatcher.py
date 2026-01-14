from dataclasses import asdict
import json
from core._shared.application.handler import Event
from core.video.application.events.handlers import EventDispatcher
from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel


class RabbitMQEventDispatcher(EventDispatcher):
    """
    RabbitMQ event dispatcher implementation.
    """

    def __init__(self, host: str = "localhost", queue: str = "videos.new") -> None:
        self.host: str = host
        self.queue: str = queue
        self.connection: BlockingConnection | None = None
        self.channel: BlockingChannel | None = None

    def dispatch(self, event: Event) -> None:
        if not self.connection:
            self.connection: BlockingConnection = BlockingConnection(
                ConnectionParameters(host=self.host)
            )
            self.channel: BlockingChannel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=json.dumps(asdict(event)),
        )
        print(f"Dispatching event {event} to RabbitMQ on queue {self.queue}")
