from dataclasses import dataclass
from decimal import Decimal
from typing import Set
from uuid import UUID

from core._shared.notification import Notification
from core.video.domain.video_repository import VideoRepository
from core.category.domain.category_repository import CategoryRepository
from core.genre.domain.genre_repository import GenreRepository
from core.castmember.domain.castmember_repository import CastMemberRepository
from core.video.application.exceptions import (
    InvalidVideo,
    RelatedEntitiesNotFound,
)
from core.video.domain.video import Video
from core.video.domain.value_objects import Rating


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
        category_ids: Set = {
            category.id for category in self.category_repository.list()
        }
        categories_input_set = set(input.categories)
        if not categories_input_set.issubset(category_ids):
            missing_categories = categories_input_set - category_ids
            notification.add_error(
                f"Categories with provided IDs not found: {', '.join(str(missing_category_id) for missing_category_id in missing_categories)}"
            )

    def validate_genres(self, input: Input, notification: Notification) -> None:
        if not input.genres:
            return
        genre_ids: Set = {genre.id for genre in self.genre_repository.list()}
        genres_input_set = set(input.genres)
        if not genres_input_set.issubset(genre_ids):
            missing_genres = genres_input_set - genre_ids
            notification.add_error(
                f"Genres with provided IDs not found: {', '.join(str(missing_genre_id) for missing_genre_id in missing_genres)}"
            )

    def validate_cast_members(self, input: Input, notification: Notification) -> None:
        if not input.cast_members:
            return
        cast_member_ids: Set = {
            cast_member.id for cast_member in self.cast_member_repository.list()
        }
        cast_members_input_set = set(input.cast_members)
        if not cast_members_input_set.issubset(cast_member_ids):
            missing_cast_members = cast_members_input_set - cast_member_ids
            notification.add_error(
                f"Cast members with provided IDs not found: {', '.join(str(missing_cast_member_id) for missing_cast_member_id in missing_cast_members)}"
            )
