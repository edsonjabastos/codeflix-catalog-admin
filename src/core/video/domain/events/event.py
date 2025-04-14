from dataclasses import dataclass
from uuid import UUID

from core.video.domain.value_objects import MediaType


@dataclass(frozen=True)
class AudioVideoMediaUpdated:
    aggregate_id: UUID
    file_path: str
    media_type: MediaType
