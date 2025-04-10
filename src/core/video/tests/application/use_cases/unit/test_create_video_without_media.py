from decimal import Decimal
from unittest.mock import MagicMock
from uuid import UUID, uuid4
import pytest
from core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound
from core.video.application.use_cases.create_video_without_media import CreateVideoWithoutMedia
from core.video.domain.value_objects import Rating
from core.video.domain.video_repository import VideoRepository
from core.category.domain.category_repository import CategoryRepository
from core.genre.domain.genre_repository import GenreRepository
from core.castmember.domain.castmember_repository import CastMemberRepository

@pytest.fixture
def video_repository() -> MagicMock:
    return MagicMock(spec=VideoRepository)


@pytest.fixture
def category_repository() -> MagicMock:
    return MagicMock(spec=CategoryRepository)


@pytest.fixture
def genre_repository() -> MagicMock:
    return MagicMock(spec=GenreRepository)


@pytest.fixture
def cast_member_repository() -> MagicMock:
    return MagicMock(spec=CastMemberRepository)


@pytest.fixture
def use_case(
    video_repository: MagicMock,
    category_repository: MagicMock,
    genre_repository: MagicMock,
    cast_member_repository: MagicMock,
) -> CreateVideoWithoutMedia:
    return CreateVideoWithoutMedia(
        video_repository=video_repository,
        category_repository=category_repository,
        genre_repository=genre_repository,
        cast_member_repository=cast_member_repository,
    )


@pytest.fixture
def valid_categories_ids() -> set[UUID]:
    return {uuid4(), uuid4()}


@pytest.fixture
def valid_genres_ids() -> set[UUID]:
    return {uuid4(), uuid4()}


@pytest.fixture
def valid_cast_members_ids() -> set[UUID]:
    return {uuid4(), uuid4()}


@pytest.fixture
def valid_input(
    valid_categories_ids: set[UUID],
    valid_genres_ids: set[UUID],
    valid_cast_members_ids: set[UUID],
) -> CreateVideoWithoutMedia.Input:
    return CreateVideoWithoutMedia.Input(
        title="Test Video",
        description="Test Description",
        launch_year=2023,
        duration=Decimal("90.5"),
        rating=Rating.L,
        categories=valid_categories_ids,
        genres=valid_genres_ids,
        cast_members=valid_cast_members_ids,
    )


