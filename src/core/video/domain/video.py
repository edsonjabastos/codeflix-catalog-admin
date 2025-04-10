from dataclasses import dataclass
from core._shared.entity import Entity
from core.video.domain.value_objects import AudioVideoMedia, ImageMedia, Rating
from decimal import Decimal
from uuid import UUID


@dataclass
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
