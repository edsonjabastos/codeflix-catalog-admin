from dataclasses import dataclass
from uuid import UUID

from core._shared.application.ports.event_publisher import EventPublisher
from core.video.application.exceptions import AudioVideoMediaNotFound, VideoNotFound
from core.video.application.events.integrations_events import (
    AudioVideoMediaUpdatedIntegrationEvent,
)
from core.video.domain.events.event import AudioVideoMediaUpdated
from core.video.domain.value_objects import MediaStatus, MediaType
from core.video.domain.video import Video
from core.video.domain.video_repository import VideoRepository


class ProcessAudioVideoMedia:
    @dataclass
    class Input:
        video_id: UUID
        media_type: MediaType
        encoded_location: str
        status: MediaStatus

    def __init__(
        self,
        video_repository: VideoRepository,
        event_publisher: EventPublisher,
    ) -> None:
        self.video_repository: VideoRepository = video_repository
        self.event_publisher: EventPublisher = event_publisher

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
                media_type=request.media_type,
            )
            self.video_repository.update(video)

        elif request.media_type == MediaType.TRAILER:
            if not video.trailer:
                raise AudioVideoMediaNotFound(
                    f"Trailer media not found for video id {request.video_id}"
                )
            video.process_trailer(
                status=request.status,
                encoded_location=request.encoded_location,
            )
            self.video_repository.update(video)

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
