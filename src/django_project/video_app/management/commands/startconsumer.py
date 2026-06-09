from django.core.management.base import BaseCommand
from django_project.adapters.composition.container import get_container
import dotenv

dotenv.load_dotenv()


class Command(BaseCommand):
    help = "Start the RabbitMQ consumer for processed video media."

    def handle(self, *args, **options):
        consumer = get_container().video_converted_consumer()
        consumer.start()
