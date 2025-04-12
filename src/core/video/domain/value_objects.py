from dataclasses import dataclass
from enum import Enum, StrEnum, auto, unique


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


@dataclass(frozen=True)
class ImageMedia:
    name: str
    checksum: str
    location: str


@dataclass(frozen=True)
class AudioVideoMedia:
    checksum: str
    name: str
    raw_location: str
    encoded_location: str
    status: MediaStatus
