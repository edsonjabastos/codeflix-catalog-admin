from decimal import Decimal
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
from core.video.infra.in_memory_video_repository import InMemoryVideoRepository


@pytest.fixture
def video_repository() -> InMemoryVideoRepository:
    return InMemoryVideoRepository()


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
def video_with_trailer() -> Video:
    video = Video(
        title="Test Video",
        description="Test Description",
        launch_year=2023,
        duration=Decimal("120.5"),
        published=False,
        rating=Rating.L,
        categories=set(),
        genres=set(),
        cast_members=set(),
    )
    # Add trailer media to the video
    video.update_trailer(
        AudioVideoMedia(
            name="test_trailer.mp4",
            checksum="xyz789",
            raw_location="/videos/raw/test_trailer.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.TRAILER,
        )
    )
    return video


@pytest.fixture
def use_case(video_repository: InMemoryVideoRepository) -> ProcessAudioVideoMedia:
    return ProcessAudioVideoMedia(video_repository=video_repository)


class TestProcessAudioVideoMediaIntegration:
    def test_process_video_with_completed_status(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: InMemoryVideoRepository,
        video_with_media: Video,
    ) -> None:
        video_id = video_with_media.id
        video_repository.save(video_with_media)

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location="/videos/encoded/test.mp4",
            status=MediaStatus.COMPLETED,
        )

        use_case.execute(input_data)

        # Verify video was updated in repository
        updated_video = video_repository.get_by_id(video_id)
        assert updated_video is not None
        assert updated_video.video.status == MediaStatus.COMPLETED
        assert updated_video.video.encoded_location == "/videos/encoded/test.mp4"
        assert updated_video.published is True

    def test_process_video_with_error_status(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: InMemoryVideoRepository,
        video_with_media: Video,
    ) -> None:
        video_id = video_with_media.id
        video_repository.save(video_with_media)

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location="",
            status=MediaStatus.ERROR,
        )

        use_case.execute(input_data)

        # Verify video was updated in repository
        updated_video = video_repository.get_by_id(video_id)
        assert updated_video is not None
        assert updated_video.video.status == MediaStatus.ERROR
        assert updated_video.video.encoded_location == ""
        # Video should still be published because it was already True initially
        assert updated_video.published is True

    def test_process_video_not_found(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: InMemoryVideoRepository,
    ) -> None:
        video_id = uuid4()

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location="/videos/encoded/test.mp4",
            status=MediaStatus.COMPLETED,
        )

        with pytest.raises(VideoNotFound) as exc_info:
            use_case.execute(input_data)

        assert f"Video with id {video_id} not found" in str(exc_info.value)

    def test_process_video_media_not_found(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: InMemoryVideoRepository,
        video_without_media: Video,
    ) -> None:
        video_id = video_without_media.id
        video_repository.save(video_without_media)

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location="/videos/encoded/test.mp4",
            status=MediaStatus.COMPLETED,
        )

        with pytest.raises(AudioVideoMediaNotFound) as exc_info:
            use_case.execute(input_data)

        assert f"Video media not found for video id {video_id}" in str(exc_info.value)

    def test_process_updates_existing_video_in_repository(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: InMemoryVideoRepository,
        video_with_media: Video,
    ) -> None:
        video_id = video_with_media.id
        video_repository.save(video_with_media)

        # Verify initial state
        initial_video = video_repository.get_by_id(video_id)
        assert initial_video.video.status == MediaStatus.PENDING
        assert initial_video.video.encoded_location == ""

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location="/videos/encoded/completed.mp4",
            status=MediaStatus.COMPLETED,
        )

        use_case.execute(input_data)

        # Verify updated state
        updated_video = video_repository.get_by_id(video_id)
        assert updated_video.video.status == MediaStatus.COMPLETED
        assert updated_video.video.encoded_location == "/videos/encoded/completed.mp4"
        assert updated_video.published is True

    def test_process_preserves_video_metadata(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: InMemoryVideoRepository,
        video_with_media: Video,
    ) -> None:
        video_id = video_with_media.id
        original_title = video_with_media.title
        original_description = video_with_media.description
        original_launch_year = video_with_media.launch_year
        original_duration = video_with_media.duration
        original_rating = video_with_media.rating

        video_repository.save(video_with_media)

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location="/videos/encoded/test.mp4",
            status=MediaStatus.COMPLETED,
        )

        use_case.execute(input_data)

        # Verify all metadata is preserved
        updated_video = video_repository.get_by_id(video_id)
        assert updated_video.title == original_title
        assert updated_video.description == original_description
        assert updated_video.launch_year == original_launch_year
        assert updated_video.duration == original_duration
        assert updated_video.rating == original_rating

    def test_process_preserves_video_media_metadata(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: InMemoryVideoRepository,
        video_with_media: Video,
    ) -> None:
        video_id = video_with_media.id
        original_name = video_with_media.video.name
        original_checksum = video_with_media.video.checksum
        original_raw_location = video_with_media.video.raw_location
        original_media_type = video_with_media.video.media_type

        video_repository.save(video_with_media)

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.VIDEO,
            encoded_location="/videos/encoded/test.mp4",
            status=MediaStatus.COMPLETED,
        )

        use_case.execute(input_data)

        # Verify video media metadata is preserved
        updated_video = video_repository.get_by_id(video_id)
        assert updated_video.video.name == original_name
        assert updated_video.video.checksum == original_checksum
        assert updated_video.video.raw_location == original_raw_location
        assert updated_video.video.media_type == original_media_type

    def test_process_only_affects_target_video(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: InMemoryVideoRepository,
        video_with_media: Video,
    ) -> None:
        # Create and save two videos
        video1 = video_with_media
        video2 = Video(
            title="Another Video",
            description="Another Description",
            launch_year=2024,
            duration=Decimal("100.0"),
            published=False,
            rating=Rating.AGE_16,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video2.update_video(
            AudioVideoMedia(
                name="another_video.mp4",
                checksum="xyz789",
                raw_location="/videos/raw/another.mp4",
                encoded_location="",
                status=MediaStatus.PENDING,
                media_type=MediaType.VIDEO,
            )
        )

        video_repository.save(video1)
        video_repository.save(video2)

        # Process only video1
        input_data = ProcessAudioVideoMedia.Input(
            video_id=video1.id,
            media_type=MediaType.VIDEO,
            encoded_location="/videos/encoded/video1.mp4",
            status=MediaStatus.COMPLETED,
        )

        use_case.execute(input_data)

        # Verify video1 was updated
        updated_video1 = video_repository.get_by_id(video1.id)
        assert updated_video1.video.status == MediaStatus.COMPLETED
        assert updated_video1.published is True

        # Verify video2 was NOT affected
        untouched_video2 = video_repository.get_by_id(video2.id)
        assert untouched_video2.video.status == MediaStatus.PENDING
        assert untouched_video2.published is False

    def test_process_trailer_with_completed_status(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: InMemoryVideoRepository,
        video_with_trailer: Video,
    ) -> None:
        video_id = video_with_trailer.id
        video_repository.save(video_with_trailer)

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.TRAILER,
            encoded_location="/videos/encoded/test_trailer.mp4",
            status=MediaStatus.COMPLETED,
        )

        use_case.execute(input_data)

        # Verify trailer was updated in repository
        updated_video = video_repository.get_by_id(video_id)
        assert updated_video is not None
        assert updated_video.trailer.status == MediaStatus.COMPLETED
        assert updated_video.trailer.encoded_location == "/videos/encoded/test_trailer.mp4"
        # Video should remain unpublished
        assert updated_video.published is False

    def test_process_trailer_updates_existing_trailer_in_repository(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: InMemoryVideoRepository,
        video_with_trailer: Video,
    ) -> None:
        video_id = video_with_trailer.id
        original_checksum = video_with_trailer.trailer.checksum
        original_name = video_with_trailer.trailer.name
        video_repository.save(video_with_trailer)

        input_data = ProcessAudioVideoMedia.Input(
            video_id=video_id,
            media_type=MediaType.TRAILER,
            encoded_location="/videos/encoded/test_trailer.mp4",
            status=MediaStatus.COMPLETED,
        )

        use_case.execute(input_data)

        # Verify trailer metadata was preserved
        updated_video = video_repository.get_by_id(video_id)
        assert updated_video.trailer.checksum == original_checksum
        assert updated_video.trailer.name == original_name
        assert updated_video.trailer.raw_location == "/videos/raw/test_trailer.mp4"
        assert updated_video.trailer.media_type == MediaType.TRAILER

    def test_process_trailer_does_not_affect_main_video(
        self,
        use_case: ProcessAudioVideoMedia,
        video_repository: InMemoryVideoRepository,
    ) -> None:
        # Create a video with both video and trailer
        video = Video(
            title="Test Video",
            description="Test Description",
            launch_year=2023,
            duration=Decimal("120.5"),
            published=False,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video.update_video(
            AudioVideoMedia(
                name="main_video.mp4",
                checksum="main123",
                raw_location="/videos/raw/main.mp4",
                encoded_location="",
                status=MediaStatus.PENDING,
                media_type=MediaType.VIDEO,
            )
        )
        video.update_trailer(
            AudioVideoMedia(
                name="trailer.mp4",
                checksum="trailer123",
                raw_location="/videos/raw/trailer.mp4",
                encoded_location="",
                status=MediaStatus.PENDING,
                media_type=MediaType.TRAILER,
            )
        )
        video_repository.save(video)

        # Process only the trailer
        input_data = ProcessAudioVideoMedia.Input(
            video_id=video.id,
            media_type=MediaType.TRAILER,
            encoded_location="/videos/encoded/trailer.mp4",
            status=MediaStatus.COMPLETED,
        )

        use_case.execute(input_data)

        # Verify trailer was updated
        updated_video = video_repository.get_by_id(video.id)
        assert updated_video.trailer.status == MediaStatus.COMPLETED
        assert updated_video.trailer.encoded_location == "/videos/encoded/trailer.mp4"

        # Verify main video was NOT affected
        assert updated_video.video.status == MediaStatus.PENDING
        assert updated_video.video.encoded_location == ""
        assert updated_video.published is False
