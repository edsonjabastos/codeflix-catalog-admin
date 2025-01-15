from dataclasses import dataclass


@dataclass
class Notification:
    def __init__(self):
        self._errors: list[str] = []

    def add_error(self, message: str) -> None:
        self._errors.append(message)

    @property
    def has_errors(self) -> bool:
        return bool(self._errors)

    @property
    def messages(self) -> str:
        return ", ".join(self._errors)
