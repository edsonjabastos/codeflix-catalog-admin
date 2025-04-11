import pytest
from decimal import Decimal
from uuid import UUID, uuid4
from core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound
from core.video.application.use_cases.create_video_without_media import (
    CreateVideoWithoutMedia,
)
from core.video.domain.value_objects import Rating
from core.video.infra.in_memory_video_repository import InMemoryVideoRepository
from core.category.infra.in_memory_category_repository import InMemoryCategoryRepository
from core.genre.infra.in_memory_genre_repository import InMemoryGenreRepository
from core.castmember.infra.in_memory_castmember_repository import (
    InMemoryCastMemberRepository,
)
from core.category.domain.category import Category
from core.genre.domain.genre import Genre
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.value_objects import CastMemberType


@pytest.fixture
def video_repository() -> InMemoryVideoRepository:
    return InMemoryVideoRepository()


@pytest.fixture
def categories() -> list[Category]:
    return [
        Category(name="Category 1", description="Description 1"),
        Category(name="Category 2", description="Description 2"),
        Category(name="Category 3", description="Description 3"),
    ]


@pytest.fixture
def category_repository(categories: list[Category]) -> InMemoryCategoryRepository:
    repo = InMemoryCategoryRepository()
    for category in categories:
        repo.save(category)
    return repo


@pytest.fixture
def genres() -> list[Genre]:
    return [
        Genre(name="Genre 1"),
        Genre(name="Genre 2"),
        Genre(name="Genre 3"),
    ]


@pytest.fixture
def genre_repository(genres: list[Genre]) -> InMemoryGenreRepository:
    repo = InMemoryGenreRepository()
    for genre in genres:
        repo.save(genre)
    return repo


@pytest.fixture
def cast_members() -> list[CastMember]:
    return [
        CastMember(name="Cast Member 1", type=CastMemberType.ACTOR),
        CastMember(name="Cast Member 2", type=CastMemberType.DIRECTOR),
        CastMember(name="Cast Member 3", type=CastMemberType.ACTOR),
    ]


@pytest.fixture
def cast_member_repository(
    cast_members: list[CastMember],
) -> InMemoryCastMemberRepository:
    repo = InMemoryCastMemberRepository()
    for cast_member in cast_members:
        repo.save(cast_member)
    return repo


@pytest.fixture
def use_case(
    video_repository: InMemoryVideoRepository,
    category_repository: InMemoryCategoryRepository,
    genre_repository: InMemoryGenreRepository,
    cast_member_repository: InMemoryCastMemberRepository,
) -> CreateVideoWithoutMedia:
    return CreateVideoWithoutMedia(
        video_repository=video_repository,
        category_repository=category_repository,
        genre_repository=genre_repository,
        cast_member_repository=cast_member_repository,
    )


@pytest.fixture
def valid_categories_ids(categories: list[Category]) -> set[UUID]:
    return {category.id for category in categories}


@pytest.fixture
def valid_genres_ids(genres: list[Genre]) -> set[UUID]:
    return {genre.id for genre in genres}


@pytest.fixture
def valid_cast_members_ids(cast_members: list[CastMember]) -> set[UUID]:
    return {cast_member.id for cast_member in cast_members}