class TestCreateVideoWithoutMedia:
    def test_execute_with_valid_data(
        self,
        use_case: CreateVideoWithoutMedia,
        valid_input: CreateVideoWithoutMedia.Input,
        video_repository: MagicMock,
        category_repository: MagicMock,
        genre_repository: MagicMock,
        cast_member_repository: MagicMock,
        valid_categories_ids: set[UUID],
        valid_genres_ids: set[UUID],
        valid_cast_members_ids: set[UUID],
    ) -> None:
        # Mock the repositories to return valid entities
        category_repository.list.return_value = [
            MagicMock(id=category_id) for category_id in valid_categories_ids
        ]
        genre_repository.list.return_value = [
            MagicMock(id=genre_id) for genre_id in valid_genres_ids
        ]
        cast_member_repository.list.return_value = [
            MagicMock(id=cast_member_id) for cast_member_id in valid_cast_members_ids
        ]

        # Call the use case
        output: CreateVideoWithoutMedia.Output = use_case.execute(valid_input)

        # Assert the result
        assert isinstance(output, CreateVideoWithoutMedia.Output)
        assert isinstance(output.id, UUID)
        video_repository.save.assert_called_once()

    def test_execute_with_invalid_categories(
        self,
        use_case: CreateVideoWithoutMedia,
        valid_input: CreateVideoWithoutMedia.Input,
        category_repository: MagicMock,
        genre_repository: MagicMock,
        cast_member_repository: MagicMock,
        valid_genres_ids: set[UUID],
        valid_cast_members_ids: set[UUID],
    ) -> None:
        # Mock repositories with missing categories
        category_repository.list.return_value = []
        genre_repository.list.return_value = [
            MagicMock(id=genre_id) for genre_id in valid_genres_ids
        ]
        cast_member_repository.list.return_value = [
            MagicMock(id=cast_member_id) for cast_member_id in valid_cast_members_ids
        ]

        # Assert that the use case raises the expected exception
        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(valid_input)

        assert "Categories with provided IDs not found" in str(exc_info.value)

    def test_execute_with_invalid_genres(
        self,
        use_case: CreateVideoWithoutMedia,
        valid_input: CreateVideoWithoutMedia.Input,
        category_repository: MagicMock,
        genre_repository: MagicMock,
        cast_member_repository: MagicMock,
        valid_categories_ids: set[UUID],
        valid_cast_members_ids: set[UUID],
    ) -> None:
        # Mock repositories with missing genres
        category_repository.list.return_value = [
            MagicMock(id=category_id) for category_id in valid_categories_ids
        ]
        genre_repository.list.return_value = []
        cast_member_repository.list.return_value = [
            MagicMock(id=cast_member_id) for cast_member_id in valid_cast_members_ids
        ]

        # Assert that the use case raises the expected exception
        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(valid_input)

        assert "Genres with provided IDs not found" in str(exc_info.value)

    def test_execute_with_invalid_cast_members(
        self,
        use_case: CreateVideoWithoutMedia,
        valid_input: CreateVideoWithoutMedia.Input,
        category_repository: MagicMock,
        genre_repository: MagicMock,
        cast_member_repository: MagicMock,
        valid_categories_ids: set[UUID],
        valid_genres_ids: set[UUID],
    ) -> None:
        # Mock repositories with missing cast members
        category_repository.list.return_value = [
            MagicMock(id=category_id) for category_id in valid_categories_ids
        ]
        genre_repository.list.return_value = [
            MagicMock(id=genre_id) for genre_id in valid_genres_ids
        ]
        cast_member_repository.list.return_value = []

        # Assert that the use case raises the expected exception
        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(valid_input)

        assert "Cast members with provided IDs not found" in str(exc_info.value)

    def test_execute_with_invalid_video_data(
        self,
        use_case: CreateVideoWithoutMedia,
        valid_input: CreateVideoWithoutMedia.Input,
        category_repository: MagicMock,
        genre_repository: MagicMock,
        cast_member_repository: MagicMock,
        valid_categories_ids: set[UUID],
        valid_genres_ids: set[UUID],
        valid_cast_members_ids: set[UUID],
    ) -> None:
        # Mock the repositories to return valid entities
        category_repository.list.return_value = [
            MagicMock(id=category_id) for category_id in valid_categories_ids
        ]
        genre_repository.list.return_value = [
            MagicMock(id=genre_id) for genre_id in valid_genres_ids
        ]
        cast_member_repository.list.return_value = [
            MagicMock(id=cast_member_id) for cast_member_id in valid_cast_members_ids
        ]

        # Create an invalid input (empty title)
        invalid_input = CreateVideoWithoutMedia.Input(
            title="",  # Empty title is invalid
            description=valid_input.description,
            launch_year=valid_input.launch_year,
            duration=valid_input.duration,
            rating=valid_input.rating,
            categories=valid_input.categories,
            genres=valid_input.genres,
            cast_members=valid_input.cast_members,
        )

        # Assert that the use case raises the expected exception
        with pytest.raises(InvalidVideo):
            use_case.execute(invalid_input)

    def test_execute_with_multiple_validation_failures(
        self,
        use_case: CreateVideoWithoutMedia,
        valid_input: CreateVideoWithoutMedia.Input,
        category_repository: MagicMock,
        genre_repository: MagicMock,
        cast_member_repository: MagicMock,
    ) -> None:
        # Mock all repositories to return empty lists
        category_repository.list.return_value = []
        genre_repository.list.return_value = []
        cast_member_repository.list.return_value = []

        # Assert that the use case raises the expected exception
        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(valid_input)

        # Check that all validation errors are present
        error_message = str(exc_info.value)
        assert "Categories with provided IDs not found" in error_message
        assert "Genres with provided IDs not found" in error_message
        assert "Cast members with provided IDs not found" in error_message