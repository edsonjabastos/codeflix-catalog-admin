from decimal import Decimal
from unittest.mock import create_autospec, patch
import pytest
from core._shared.application.ports.checksum_service import ChecksumService
from core._shared.application.ports.event_publisher import EventPublisher
from core._shared.application.ports.storage_service import StorageService
from core.video.application.use_cases.upload_video import UploadVideo
from core.video.application.exceptions import VideoNotFound
from core.video.domain.value_objects import (
    MediaStatus,
    Rating,
    AudioVideoMedia,
    MediaType,
)
from core.video.domain.video import Video
from django_project.adapters.persistence.in_memory.video_repository import (
    InMemoryVideoRepository,
)
from django_project.adapters.storage.file_checksum_service import FileChecksumService
from core.video.application.events.integrations_events import (
    AudioVideoMediaUpdatedIntegrationEvent,
)


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
def mock_storage_service() -> StorageService:
    return create_autospec(StorageService)


@pytest.fixture
def mock_event_publisher() -> EventPublisher:
    return create_autospec(EventPublisher)


@pytest.fixture
def mock_checksum_service() -> ChecksumService:
    return create_autospec(ChecksumService)


@pytest.fixture
def storage_base_path(tmp_path) -> str:
    return str(tmp_path)


class TestUploadVideo:
    def test_upload_video_media_to_video(
        self,
        video: Video,
        video_repository: InMemoryVideoRepository,
        mock_storage_service: StorageService,
        mock_event_publisher: EventPublisher,
        mock_checksum_service: ChecksumService,
        storage_base_path: str,
    ) -> None:
        mock_checksum_service.compute.return_value = "test_checksum"

        upload_video: UploadVideo = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage_service,
            event_publisher=mock_event_publisher,
            checksum_service=mock_checksum_service,
            storage_base_path=storage_base_path,
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

        assert video_repository.videos[0] == video_from_repo

        assert video_from_repo.video == AudioVideoMedia(
            name=input.file_name,
            checksum="test_checksum",
            raw_location=f"videos/{video.id}/test_video.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO,
        )

        mock_event_publisher.publish.assert_called_once()

    def test_upload_video_media_not_found(
        self,
        video_repository: InMemoryVideoRepository,
        mock_storage_service: StorageService,
        mock_event_publisher: EventPublisher,
        mock_checksum_service: ChecksumService,
        storage_base_path: str,
    ) -> None:
        upload_video: UploadVideo = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage_service,
            event_publisher=mock_event_publisher,
            checksum_service=mock_checksum_service,
            storage_base_path=storage_base_path,
        )

        input: UploadVideo.Input = UploadVideo.Input(
            video_id="non_existent_id",
            file_name="test_video.mp4",
            content=b"test_content",
            content_type="video/mp4",
        )

        with pytest.raises(VideoNotFound) as excinfo:
            upload_video.execute(input=input)

        assert str(excinfo.value) == "Video with id 'non_existent_id' not found."

    def test_upload_video_updates_repository(
        self,
        video: Video,
        video_repository: InMemoryVideoRepository,
        mock_storage_service: StorageService,
        mock_event_publisher: EventPublisher,
        mock_checksum_service: ChecksumService,
        storage_base_path: str,
    ) -> None:
        mock_checksum_service.compute.return_value = "checksum123"

        upload_video: UploadVideo = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage_service,
            event_publisher=mock_event_publisher,
            checksum_service=mock_checksum_service,
            storage_base_path=storage_base_path,
        )

        input: UploadVideo.Input = UploadVideo.Input(
            video_id=video.id,
            file_name="movie.mp4",
            content=b"video_content",
            content_type="video/mp4",
        )

        upload_video.execute(input=input)

        updated_video = video_repository.get_by_id(video.id)
        assert updated_video.video is not None
        assert updated_video.video.name == "movie.mp4"
        assert updated_video.video.status == MediaStatus.PENDING

    def test_upload_video_publishes_integration_event(
        self,
        video: Video,
        video_repository: InMemoryVideoRepository,
        mock_storage_service: StorageService,
        mock_event_publisher: EventPublisher,
        mock_checksum_service: ChecksumService,
        storage_base_path: str,
    ) -> None:
        mock_checksum_service.compute.return_value = "checksum456"

        upload_video: UploadVideo = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage_service,
            event_publisher=mock_event_publisher,
            checksum_service=mock_checksum_service,
            storage_base_path=storage_base_path,
        )

        input: UploadVideo.Input = UploadVideo.Input(
            video_id=video.id,
            file_name="upload.mp4",
            content=b"content",
            content_type="video/mp4",
        )

        upload_video.execute(input=input)

        mock_event_publisher.publish.assert_called_once()
        call_args = mock_event_publisher.publish.call_args[0][0]
        assert len(call_args) == 1
        assert isinstance(call_args[0], AudioVideoMediaUpdatedIntegrationEvent)
        assert call_args[0].resource_id == f"{video.id}.{MediaType.VIDEO}"
        assert call_args[0].file_path == f"videos/{video.id}/upload.mp4"

    def test_upload_video_calculates_real_checksum(
        self,
        video: Video,
        video_repository: InMemoryVideoRepository,
        mock_storage_service: StorageService,
        mock_event_publisher: EventPublisher,
        tmp_path,
    ) -> None:
        storage_base_path = str(tmp_path)
        checksum_service = FileChecksumService()
        upload_video: UploadVideo = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage_service,
            event_publisher=mock_event_publisher,
            checksum_service=checksum_service,
            storage_base_path=storage_base_path,
        )

        test_content = b"test_video_content_for_checksum"
        input: UploadVideo.Input = UploadVideo.Input(
            video_id=video.id,
            file_name="checksum_test.mp4",
            content=test_content,
            content_type="video/mp4",
        )

        file_path = tmp_path / "videos" / str(video.id) / "checksum_test.mp4"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(test_content)

        with patch("core.video.application.use_cases.upload_video.Path") as mock_path:
            mock_path.return_value.__truediv__.return_value.__truediv__.return_value = (
                str(file_path.relative_to(tmp_path))
            )
            upload_video.execute(input=input)

        updated_video = video_repository.get_by_id(video.id)
        assert updated_video.video is not None
        assert updated_video.video.checksum is not None
        assert len(updated_video.video.checksum) > 0

        expected_checksum = checksum_service.compute(
            f"videos/{video.id}/checksum_test.mp4", storage_base_path
        )
        assert updated_video.video.checksum == expected_checksum
