from dataclasses import dataclass

from core._shared.events.event import Event


@dataclass(frozen=True)
class AudioVideoMediaUpdatedIntegrationEvent(Event):
    resource_id: str
    file_path: str

    def __str__(self) -> str:
        return (
            f"AudioVideoMediaUpdatedIntegrationEvent("
            f"resource_id={self.resource_id}, file_path={self.file_path})"
        )
