import pytest
from decimal import Decimal
from uuid import UUID, uuid4
from unittest.mock import patch
from core.video.domain.video import Video
from core.video.domain.value_objects import Rating


class TestVideo:
    def test_video_instantiation_with_valid_data(self) -> None:
        video: Video = Video(
            title="Test Video",
            description="A test video description",
            launch_year=2023,
            duration=Decimal("90.5"),
            published=False,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        assert video.title == "Test Video"
        assert video.description == "A test video description"
        assert video.launch_year == 2023
        assert video.duration == Decimal("90.5")
        assert video.published is False
        assert video.rating == Rating.L
        assert video.categories == set()
        assert video.genres == set()
        assert video.cast_members == set()
        assert isinstance(video.id, UUID)

    def test_video_with_custom_id_and_sets(self) -> None:
        video_id: UUID = uuid4()
        category_id: UUID = uuid4()
        genre_id: UUID = uuid4()
        cast_member_id: UUID = uuid4()

        video: Video = Video(
            id=video_id,
            title="Custom Video",
            description="A video with custom ID and sets",
            launch_year=2023,
            duration=Decimal("120"),
            published=True,
            rating=Rating.AGE_16,
            categories={category_id},
            genres={genre_id},
            cast_members={cast_member_id},
        )

        assert video.id == video_id
        assert category_id in video.categories
        assert genre_id in video.genres
        assert cast_member_id in video.cast_members

    def test_video_str_representation(self) -> None:
        video: Video = Video(
            title="Test Video",
            description="A test video description",
            launch_year=2023,
            duration=Decimal("90.5"),
            published=False,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        assert str(video) == "Test Video - A test video description (2023)"

    def test_video_repr_representation(self) -> None:
        video_id: UUID = uuid4()
        video: Video = Video(
            id=video_id,
            title="Test Video",
            description="A test video description",
            launch_year=2023,
            duration=Decimal("90.5"),
            published=False,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        assert repr(video) == f"<Video Test Video ({video_id})>"


class TestVideoValidation:
    def test_empty_title_raises_error(self) -> None:
        with pytest.raises(ValueError, match="title cannot be empty"):
            Video(
                title="",
                description="Description",
                launch_year=2023,
                duration=Decimal("90"),
                published=True,
                rating=Rating.L,
                categories=set(),
                genres=set(),
                cast_members=set(),
            )

    def test_title_too_long_raises_error(self) -> None:
        with pytest.raises(
            ValueError, match="title cannot be longer than 255 characters"
        ):
            Video(
                title="a" * 256,
                description="Description",
                launch_year=2023,
                duration=Decimal("90"),
                published=True,
                rating=Rating.L,
                categories=set(),
                genres=set(),
                cast_members=set(),
            )

    def test_empty_description_raises_error(self) -> None:
        with pytest.raises(ValueError, match="description cannot be empty"):
            Video(
                title="Title",
                description="",
                launch_year=2023,
                duration=Decimal("90"),
                published=True,
                rating=Rating.L,
                categories=set(),
                genres=set(),
                cast_members=set(),
            )

    def test_description_too_long_raises_error(self) -> None:
        with pytest.raises(
            ValueError, match="description cannot be longer than 1024 characters"
        ):
            Video(
                title="Title",
                description="a" * 1025,
                launch_year=2023,
                duration=Decimal("90"),
                published=True,
                rating=Rating.L,
                categories=set(),
                genres=set(),
                cast_members=set(),
            )

    def test_non_integer_launch_year_raises_error(self) -> None:
        with pytest.raises(ValueError, match="launch_year must be an integer"):
            Video(
                title="Title",
                description="Description",
                launch_year="2023",  # type: ignore
                duration=Decimal("90"),
                published=True,
                rating=Rating.L,
                categories=set(),
                genres=set(),
                cast_members=set(),
            )

    def test_non_decimal_duration_raises_error(self) -> None:
        with pytest.raises(ValueError, match="duration must be a decimal"):
            Video(
                title="Title",
                description="Description",
                launch_year=2023,
                duration=90,  # type: ignore
                published=True,
                rating=Rating.L,
                categories=set(),
                genres=set(),
                cast_members=set(),
            )

    def test_non_boolean_published_raises_error(self) -> None:
        with pytest.raises(ValueError, match="published must be a boolean"):
            Video(
                title="Title",
                description="Description",
                launch_year=2023,
                duration=Decimal("90"),
                published="true",  # type: ignore
                rating=Rating.L,
                categories=set(),
                genres=set(),
                cast_members=set(),
            )

    def test_non_rating_enum_raises_error(self) -> None:
        with pytest.raises(ValueError, match="rating must be a Rating"):
            Video(
                title="Title",
                description="Description",
                launch_year=2023,
                duration=Decimal("90"),
                published=True,
                rating="PG-13",  # type: ignore
                categories=set(),
                genres=set(),
                cast_members=set(),
            )


class TestVideoEquality:
    def test_videos_with_same_id_are_equal(self) -> None:
        video_id: UUID = uuid4()
        video1: Video = Video(
            id=video_id,
            title="Video 1",
            description="Description 1",
            launch_year=2023,
            duration=Decimal("90"),
            published=True,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        video2: Video = Video(
            id=video_id,
            title="Video 1",
            description="Description 1",
            launch_year=2023,
            duration=Decimal("90"),
            published=True,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        assert video1 == video2

    def test_equality_with_different_class(self) -> None:
        class FakeVideo:
            pass

        common_id: UUID = uuid4()
        video: Video = Video(
            id=common_id,
            title="Video",
            description="Description",
            launch_year=2023,
            duration=Decimal("90"),
            published=True,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        fake_video = FakeVideo()
        fake_video.id = common_id

        assert video != fake_video
