from dataclasses import dataclass
from decimal import Decimal
from uuid import UUID
from core.video.domain.video_repository import VideoRepository
from core.video.domain.video import Video
from core.video.application.exceptions import VideoNotFound
from core.video.domain.value_objects import Rating


class GetVideo:
    def __init__(self, video_repository: VideoRepository) -> None:
        self.repository: VideoRepository = video_repository

    @dataclass
    class Input:
        id: UUID

    @dataclass
    class Output:
        id: UUID
        title: str
        description: str
        launch_year: int
        published: bool
        duration: Decimal
        rating: Rating

        categories: set[UUID]
        genres: set[UUID]
        cast_members: set[UUID]

    def execute(self, input: "GetVideo.Input") -> "GetVideo.Output":
        video: Video = self.repository.get_by_id(input.id)

        if not isinstance(video, Video):
            raise VideoNotFound(f"Video with id '{input.id}' not found.")

        return GetVideo.Output(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            published=video.published,
            rating=video.rating,
            categories=video.categories,
            genres=video.genres,
            cast_members=video.cast_members,
        )
