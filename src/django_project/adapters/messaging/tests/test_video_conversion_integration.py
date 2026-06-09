"""
Integration test for the video conversion flow without RabbitMQ or an external consumer.

Exercises the full path: consumer message parsing → use case → Django repository.
"""

import json
from decimal import Decimal

import pytest

from core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType, Rating
from core.video.domain.video import Video
from django_project.adapters.composition.container import get_container
from django_project.adapters.persistence.django.video_repository import (
    DjangoORMVideoRepository,
)
from django_project.adapters.messaging.video_converted_consumer import (
    VideoConvertedRabbitMQConsumer,
)


@pytest.fixture
def video_repository() -> DjangoORMVideoRepository:
    return get_container().video_repository()


@pytest.fixture
def consumer() -> VideoConvertedRabbitMQConsumer:
    return get_container().video_converted_consumer()


@pytest.fixture
def video_with_pending_media(video_repository: DjangoORMVideoRepository) -> Video:
    video = Video(
        title="Conversion Test Video",
        description="Integration test video",
        launch_year=2024,
        duration=Decimal("90.0"),
        published=False,
        rating=Rating.L,
        categories=set(),
        genres=set(),
        cast_members=set(),
    )
    video.update_video(
        AudioVideoMedia(
            name="test.mp4",
            checksum="abc123",
            raw_location=f"/videos/{video.id}/test.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO,
        )
    )
    video_repository.save(video)
    return video


@pytest.mark.django_db
class TestVideoConversionIntegration:
    def test_consumer_message_marks_video_completed_and_published(
        self,
        consumer: VideoConvertedRabbitMQConsumer,
        video_repository: DjangoORMVideoRepository,
        video_with_pending_media: Video,
    ) -> None:
        encoded_location = f"/encoded/videos/{video_with_pending_media.id}"
        message = {
            "error": "",
            "video": {
                "resource_id": f"{video_with_pending_media.id}.VIDEO",
                "encoded_video_folder": encoded_location,
            },
            "status": "COMPLETED",
        }

        consumer.on_message(json.dumps(message).encode("utf-8"))

        updated_video = video_repository.get_by_id(video_with_pending_media.id)

        assert updated_video is not None
        assert updated_video.video is not None
        assert updated_video.video.status == MediaStatus.COMPLETED
        assert updated_video.video.encoded_location == encoded_location
        assert updated_video.published is True
