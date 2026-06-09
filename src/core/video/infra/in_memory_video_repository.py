from typing import List
from uuid import UUID

from core.video.domain.video import Video
from core.video.domain.video_repository import VideoRepository


class InMemoryVideoRepository(VideoRepository):
    def __init__(self, videos: List[Video] = None) -> None:
        self.videos: List[Video] = videos or []

    def save(self, video: Video) -> None:
        self.videos.append(video)

    def get_by_id(self, id: UUID) -> Video | None:
        return next((video for video in self.videos if video.id == id), None)

    def delete(self, id: UUID) -> None:
        video: Video = self.get_by_id(id=id)
        if video:
            self.videos.remove(video)

    def update(self, video: Video) -> None:
        video_to_be_updated: Video = self.get_by_id(id=video.id)
        if video_to_be_updated:
            video_to_be_updated_index: int = self.videos.index(video_to_be_updated)
            self.videos[video_to_be_updated_index] = video

    def list(self) -> List[Video]:
        return [video for video in self.videos]
