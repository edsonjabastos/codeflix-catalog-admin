from dataclasses import dataclass
from pathlib import Path
from uuid import UUID

from core._shared.application.ports.checksum_service import ChecksumService
from core._shared.application.ports.event_publisher import EventPublisher
from core._shared.application.ports.storage_service import StorageService
from core.video.application.events.integrations_events import (
    AudioVideoMediaUpdatedIntegrationEvent,
)
from core.video.application.exceptions import VideoNotFound
from core.video.domain.events.event import AudioVideoMediaUpdated
from core.video.domain.video import Video
from core.video.domain.video_repository import VideoRepository
from core.video.domain.value_objects import AudioVideoMedia, MediaStatus, MediaType


class UploadVideo:
    def __init__(
        self,
        video_repository: VideoRepository,
        storage_service: StorageService,
        event_publisher: EventPublisher,
        checksum_service: ChecksumService,
        storage_base_path: str,
    ) -> None:
        self.repository: VideoRepository = video_repository
        self.storage_service: StorageService = storage_service
        self.event_publisher: EventPublisher = event_publisher
        self.checksum_service: ChecksumService = checksum_service
        self.storage_base_path: str = storage_base_path

    @dataclass
    class Input:
        video_id: UUID
        file_name: str
        content: bytes
        content_type: str
        media_type: MediaType = MediaType.VIDEO

    def execute(self, input: Input) -> None:
        video: Video = self.repository.get_by_id(input.video_id)

        if not isinstance(video, Video):
            raise VideoNotFound(f"Video with id '{input.video_id}' not found.")

        file_path = str(Path("videos") / str(input.video_id) / input.file_name)

        self.storage_service.store(
            file_path=file_path,
            content=input.content,
            content_type=input.content_type,
        )

        audio_video_media: AudioVideoMedia = AudioVideoMedia(
            name=input.file_name,
            checksum=self.checksum_service.compute(file_path, self.storage_base_path),
            raw_location=file_path,
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=input.media_type,
        )

        if input.media_type == MediaType.VIDEO:
            video.update_video(video=audio_video_media)
        else:
            video.update_trailer(trailer=audio_video_media)

        self.repository.update(video)

        integration_events = self._map_domain_events(video.pull_events())
        if integration_events:
            self.event_publisher.publish(integration_events)

    def _map_domain_events(
        self, events: list
    ) -> list[AudioVideoMediaUpdatedIntegrationEvent]:
        integration_events: list[AudioVideoMediaUpdatedIntegrationEvent] = []
        for event in events:
            if isinstance(event, AudioVideoMediaUpdated):
                integration_events.append(
                    AudioVideoMediaUpdatedIntegrationEvent(
                        resource_id=f"{event.aggregate_id}.{event.media_type}",
                        file_path=event.file_path,
                    )
                )
        return integration_events
