from dataclasses import dataclass
from uuid import UUID

from core.video.domain.value_objects import MediaType, MediaStatus
from core.video.domain.video_repository import VideoRepository
from core.video.domain.video import Video
from core.video.application.exceptions import VideoNotFound, AudioVideoMediaNotFound


class ProcessAudioVideoMedia:
    @dataclass
    class Input:
        video_id: UUID
        media_type: MediaType
        encoded_location: str
        status: MediaStatus

    def __init__(self, video_repository: VideoRepository) -> None:
        self.video_repository: VideoRepository = video_repository

    def execute(self, request: Input) -> None:
        video: Video = self.video_repository.get_by_id(id=request.video_id)
        if video is None:
            raise VideoNotFound(f"Video with id {request.video_id} not found")
        if request.media_type == MediaType.VIDEO:
            if not video.video:
                raise AudioVideoMediaNotFound(
                    f"Video media not found for video id {request.video_id}"
                )
            video.process(
                status=request.status,
                encoded_location=request.encoded_location,
            )
            self.video_repository.update(video)
