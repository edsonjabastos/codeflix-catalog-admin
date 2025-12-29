from decimal import Decimal
from unittest.mock import create_autospec, patch
import pytest
from core._shared.application.handler import AbstractMessageBus
from core._shared.infrastructure.storage.abstract_storage_service import (
    AbstractStorageService,
)
from core.video.application.use_cases.upload_video import UploadVideo
from core.video.application.exceptions import VideoNotFound
from core.video.domain.value_objects import (
    MediaStatus,
    Rating,
    AudioVideoMedia,
    MediaType,
)
from core.video.domain.video import Video
from core.video.infra.in_memory_video_repository import InMemoryVideoRepository
from core._shared.utils.checksum import get_file_checksum
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
def mock_storage_service() -> AbstractStorageService:
    return create_autospec(AbstractStorageService)


@pytest.fixture
def mock_message_bus() -> AbstractMessageBus:
    return create_autospec(AbstractMessageBus)


class TestUploadVideo:
    @patch("core.video.application.use_cases.upload_video.get_file_checksum")
    def test_upload_video_media_to_video(
        self,
        mock_checksum,
        video: Video,
        video_repository: InMemoryVideoRepository,
        mock_storage_service: AbstractStorageService,
        mock_message_bus: AbstractMessageBus,
    ) -> None:
        mock_checksum.return_value = "test_checksum"

        upload_video: UploadVideo = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage_service,
            message_bus=mock_message_bus,
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

        mock_message_bus.handle.assert_called_once()

    def test_upload_video_media_not_found(
        self,
        video_repository: InMemoryVideoRepository,
        mock_storage_service: AbstractStorageService,
        mock_message_bus: AbstractMessageBus,
    ) -> None:
        upload_video: UploadVideo = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage_service,
            message_bus=mock_message_bus,
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

    @patch("core.video.application.use_cases.upload_video.get_file_checksum")
    def test_upload_video_updates_repository(
        self,
        mock_checksum,
        video: Video,
        video_repository: InMemoryVideoRepository,
        mock_storage_service: AbstractStorageService,
        mock_message_bus: AbstractMessageBus,
    ) -> None:
        mock_checksum.return_value = "checksum123"

        upload_video: UploadVideo = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage_service,
            message_bus=mock_message_bus,
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

    @patch("core.video.application.use_cases.upload_video.get_file_checksum")
    def test_upload_video_publishes_integration_event(
        self,
        mock_checksum,
        video: Video,
        video_repository: InMemoryVideoRepository,
        mock_storage_service: AbstractStorageService,
        mock_message_bus: AbstractMessageBus,
    ) -> None:
        mock_checksum.return_value = "checksum456"

        upload_video: UploadVideo = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage_service,
            message_bus=mock_message_bus,
        )

        input: UploadVideo.Input = UploadVideo.Input(
            video_id=video.id,
            file_name="upload.mp4",
            content=b"content",
            content_type="video/mp4",
        )

        upload_video.execute(input=input)

        mock_message_bus.handle.assert_called_once()
        call_args = mock_message_bus.handle.call_args[0][0]
        assert len(call_args) == 1
        assert isinstance(call_args[0], AudioVideoMediaUpdatedIntegrationEvent)
        assert call_args[0].resource_id == f"{video.id}.{MediaType.VIDEO}"
        assert call_args[0].file_path == f"videos/{video.id}/upload.mp4"

    def test_upload_video_calculates_real_checksum(
        self,
        video: Video,
        video_repository: InMemoryVideoRepository,
        mock_storage_service: AbstractStorageService,
        mock_message_bus: AbstractMessageBus,
        tmp_path,
    ) -> None:
        upload_video: UploadVideo = UploadVideo(
            video_repository=video_repository,
            storage_service=mock_storage_service,
            message_bus=mock_message_bus,
        )

        test_content = b"test_video_content_for_checksum"
        input: UploadVideo.Input = UploadVideo.Input(
            video_id=video.id,
            file_name="checksum_test.mp4",
            content=test_content,
            content_type="video/mp4",
        )

        # Create the actual file to calculate checksum
        file_path = tmp_path / "videos" / str(video.id) / "checksum_test.mp4"
        file_path.parent.mkdir(parents=True, exist_ok=True)
        file_path.write_bytes(test_content)

        with patch("core.video.application.use_cases.upload_video.Path") as mock_path:
            mock_path.return_value.__truediv__.return_value.__truediv__.return_value = (
                str(file_path)
            )
            upload_video.execute(input=input)

        updated_video = video_repository.get_by_id(video.id)
        assert updated_video.video is not None
        assert updated_video.video.checksum is not None
        assert len(updated_video.video.checksum) > 0

        # Verify checksum is consistent
        expected_checksum = get_file_checksum(str(file_path))
        assert updated_video.video.checksum == expected_checksum
