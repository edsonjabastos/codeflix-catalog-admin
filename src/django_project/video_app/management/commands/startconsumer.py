from django.core.management.base import BaseCommand
from core.video.infra.video_converted_rabbitmq_consumer import (
    VideoConvertedRabbitMQConsumer,
)
import os
import dotenv

dotenv.load_dotenv()


class Command(BaseCommand):
    help = "Start the RabbitMQ consumer for processed video media."

    def handle(self, *args, **options):
        consumer: VideoConvertedRabbitMQConsumer = VideoConvertedRabbitMQConsumer(
            host=os.getenv("RABBITMQ_HOST", "localhost"),
            queue=os.getenv("VIDEOS_CONVERTED_QUEUE", "videos.converted"),
        )
        consumer.start()
