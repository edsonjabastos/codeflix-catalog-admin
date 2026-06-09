from typing import List
from uuid import UUID
from core.video.domain.video_repository import VideoRepository
from core.video.domain.video import Video


class InMemoryVideoRepository(VideoRepository):
    def __init__(self, videos: List[Video] = None) -> None:
        self.videos: List[Video] = videos or []

    def save(self, video: Video) -> None:
        self.videos.append(video)

        return None

    def get_by_id(self, id: UUID) -> Video | None:

        return next((video for video in self.videos if video.id == id), None)

    def delete(self, id: UUID) -> None:
        video: Video = self.get_by_id(id=id)
        if video:
            self.videos.remove(video)

        return None

    def update(self, video: Video) -> None:
        video_to_be_updated: Video = self.get_by_id(id=video.id)
        if video_to_be_updated:
            # self.delete(id=video.id) # alternative way to update
            # self.save(video)
            video_to_be_updated_index: int = self.videos.index(video_to_be_updated)
            self.videos[video_to_be_updated_index] = video

        return None

    def list(self) -> List[Video]:

        return [video for video in self.videos]
