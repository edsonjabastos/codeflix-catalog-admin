from decimal import Decimal
from unittest.mock import MagicMock, patch
from uuid import uuid4, UUID
import pytest
from core.video.application.exceptions import VideoNotFound, AudioVideoMediaNotFound
from core.video.application.use_cases.process_audio_video_media import (
    ProcessAudioVideoMedia,
)
from core.video.domain.value_objects import (
    Rating,
    MediaStatus,
    MediaType,
    AudioVideoMedia,
)
from core.video.domain.video import Video
from core.video.domain.video_repository import VideoRepository


@pytest.fixture
def video_repository() -> MagicMock:
    return MagicMock(spec=VideoRepository)


@pytest.fixture
def video_with_media() -> Video:
    video = Video(
        title="Test Video",
        description="Test Description",
        launch_year=2023,
        duration=Decimal("120.5"),
        published=True,
        rating=Rating.L,
        categories=set(),
        genres=set(),
        cast_members=set(),
    )
    # Add video media to the video
    video.update_video(
        AudioVideoMedia(
            name="test_video.mp4",
            checksum="abc123",
            raw_location="/videos/raw/test.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO,
        )
    )
    return video


@pytest.fixture
def video_without_media() -> Video:
    return Video(
        title="Test Video Without Media",
        description="Test Description",
        launch_year=2023,
        duration=Decimal("90.5"),
        published=False,
        rating=Rating.AGE_12,
        categories=set(),
        genres=set(),
        cast_members=set(),
    )


@pytest.fixture
def use_case(video_repository: MagicMock) -> ProcessAudioVideoMedia:
    return ProcessAudioVideoMedia(video_repository=video_repository)


class TestProcessAudioVideoMedia:
    def test_process_video_with_completed_status(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: MagicMock,
        video_with_media: Video,
    ) -> None:
        video_id = video_with_media.id
        video_repository.get_by_id.return_value = video_with_media

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location="/videos/encoded/test.mp4",
            status=MediaStatus.COMPLETED,
        )

        use_case.execute(input_data)

        video_repository.get_by_id.assert_called_once_with(id=video_id)
        video_repository.update.assert_called_once_with(video_with_media)
        assert video_with_media.video.status == MediaStatus.COMPLETED
        assert video_with_media.video.encoded_location == "/videos/encoded/test.mp4"
        assert video_with_media.published is True

    def test_process_video_with_error_status(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: MagicMock,
        video_with_media: Video,
    ) -> None:
        video_id = video_with_media.id
        video_repository.get_by_id.return_value = video_with_media

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location="",
            status=MediaStatus.ERROR,
        )

        use_case.execute(input_data)

        video_repository.get_by_id.assert_called_once_with(id=video_id)
        video_repository.update.assert_called_once_with(video_with_media)
        assert video_with_media.video.status == MediaStatus.ERROR
        assert video_with_media.video.encoded_location == ""

    def test_process_video_not_found(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: MagicMock,
    ) -> None:
        video_id = uuid4()
        video_repository.get_by_id.return_value = None

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location="/videos/encoded/test.mp4",
            status=MediaStatus.COMPLETED,
        )

        with pytest.raises(VideoNotFound) as exc_info:
            use_case.execute(input_data)

        assert f"Video with id {video_id} not found" in str(exc_info.value)
        video_repository.get_by_id.assert_called_once_with(id=video_id)
        video_repository.update.assert_not_called()

    def test_process_video_media_not_found(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: MagicMock,
        video_without_media: Video,
    ) -> None:
        video_id = video_without_media.id
        video_repository.get_by_id.return_value = video_without_media

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location="/videos/encoded/test.mp4",
            status=MediaStatus.COMPLETED,
        )

        with pytest.raises(AudioVideoMediaNotFound) as exc_info:
            use_case.execute(input_data)

        assert f"Video media not found for video id {video_id}" in str(exc_info.value)
        video_repository.get_by_id.assert_called_once_with(id=video_id)
        video_repository.update.assert_not_called()

    def test_process_calls_video_process_method(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: MagicMock,
        video_with_media: Video,
    ) -> None:
        video_id = video_with_media.id
        video_repository.get_by_id.return_value = video_with_media
        encoded_location = "/videos/encoded/output.mp4"

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location=encoded_location,
            status=MediaStatus.COMPLETED,
        )

        with patch.object(video_with_media, "process") as mock_process:
            use_case.execute(input_data)
            mock_process.assert_called_once_with(
                status=MediaStatus.COMPLETED,
                encoded_location=encoded_location,
            )

    def test_process_updates_repository(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: MagicMock,
        video_with_media: Video,
    ) -> None:
        video_id = video_with_media.id
        video_repository.get_by_id.return_value = video_with_media

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location="/videos/encoded/test.mp4",
            status=MediaStatus.COMPLETED,
        )

        use_case.execute(input_data)

        video_repository.update.assert_called_once()
        call_args = video_repository.update.call_args[0][0]
        assert isinstance(call_args, Video)
        assert call_args.id == video_id

    def test_process_only_handles_video_media_type(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: MagicMock,
        video_with_media: Video,
    ) -> None:
        video_id = video_with_media.id
        video_repository.get_by_id.return_value = video_with_media

        # Test with TRAILER media type (should not process)
        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.TRAILER,
            encoded_location="/videos/encoded/trailer.mp4",
            status=MediaStatus.COMPLETED,
        )

        use_case.execute(input_data)

        # Should not call update since media_type is not VIDEO
        video_repository.get_by_id.assert_called_once_with(id=video_id)
        video_repository.update.assert_not_called()

    def test_process_preserves_video_properties(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: MagicMock,
        video_with_media: Video,
    ) -> None:
        video_id = video_with_media.id
        original_title = video_with_media.title
        original_description = video_with_media.description
        original_checksum = video_with_media.video.checksum
        original_name = video_with_media.video.name

        video_repository.get_by_id.return_value = video_with_media

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location="/videos/encoded/test.mp4",
            status=MediaStatus.COMPLETED,
        )

        use_case.execute(input_data)

        # Verify video properties are preserved
        assert video_with_media.title == original_title
        assert video_with_media.description == original_description
        assert video_with_media.video.checksum == original_checksum
        assert video_with_media.video.name == original_name
