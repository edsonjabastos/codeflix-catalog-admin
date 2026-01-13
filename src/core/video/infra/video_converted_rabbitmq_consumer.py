import json
import logging
from uuid import UUID

from pika import BlockingConnection, ConnectionParameters
from pika.adapters.blocking_connection import BlockingChannel

from core._shared.events.abstract_consumer import AbstractConsumer
from core.video.application.use_cases.process_audio_video_media import (
    ProcessAudioVideoMedia,
)
from core.video.domain.value_objects import MediaType, MediaStatus
from django_project.video_app.repository import DjangoORMVideoRepository

logger = logging.getLogger(__name__)


class VideoConvertedRabbitMQConsumer(AbstractConsumer):
    def __init__(self, host: str = "localhost", queue: str = "videos.converted"):
        self.host: str = host
        self.queue: str = queue
        self.connection: BlockingConnection | None = None
        self.channel: BlockingChannel | None = None

    def on_message(self, message: bytes):
        print(f"Received message: {message}")
        try:
            # Body payload
            message: dict = json.loads(message)

            # Tratamento de erro
            error_message = message["error"]
            if error_message:
                aggregate_id_raw, _ = message["message"]["resource_id"].split(".")
                logger.error(
                    f"Error processing video {aggregate_id_raw}: {error_message}"
                )
                return

            # Serialização do evento
            aggregate_id_raw, media_type_raw = message["video"]["resource_id"].split(
                "."
            )
            aggregate_id: UUID = UUID(aggregate_id_raw)
            media_type: MediaType = MediaType(media_type_raw)
            encoded_location: str = message["video"]["encoded_video_folder"]
            status: MediaStatus = MediaStatus(message["status"])

            # Execução do caso de uso
            process_audio_video_media_input: ProcessAudioVideoMedia.Input = (
                ProcessAudioVideoMedia.Input(
                    video_id=aggregate_id,
                    encoded_location=encoded_location,
                    media_type=media_type,
                    status=status,
                )
            )
            print("Calling use case with input", process_audio_video_media_input)
            use_case: ProcessAudioVideoMedia = ProcessAudioVideoMedia(
                video_repository=DjangoORMVideoRepository()
            )
            use_case.execute(request=process_audio_video_media_input)
        except Exception as e:
            logger.error(f"Error processing payload {message}", exc_info=True)
            return

    def start(self):
        self.connection: BlockingConnection = BlockingConnection(
            ConnectionParameters(host=self.host)
        )
        self.channel: BlockingChannel = self.connection.channel()

        # Cria a fila se não existir
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
