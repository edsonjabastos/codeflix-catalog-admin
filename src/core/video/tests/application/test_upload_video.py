from decimal import Decimal
from unittest.mock import create_autospec
import pytest
from core._shared.abstract_storage_service import AbstractStorageService
from core.video.application.use_cases.upload_video import UploadVideo
from core.video.domain.value_objects import MediaStatus, Rating, AudioVideoMedia
from core.video.domain.video import Video
from core.video.infra.in_memory_video_repository import InMemoryVideoRepository


@pytest.fixture
def video() -> Video:
    return Video(
        title="Test Video",
        description="Test Description",
        launch_year=2021,
        duration=Decimal("120.5"),
        published=True,
        rating=Rating.L,
        categories=set(),
        genres=set(),
        cast_members=set(),
    )


@pytest.fixture
def video_repository(video: Video) -> InMemoryVideoRepository:
    return InMemoryVideoRepository(videos=[video])


@pytest.fixture
def mock_storage_service():
    return create_autospec(AbstractStorageService)


class TestUploadVideo:
    def test_upload_video_media_to_video(
        self,
        video: Video,
        video_repository: InMemoryVideoRepository,
        mock_storage_service,
    ) -> None:

        upload_video: UploadVideo = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage_service,
        )

        input: UploadVideo.Input = UploadVideo.Input(
            video_id=video.id,
            file_name="test_video.mp4",
            content=b"test_content",
            content_type="video/mp4",
        )
        upload_video.execute(input=input)

        mock_storage_service.store.assert_called_once_with(
            file_path=f"videos/{video.id}/test_video.mp4",
            content=input.content,
            content_type=input.content_type,
        )

        video_from_repo = video_repository.get_by_id(video.id)

        video_from_repo.video == AudioVideoMedia(
            name=input.file_name,
            raw_location=f"videos/{video.id}/test_video.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type="VIDEO",
        )

    def test_upload_video_media_not_found(
        self,
        video_repository: InMemoryVideoRepository,
        mock_storage_service,
    ) -> None:
        upload_video: UploadVideo = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage_service,
        )

        input: UploadVideo.Input = UploadVideo.Input(
            video_id="non_existent_id",
            file_name="test_video.mp4",
            content=b"test_content",
            content_type="video/mp4",
        )

        with pytest.raises(Exception) as excinfo:
            upload_video.execute(input=input)

        assert str(excinfo.value) == "Video with id 'non_existent_id' not found."
