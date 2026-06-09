import json
import logging
from uuid import UUID

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel

from core.video.application.use_cases.process_audio_video_media import (
    ProcessAudioVideoMedia,
)
from core.video.domain.value_objects import MediaStatus, MediaType
from django_project.adapters.messaging.abstract_consumer import AbstractConsumer

logger = logging.getLogger(__name__)


class VideoConvertedRabbitMQConsumer(AbstractConsumer):
    def __init__(
        self,
        use_case: ProcessAudioVideoMedia,
        host: str = "localhost",
        queue: str = "videos.converted",
    ):
        self.use_case = use_case
        self.host: str = host
        self.queue: str = queue
        self.connection: BlockingConnection | None = None
        self.channel: BlockingChannel | None = None

    def on_message(self, message: bytes):
        print(f"Received message: {message}")
        try:
            payload: dict = json.loads(message)

            error_message = payload["error"]
            if error_message:
                aggregate_id_raw, _ = payload["message"]["resource_id"].split(".")
                logger.error(
                    f"Error processing video {aggregate_id_raw}: {error_message}"
                )
                return

            aggregate_id_raw, media_type_raw = payload["video"]["resource_id"].split(
                "."
            )
            aggregate_id: UUID = UUID(aggregate_id_raw)
            media_type: MediaType = MediaType(media_type_raw)
            encoded_location: str = payload["video"]["encoded_video_folder"]
            status: MediaStatus = MediaStatus(payload["status"])

            process_input = ProcessAudioVideoMedia.Input(
                video_id=aggregate_id,
                encoded_location=encoded_location,
                media_type=media_type,
                status=status,
            )
            print("Calling use case with input", process_input)
            self.use_case.execute(request=process_input)
        except Exception:
            logger.error(f"Error processing payload {message}", exc_info=True)
            return

    def start(self):
        self.connection = BlockingConnection(ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)
        self.channel.basic_consume(
            queue=self.queue, on_message_callback=self.on_message_callback
        )
        print("Consumer started. Waiting for messages. To exit press CTRL+C")
        self.channel.start_consuming()

    def on_message_callback(self, ch, method, properties, body):
        self.on_message(body)

    def stop(self):
        self.connection.close()
