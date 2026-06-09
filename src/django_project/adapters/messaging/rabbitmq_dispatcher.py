from dataclasses import asdict
import json
import os

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel

from core._shared.application.ports.event_dispatcher import EventDispatcher
from core._shared.events.event import Event


class RabbitMQEventDispatcher(EventDispatcher):
    def __init__(
        self,
        host: str | None = None,
        queue: str = "videos.new",
    ) -> None:
        self.host: str = host or os.getenv("RABBITMQ_HOST", "localhost")
        self.queue: str = queue
        self.connection: BlockingConnection | None = None
        self.channel: BlockingChannel | None = None

    def dispatch(self, event: Event) -> None:
        if not self.connection:
            self.connection = BlockingConnection(
                ConnectionParameters(host=self.host)
            )
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)
        self.channel.basic_publish(
            exchange="",
            routing_key=self.queue,
            body=json.dumps(asdict(event)),
        )
        print(f"Dispatching event {event} to RabbitMQ on queue {self.queue}")
