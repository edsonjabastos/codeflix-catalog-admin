import pytest
from decimal import Decimal
from uuid import UUID, uuid4
from core.video.domain.video import Video
from core.video.domain.value_objects import MediaType, Rating
from unittest.mock import patch
from core.video.domain.value_objects import (
    Rating,
    ImageMedia,
    AudioVideoMedia,
    MediaStatus,
)
from core.video.domain.events.event import AudioVideoMediaUpdated


@pytest.fixture
def valid_video_params() -> dict:
    return {
        "title": "Test Video",
        "description": "A test video description",
        "launch_year": 2023,
        "duration": Decimal("90.5"),
        "published": True,
        "rating": Rating.AGE_12,
        "categories": {uuid4(), uuid4()},
        "genres": {uuid4(), uuid4()},
        "cast_members": {uuid4(), uuid4()},
    }


@pytest.fixture
def image_media() -> ImageMedia:
    return ImageMedia(
        name="test_image.png",
        checksum="abc123",
        location="/images/test.png",
    )


@pytest.fixture
def audio_video_media() -> AudioVideoMedia:
    return AudioVideoMedia(
        name="test_video.mp4",
        checksum="abc123",
        raw_location="/videos/raw/test.mp4",
        encoded_location="/videos/encoded/test.mp4",
        status=MediaStatus.COMPLETED,
        media_type=MediaType.VIDEO,
    )


@pytest.fixture
def video(valid_video_params: dict) -> Video:
    return Video(**valid_video_params)


class TestVideoCreation:
    def test_video_creation_with_default_values(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)

        assert video.title == valid_video_params["title"]
        assert video.description == valid_video_params["description"]
        assert video.launch_year == valid_video_params["launch_year"]
        assert video.duration == valid_video_params["duration"]
        assert video.published == valid_video_params["published"]
        assert video.rating == valid_video_params["rating"]
        assert video.categories == valid_video_params["categories"]
        assert video.genres == valid_video_params["genres"]
        assert video.cast_members == valid_video_params["cast_members"]
        assert video.banner is None
        assert video.thumbnail is None
        assert video.thumbnail_half is None
        assert video.trailer is None
        assert video.video is None
        assert isinstance(video.id, UUID)

    def test_video_creation_with_custom_id(self, valid_video_params: dict) -> None:
        video_id: UUID = uuid4()
        video: Video = Video(id=video_id, **valid_video_params)

        assert video.id == video_id

    def test_empty_title_validation(self, valid_video_params: dict) -> None:
        valid_video_params["title"] = ""

        with pytest.raises(ValueError, match="title cannot be empty"):
            Video(**valid_video_params)

    def test_long_title_validation(self, valid_video_params: dict) -> None:
        valid_video_params["title"] = "a" * 256

        with pytest.raises(
            ValueError, match="title cannot be longer than 255 characters"
        ):
            Video(**valid_video_params)

    def test_empty_description_validation(self, valid_video_params: dict) -> None:
        valid_video_params["description"] = ""

        with pytest.raises(ValueError, match="description cannot be empty"):
            Video(**valid_video_params)

    def test_long_description_validation(self, valid_video_params: dict) -> None:
        valid_video_params["description"] = "a" * 1025

        with pytest.raises(
            ValueError, match="description cannot be longer than 1024 characters"
        ):
            Video(**valid_video_params)

    def test_launch_year_type_validation(self, valid_video_params: dict) -> None:
        valid_video_params["launch_year"] = "2023"

        with pytest.raises(ValueError, match="launch_year must be an integer"):
            Video(**valid_video_params)

    def test_duration_type_validation(self, valid_video_params: dict) -> None:
        valid_video_params["duration"] = 90.5

        with pytest.raises(ValueError, match="duration must be a decimal"):
            Video(**valid_video_params)

    def test_published_type_validation(self, valid_video_params: dict) -> None:
        valid_video_params["published"] = "True"

        with pytest.raises(ValueError, match="published must be a boolean"):
            Video(**valid_video_params)

    def test_rating_type_validation(self, valid_video_params: dict) -> None:
        valid_video_params["rating"] = "PG-13"

        with pytest.raises(ValueError, match="rating must be a Rating"):
            Video(**valid_video_params)

    def test_validate_called_on_creation(self, valid_video_params: dict) -> None:
        with patch.object(Video, "validate") as mock_validate:
            Video(**valid_video_params)
            mock_validate.assert_called_once()


