from dataclasses import dataclass
from core._shared.entity import Entity
from core.video.domain.value_objects import AudioVideoMedia, ImageMedia, Rating
from decimal import Decimal
from uuid import UUID


@dataclass(slots=True, kw_only=True)
class Video(Entity):
    title: str
    description: str
    launch_year: int
    duration: Decimal
    published: bool
    rating: Rating

    categories: set[UUID]
    genres: set[UUID]
    cast_members: set[UUID]

    banner: ImageMedia | None = None
    thumbnail: ImageMedia | None = None
    thumbnail_half: ImageMedia | None = None
    trailer: AudioVideoMedia | None = None
    video: AudioVideoMedia | None = None

    def __post_init__(self) -> None:
        self.validate()

    def __str__(self) -> str:
        return f"{self.title} - {self.description} ({self.launch_year})"

    def __repr__(self) -> str:
        return f"<Video {self.title} ({self.id})>"

    def validate(self) -> None:

        if not self.title:
            self.notification.add_error("title cannot be empty")
        if len(self.title) > 255:
            self.notification.add_error("title cannot be longer than 255 characters")
        if not self.description:
            self.notification.add_error("description cannot be empty")
        if len(self.description) > 1024:
            self.notification.add_error(
                "description cannot be longer than 1024 characters"
            )
        if not isinstance(self.launch_year, int):
            self.notification.add_error("launch_year must be an integer")
        if not isinstance(self.duration, Decimal):
            self.notification.add_error("duration must be a decimal")
        if not isinstance(self.published, bool):
            self.notification.add_error("published must be a boolean")
        if not isinstance(self.rating, Rating):
            self.notification.add_error("rating must be a Rating")

        if self.notification.has_errors:
            raise ValueError(self.notification.messages)

    def update(
        self,
        title: str,
        description: str,
        launch_year: int,
        duration: Decimal,
        published: bool,
        rating: Rating,
    ) -> None:
        self.title = title
        self.description = description
        self.launch_year = launch_year
        self.duration = duration
        self.published = published
        self.rating = rating

        self.validate()

    def add_category(self, category_id: UUID) -> None:
        self.categories.add(category_id)
        self.validate()

    def remove_category(self, category_id: UUID) -> None:
        self.categories.remove(category_id)
        self.validate()

    def add_genre(self, genre_id: UUID) -> None:
        self.genres.add(genre_id)
        self.validate()

    def remove_genre(self, genre_id: UUID) -> None:
        self.genres.remove(genre_id)
        self.validate()

    def add_cast_member(self, cast_member_id: UUID) -> None:
        self.cast_members.add(cast_member_id)
        self.validate()

    def remove_cast_member(self, cast_member_id: UUID) -> None:
        self.cast_members.remove(cast_member_id)
        self.validate()

    def update_banner(self, banner: ImageMedia) -> None:
        self.banner = banner
        self.validate()

    def update_thumbnail(self, thumbnail: ImageMedia) -> None:
        self.thumbnail = thumbnail
        self.validate()

    def update_thumbnail_half(self, thumbnail_half: ImageMedia) -> None:
        self.thumbnail_half = thumbnail_half
        self.validate()

    def update_trailer(self, trailer: AudioVideoMedia) -> None:
        self.trailer = trailer
        self.validate()

    def update_video(self, video: AudioVideoMedia) -> None:
        self.video = video
        self.validate()
