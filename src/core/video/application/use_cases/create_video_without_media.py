from dataclasses import dataclass
from decimal import Decimal
from typing import Set
from uuid import UUID

from core._shared.domain.notification import Notification
from core.castmember.domain.castmember_repository import CastMemberRepository
from core.category.domain.category_repository import CategoryRepository
from core.genre.domain.genre_repository import GenreRepository
from core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound
from core.video.domain.value_objects import Rating
from core.video.domain.video import Video
from core.video.domain.video_repository import VideoRepository


class CreateVideoWithoutMedia:
    def __init__(
        self,
        video_repository: VideoRepository,
        category_repository: CategoryRepository,
        genre_repository: GenreRepository,
        cast_member_repository: CastMemberRepository,
    ):
        self.video_repository = video_repository
        self.category_repository = category_repository
        self.genre_repository = genre_repository
        self.cast_member_repository = cast_member_repository

    @dataclass
    class Input:
        title: str
        description: str
        launch_year: int
        duration: Decimal
        rating: Rating

        categories: set[UUID]
        genres: set[UUID]
        cast_members: set[UUID]

    @dataclass
    class Output:
        id: UUID

    def execute(self, input: Input) -> Output:
        notification: Notification = Notification()

        self.validate_categories(input, notification)
        self.validate_genres(input, notification)
        self.validate_cast_members(input, notification)

        if notification.has_errors:
            raise RelatedEntitiesNotFound(notification.messages)

        try:
            video = Video(
                title=input.title,
                description=input.description,
                launch_year=input.launch_year,
                duration=Decimal(input.duration),
                published=False,
                rating=input.rating,
                categories=input.categories,
                genres=input.genres,
                cast_members=input.cast_members,
            )
        except ValueError as e:
            raise InvalidVideo(e)
        self.video_repository.save(video)

        return self.Output(id=video.id)

    def validate_categories(self, input: Input, notification: Notification) -> None:
        if not input.categories:
            return
        if not self.category_repository.exists_by_ids(input.categories):
            missing_categories = self.category_repository.find_missing_ids(
                input.categories
            )
            notification.add_error(
                f"Categories with provided IDs not found: {', '.join(str(missing_category_id) for missing_category_id in missing_categories)}"
            )

    def validate_genres(self, input: Input, notification: Notification) -> None:
        if not input.genres:
            return
        if not self.genre_repository.exists_by_ids(input.genres):
            missing_genres = self.genre_repository.find_missing_ids(input.genres)
            notification.add_error(
                f"Genres with provided IDs not found: {', '.join(str(missing_genre_id) for missing_genre_id in missing_genres)}"
            )

    def validate_cast_members(self, input: Input, notification: Notification) -> None:
        if not input.cast_members:
            return
        if not self.cast_member_repository.exists_by_ids(input.cast_members):
            missing_cast_members = self.cast_member_repository.find_missing_ids(
                input.cast_members
            )
            notification.add_error(
                f"Cast members with provided IDs not found: {', '.join(str(missing_cast_member_id) for missing_cast_member_id in missing_cast_members)}"
            )