@pytest.fixture
def valid_input(
    valid_categories_ids: set[UUID],
    valid_genres_ids: set[UUID],
    valid_cast_members_ids: set[UUID],
) -> CreateVideoWithoutMedia.Input:
    return CreateVideoWithoutMedia.Input(
        title="Test Video",
        description="Test Description",
        launch_year=2021,
        duration=Decimal("120.5"),
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
        video_repository: InMemoryVideoRepository,
    ) -> None:
        # Act
        output = use_case.execute(valid_input)

        # Assert
        assert output is not None
        assert isinstance(output.id, UUID)

        video = video_repository.get_by_id(output.id)
        assert video is not None
        assert video.title == valid_input.title
        assert video.description == valid_input.description
        assert video.launch_year == valid_input.launch_year
        assert video.duration == valid_input.duration
        assert video.categories == valid_input.categories
        assert video.genres == valid_input.genres
        assert video.cast_members == valid_input.cast_members
        assert video.published is False

    def test_execute_with_invalid_categories(
        self,
        use_case: CreateVideoWithoutMedia,
        valid_input: CreateVideoWithoutMedia.Input,
    ) -> None:
        # Arrange
        invalid_category_id = uuid4()
        input_with_invalid_category = CreateVideoWithoutMedia.Input(
            title=valid_input.title,
            description=valid_input.description,
            launch_year=valid_input.launch_year,
            duration=valid_input.duration,
            rating=valid_input.rating,
            categories={invalid_category_id},
            genres=valid_input.genres,
            cast_members=valid_input.cast_members,
        )

        # Act & Assert
        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(input_with_invalid_category)

        assert "Categories with provided IDs not found" in str(exc_info.value)
        assert str(invalid_category_id) in str(exc_info.value)

    def test_execute_with_invalid_genres(
        self,
        use_case: CreateVideoWithoutMedia,
        valid_input: CreateVideoWithoutMedia.Input,
    ) -> None:
        # Arrange
        invalid_genre_id = uuid4()
        input_with_invalid_genre = CreateVideoWithoutMedia.Input(
            title=valid_input.title,
            description=valid_input.description,
            launch_year=valid_input.launch_year,
            duration=valid_input.duration,
            rating=valid_input.rating,
            categories=valid_input.categories,
            genres={invalid_genre_id},
            cast_members=valid_input.cast_members,
        )

        # Act & Assert
        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(input_with_invalid_genre)

        assert "Genres with provided IDs not found" in str(exc_info.value)
        assert str(invalid_genre_id) in str(exc_info.value)

    def test_execute_with_invalid_cast_members(
        self,
        use_case: CreateVideoWithoutMedia,
        valid_input: CreateVideoWithoutMedia.Input,
    ) -> None:
        # Arrange
        invalid_cast_member_id = uuid4()
        input_with_invalid_cast_member = CreateVideoWithoutMedia.Input(
            title=valid_input.title,
            description=valid_input.description,
            launch_year=valid_input.launch_year,
            duration=valid_input.duration,
            rating=valid_input.rating,
            categories=valid_input.categories,
            genres=valid_input.genres,
            cast_members={invalid_cast_member_id},
        )

        # Act & Assert
        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(input_with_invalid_cast_member)

        assert "Cast members with provided IDs not found" in str(exc_info.value)
        assert str(invalid_cast_member_id) in str(exc_info.value)

    def test_execute_with_multiple_invalid_entities(
        self,
        use_case: CreateVideoWithoutMedia,
        valid_input: CreateVideoWithoutMedia.Input,
    ) -> None:
        # Arrange
        invalid_category_id = uuid4()
        invalid_genre_id = uuid4()
        invalid_cast_member_id = uuid4()

        input_with_multiple_invalid_entities = CreateVideoWithoutMedia.Input(
            title=valid_input.title,
            description=valid_input.description,
            launch_year=valid_input.launch_year,
            duration=valid_input.duration,
            rating=valid_input.rating,
            categories={invalid_category_id},
            genres={invalid_genre_id},
            cast_members={invalid_cast_member_id},
        )

        # Act & Assert
        with pytest.raises(RelatedEntitiesNotFound) as exc_info:
            use_case.execute(input_with_multiple_invalid_entities)

        error_message = str(exc_info.value)
        assert "Categories with provided IDs not found" in error_message
        assert "Genres with provided IDs not found" in error_message
        assert "Cast members with provided IDs not found" in error_message
        assert str(invalid_category_id) in error_message
        assert str(invalid_genre_id) in error_message
        assert str(invalid_cast_member_id) in error_message

    def test_execute_with_invalid_video_data(
        self,
        use_case: CreateVideoWithoutMedia,
        valid_categories_ids: set[UUID],
        valid_genres_ids: set[UUID],
        valid_cast_members_ids: set[UUID],
    ) -> None:
        # Empty title should cause validation error
        invalid_input = CreateVideoWithoutMedia.Input(
            title="",
            description="Test Description",
            launch_year=2021,
            duration=Decimal("120.5"),
            rating="L",
            categories=valid_categories_ids,
            genres=valid_genres_ids,
            cast_members=valid_cast_members_ids,
        )

        # Act & Assert
        with pytest.raises(InvalidVideo):
            use_case.execute(invalid_input)
