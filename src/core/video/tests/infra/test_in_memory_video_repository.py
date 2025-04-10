import pytest
from decimal import Decimal
from uuid import uuid4, UUID
from core.video.domain.video import Video
from core.video.domain.value_objects import Rating
from core.video.infra.in_memory_video_repository import InMemoryVideoRepository


@pytest.fixture
def video_repository() -> InMemoryVideoRepository:
    return InMemoryVideoRepository()


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


class TestSaveInMemoryVideoRepository:
    def test_can_save_video(
        self, video_repository: InMemoryVideoRepository, video: Video
    ) -> None:
        result = video_repository.save(video)

        assert result is None
        assert len(video_repository.videos) == 1
        assert video_repository.videos[0] == video

    def test_can_save_multiple_videos(
        self, video_repository: InMemoryVideoRepository
    ) -> None:
        video1 = Video(
            title="Test Video 1",
            description="Test Description 1",
            launch_year=2021,
            duration=Decimal("120.5"),
            published=True,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video2 = Video(
            title="Test Video 2",
            description="Test Description 2",
            launch_year=2022,
            duration=Decimal("130.5"),
            published=False,
            rating=Rating.AGE_10,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        video_repository.save(video1)
        video_repository.save(video2)

        assert len(video_repository.videos) == 2
        assert video_repository.videos[0] == video1
        assert video_repository.videos[1] == video2


class TestGetByIdInMemoryVideoRepository:
    def test_can_get_video_by_id(
        self, video_repository: InMemoryVideoRepository, video: Video
    ) -> None:
        video_repository.save(video)

        video_found = video_repository.get_by_id(video.id)

        assert video_found == video

    def test_return_none_when_video_not_found(
        self, video_repository: InMemoryVideoRepository
    ) -> None:
        video_found = video_repository.get_by_id(
            UUID("123e4567-e89b-12d3-a456-426614174000")
        )

        assert video_found is None


class TestDeleteInMemoryVideoRepository:
    def test_can_delete_video(
        self, video_repository: InMemoryVideoRepository, video: Video
    ) -> None:
        video_repository.save(video)

        result = video_repository.delete(video.id)

        assert result is None
        assert len(video_repository.videos) == 0
        assert video_repository.get_by_id(video.id) is None

    def test_do_nothing_when_video_not_found(
        self, video_repository: InMemoryVideoRepository
    ) -> None:
        id: UUID = uuid4()

        result = video_repository.delete(id)

        assert result is None
        assert len(video_repository.videos) == 0


class TestUpdateInMemoryVideoRepository:
    def test_can_update_video(
        self, video_repository: InMemoryVideoRepository, video: Video
    ) -> None:
        video_repository.save(video)

        video.title = "Updated Title"
        video.description = "Updated Description"
        result = video_repository.update(video)

        assert result is None
        updated_video = video_repository.get_by_id(video.id)
        assert updated_video is not None
        assert updated_video.title == "Updated Title"
        assert updated_video.description == "Updated Description"

    def test_do_nothing_when_video_not_found(
        self, video_repository: InMemoryVideoRepository
    ) -> None:
        video = Video(
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

        result = video_repository.update(video)

        assert result is None
        assert len(video_repository.videos) == 0


class TestListInMemoryVideoRepository:
    def test_returns_empty_list_when_no_videos(
        self, video_repository: InMemoryVideoRepository
    ) -> None:
        videos = video_repository.list()

        assert len(videos) == 0

    def test_returns_all_videos(
        self, video_repository: InMemoryVideoRepository
    ) -> None:
        video1 = Video(
            title="Test Video 1",
            description="Test Description 1",
            launch_year=2021,
            duration=Decimal("120.5"),
            published=True,
            rating=Rating.L,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )
        video2 = Video(
            title="Test Video 2",
            description="Test Description 2",
            launch_year=2022,
            duration=Decimal("130.5"),
            published=False,
            rating=Rating.AGE_10,
            categories=set(),
            genres=set(),
            cast_members=set(),
        )

        video_repository.save(video1)
        video_repository.save(video2)

        videos = video_repository.list()

        assert len(videos) == 2
        assert video1 in videos
        assert video2 in videos
