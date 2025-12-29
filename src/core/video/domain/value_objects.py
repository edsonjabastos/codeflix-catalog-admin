from dataclasses import dataclass
from enum import StrEnum, unique


@unique
class Rating(StrEnum):
    ER = "ER"
    L = "L"
    AGE_10 = "AGE_10"
    AGE_12 = "AGE_12"
    AGE_14 = "AGE_14"
    AGE_16 = "AGE_16"
    AGE_18 = "AGE_18"


@unique
class MediaStatus(StrEnum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    ERROR = "ERROR"


@unique
class MediaType(StrEnum):
    VIDEO = "VIDEO"
    TRAILER = "TRAILER"


@dataclass(frozen=True)
class ImageMedia:
    name: str
    checksum: str
    location: str


@dataclass(frozen=True)
class AudioVideoMedia:
    name: str
    checksum: str
    raw_location: str
    encoded_location: str
    status: MediaStatus
    media_type: MediaType
