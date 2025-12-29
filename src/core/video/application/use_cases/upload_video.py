from dataclasses import dataclass
from pathlib import Path
from uuid import UUID


from core._shared.application.handler import AbstractMessageBus
from core._shared.infrastructure.storage.abstract_storage_service import (
    AbstractStorageService,
)
from core.video.application.exceptions import VideoNotFound
from core.video.domain.video_repository import VideoRepository
from core.video.domain.video import Video
from core.video.domain.value_objects import MediaStatus, AudioVideoMedia, MediaType
from core.video.application.events.integrations_events import (
    AudioVideoMediaUpdatedIntegrationEvent,
)
from core._shared.utils.checksum import get_file_checksum


class UploadVideo:
    def __init__(
        self,
        video_repository: VideoRepository,
        storage_service: AbstractStorageService,
        message_bus: AbstractMessageBus,
    ) -> None:
        self.repository: VideoRepository = video_repository
        self.storage_service: AbstractStorageService = storage_service
        self.message_bus: AbstractMessageBus = message_bus

    @dataclass
    class Input:
        video_id: UUID
        file_name: str
        content: bytes
        content_type: str

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
            checksum=get_file_checksum(file_path),
            raw_location=file_path,
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO,
        )

        video.update_video(
            video=audio_video_media,
        )

        self.repository.update(video)

        self.message_bus.handle(
            [
                AudioVideoMediaUpdatedIntegrationEvent(
                    resource_id=f"{video.id}.{MediaType.VIDEO}",
                    file_path=file_path,
                )
            ]
        )
