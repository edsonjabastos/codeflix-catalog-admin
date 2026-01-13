from django.core.management.base import BaseCommand
from core.video.infra.video_converted_rabbitmq_consumer import (
    VideoConvertedRabbitMQConsumer,
)


class Command(BaseCommand):
    help = "Start the RabbitMQ consumer for processed video media."

    def handle(self, *args, **options):
        consumer: VideoConvertedRabbitMQConsumer = VideoConvertedRabbitMQConsumer()
        consumer.start()