class TestVideoUpdate:
    def test_update_video(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        new_title: str = "Updated Title"
        new_description: str = "Updated description"
        new_launch_year: int = 2024
        new_duration: Decimal = Decimal("120.5")
        new_published: bool = False
        new_rating: Rating = Rating.AGE_16

        video.update(
            new_title,
            new_description,
            new_launch_year,
            new_duration,
            new_published,
            new_rating,
        )

        assert video.title == new_title
        assert video.description == new_description
        assert video.launch_year == new_launch_year
        assert video.duration == new_duration
        assert video.published == new_published
        assert video.rating == new_rating

    def test_validate_called_on_update(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)

        with patch.object(video, "validate") as mock_validate:
            video.update(
                "Updated Title",
                "Updated description",
                2024,
                Decimal("120.5"),
                False,
                Rating.AGE_16,
            )
            mock_validate.assert_called_once()


class TestVideoCategories:
    def test_add_category(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        new_category_id: UUID = uuid4()

        assert new_category_id not in video.categories
        video.add_category(new_category_id)
        assert new_category_id in video.categories

    def test_remove_category(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        existing_category: UUID = next(iter(video.categories))

        video.remove_category(existing_category)
        assert existing_category not in video.categories

    def test_validate_called_on_add_category(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        new_category_id: UUID = uuid4()

        with patch.object(video, "validate") as mock_validate:
            video.add_category(new_category_id)
            mock_validate.assert_called_once()

    def test_validate_called_on_remove_category(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        existing_category: UUID = next(iter(video.categories))

        with patch.object(video, "validate") as mock_validate:
            video.remove_category(existing_category)
            mock_validate.assert_called_once()


class TestVideoGenres:
    def test_add_genre(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        new_genre_id: UUID = uuid4()

        assert new_genre_id not in video.genres
        video.add_genre(new_genre_id)
        assert new_genre_id in video.genres

    def test_remove_genre(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        existing_genre: UUID = next(iter(video.genres))

        video.remove_genre(existing_genre)
        assert existing_genre not in video.genres

    def test_validate_called_on_add_genre(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        new_genre_id: UUID = uuid4()

        with patch.object(video, "validate") as mock_validate:
            video.add_genre(new_genre_id)
            mock_validate.assert_called_once()

    def test_validate_called_on_remove_genre(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        existing_genre: UUID = next(iter(video.genres))

        with patch.object(video, "validate") as mock_validate:
            video.remove_genre(existing_genre)
            mock_validate.assert_called_once()


class TestVideoCastMembers:
    def test_add_cast_member(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        new_cast_member_id: UUID = uuid4()

        assert new_cast_member_id not in video.cast_members
        video.add_cast_member(new_cast_member_id)
        assert new_cast_member_id in video.cast_members

    def test_remove_cast_member(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        existing_cast_member: UUID = next(iter(video.cast_members))

        video.remove_cast_member(existing_cast_member)
        assert existing_cast_member not in video.cast_members

    def test_validate_called_on_add_cast_member(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        new_cast_member_id: UUID = uuid4()

        with patch.object(video, "validate") as mock_validate:
            video.add_cast_member(new_cast_member_id)
            mock_validate.assert_called_once()

    def test_validate_called_on_remove_cast_member(
        self, valid_video_params: dict
    ) -> None:
        video: Video = Video(**valid_video_params)
        existing_cast_member: UUID = next(iter(video.cast_members))

        with patch.object(video, "validate") as mock_validate:
            video.remove_cast_member(existing_cast_member)
            mock_validate.assert_called_once()


class TestVideoMedia:
    def test_update_banner(
        self, valid_video_params: dict, image_media: ImageMedia
    ) -> None:
        video: Video = Video(**valid_video_params)

        video.update_banner(image_media)
        assert video.banner == image_media

    def test_update_thumbnail(
        self, valid_video_params: dict, image_media: ImageMedia
    ) -> None:
        video: Video = Video(**valid_video_params)

        video.update_thumbnail(image_media)
        assert video.thumbnail == image_media

    def test_update_thumbnail_half(
        self, valid_video_params: dict, image_media: ImageMedia
    ) -> None:
        video: Video = Video(**valid_video_params)

        video.update_thumbnail_half(image_media)
        assert video.thumbnail_half == image_media

    def test_update_trailer(
        self, valid_video_params: dict, audio_video_media: AudioVideoMedia
    ) -> None:
        video: Video = Video(**valid_video_params)

        video.update_trailer(audio_video_media)
        assert video.trailer == audio_video_media

    def test_update_video(
        self, valid_video_params: dict, audio_video_media: AudioVideoMedia
    ) -> None:
        video: Video = Video(**valid_video_params)

        video.update_video(audio_video_media)
        assert video.video == audio_video_media

    def test_update_video_and_dispactch_event(
        self, video: Video, audio_video_media: AudioVideoMedia
    ) -> None:
        video.update_video(audio_video_media)
        assert video.video == audio_video_media
        assert video.events == [
            AudioVideoMediaUpdated(
                aggregate_id=video.id,
                file_path=audio_video_media.raw_location,
                media_type=MediaType.VIDEO,
            )
        ]


class TestVideoString:
    def test_str_representation(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        expected_str: str = f"{video.title} - {video.description} ({video.launch_year})"

        assert str(video) == expected_str

    def test_repr_representation(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        expected_repr: str = f"<Video {video.title} ({video.id})>"

        assert repr(video) == expected_repr


class TestVideoEquality:
    def test_equal_videos_with_same_id(self, valid_video_params: dict) -> None:
        video_id: UUID = uuid4()
        video1: Video = Video(id=video_id, **valid_video_params)
        video2: Video = Video(id=video_id, **valid_video_params)

        assert video1 == video2

    def test_equality_with_different_class(self, valid_video_params: dict) -> None:
        class FakeVideo: ...

        common_id: UUID = uuid4()
        video: Video = Video(id=common_id, **valid_video_params)
        fake_video = FakeVideo()
        fake_video.id = common_id

        assert video != fake_video


class TestVideoPublish:
    def test_publish_success_when_video_is_completed(
        self, valid_video_params: dict
    ) -> None:
        video: Video = Video(**valid_video_params)
        completed_video_media: AudioVideoMedia = AudioVideoMedia(
            name="test_video.mp4",
            checksum="abc123",
            raw_location="/videos/raw/test.mp4",
            encoded_location="/videos/encoded/test.mp4",
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )
        video.update_video(completed_video_media)

        assert video.published is True
        video.publish()

        assert video.published is True

    def test_publish_fails_when_no_video_media(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)

        assert video.video is None

        with pytest.raises(
            ValueError, match="Video media is required to publish the video"
        ):
            video.publish()

    def test_publish_fails_when_video_not_completed(
        self, valid_video_params: dict
    ) -> None:
        video: Video = Video(**valid_video_params)
        pending_video_media: AudioVideoMedia = AudioVideoMedia(
            name="test_video.mp4",
            checksum="abc123",
            raw_location="/videos/raw/test.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO,
        )
        video.update_video(pending_video_media)

        with pytest.raises(
            ValueError, match="Video media must be completed to publish the video"
        ):
            video.publish()

    def test_validate_called_on_publish(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        completed_video_media = AudioVideoMedia(
            name="test_video.mp4",
            checksum="abc123",
            raw_location="/videos/raw/test.mp4",
            encoded_location="/videos/encoded/test.mp4",
            status=MediaStatus.COMPLETED,
            media_type=MediaType.VIDEO,
        )
        video.update_video(completed_video_media)

        with patch.object(video, "validate") as mock_validate:
            video.publish()
            mock_validate.assert_called_once()


class TestVideoProcess:
    def test_process_with_completed_status(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        initial_video_media = AudioVideoMedia(
            name="test_video.mp4",
            checksum="abc123",
            raw_location="/videos/raw/test.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO,
        )
        video.update_video(initial_video_media)

        encoded_location = "/videos/encoded/test.mp4"
        video.process(MediaStatus.COMPLETED, encoded_location, MediaType.VIDEO)

        assert video.video.status == MediaStatus.COMPLETED
        assert video.video.encoded_location == encoded_location
        assert video.published is True

    def test_process_with_error_status(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        initial_video_media = AudioVideoMedia(
            name="test_video.mp4",
            checksum="abc123",
            raw_location="/videos/raw/test.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO,
        )
        video.update_video(initial_video_media)

        video.process(MediaStatus.ERROR, "", MediaType.VIDEO)

        assert video.video.status == MediaStatus.ERROR
        assert video.video.encoded_location == ""
        assert video.published is True  # Was already True from initial creation

    def test_process_calls_publish_when_completed(
        self, valid_video_params: dict
    ) -> None:
        video: Video = Video(**valid_video_params)
        initial_video_media = AudioVideoMedia(
            name="test_video.mp4",
            checksum="abc123",
            raw_location="/videos/raw/test.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO,
        )
        video.update_video(initial_video_media)

        with patch.object(video, "publish") as mock_publish:
            encoded_location = "/videos/encoded/test.mp4"
            video.process(MediaStatus.COMPLETED, encoded_location, MediaType.VIDEO)
            mock_publish.assert_called_once()

    def test_validate_called_on_process(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        initial_video_media = AudioVideoMedia(
            name="test_video.mp4",
            checksum="abc123",
            raw_location="/videos/raw/test.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO,
        )
        video.update_video(initial_video_media)

        with patch.object(video, "validate") as mock_validate:
            encoded_location = "/videos/encoded/test.mp4"
            video.process(MediaStatus.COMPLETED, encoded_location, MediaType.VIDEO)
            # Called twice: once in process, once in publish
            assert mock_validate.call_count == 2

    def test_process_updates_video_properties_correctly(
        self, valid_video_params: dict
    ) -> None:
        video: Video = Video(**valid_video_params)
        initial_video_media = AudioVideoMedia(
            name="test_video.mp4",
            checksum="abc123",
            raw_location="/videos/raw/test.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.VIDEO,
        )
        video.update_video(initial_video_media)

        encoded_location = "/videos/encoded/test.mp4"
        video.process(MediaStatus.COMPLETED, encoded_location, MediaType.VIDEO)

        assert video.video.name == "test_video.mp4"
        assert video.video.checksum == "abc123"
        assert video.video.raw_location == "/videos/raw/test.mp4"
        assert video.video.media_type == MediaType.VIDEO

    def test_process_trailer_with_completed_status(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        initial_trailer_media = AudioVideoMedia(
            name="test_trailer.mp4",
            checksum="xyz789",
            raw_location="/videos/raw/test_trailer.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.TRAILER,
        )
        video.update_trailer(initial_trailer_media)

        encoded_location = "/videos/encoded/test_trailer.mp4"
        video.process(MediaStatus.COMPLETED, encoded_location, MediaType.TRAILER)

        assert video.trailer.status == MediaStatus.COMPLETED
        assert video.trailer.encoded_location == encoded_location

    def test_process_trailer_with_error_status(self, valid_video_params: dict) -> None:
        video: Video = Video(**valid_video_params)
        initial_trailer_media = AudioVideoMedia(
            name="test_trailer.mp4",
            checksum="xyz789",
            raw_location="/videos/raw/test_trailer.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.TRAILER,
        )
        video.update_trailer(initial_trailer_media)

        video.process(MediaStatus.ERROR, "", MediaType.TRAILER)

        assert video.trailer.status == MediaStatus.ERROR
        assert video.trailer.encoded_location == ""

    def test_process_trailer_does_not_publish(self, valid_video_params: dict) -> None:
        valid_video_params["published"] = False
        video: Video = Video(**valid_video_params)
        initial_trailer_media = AudioVideoMedia(
            name="test_trailer.mp4",
            checksum="xyz789",
            raw_location="/videos/raw/test_trailer.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.TRAILER,
        )
        video.update_trailer(initial_trailer_media)

        encoded_location = "/videos/encoded/test_trailer.mp4"
        video.process(MediaStatus.COMPLETED, encoded_location, MediaType.TRAILER)

        assert video.published is False  # Should remain False, not auto-published

    def test_process_trailer_updates_trailer_properties_correctly(
        self, valid_video_params: dict
    ) -> None:
        video: Video = Video(**valid_video_params)
        initial_trailer_media = AudioVideoMedia(
            name="test_trailer.mp4",
            checksum="xyz789",
            raw_location="/videos/raw/test_trailer.mp4",
            encoded_location="",
            status=MediaStatus.PENDING,
            media_type=MediaType.TRAILER,
        )
        video.update_trailer(initial_trailer_media)

        encoded_location = "/videos/encoded/test_trailer.mp4"
        video.process(MediaStatus.COMPLETED, encoded_location, MediaType.TRAILER)

        assert video.trailer.name == "test_trailer.mp4"
        assert video.trailer.checksum == "xyz789"
        assert video.trailer.raw_location == "/videos/raw/test_trailer.mp4"
        assert video.trailer.media_type == MediaType.TRAILER
