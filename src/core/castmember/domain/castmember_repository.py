from abc import ABC, abstractmethod
from typing import List
from uuid import UUID

from core.castmember.domain.castmember import CastMember


class CastMemberRepository(ABC):
    @abstractmethod
    def save(self, castmember: CastMember) -> CastMember:
        raise NotImplementedError

    @abstractmethod
    def update(self, castmember: CastMember) -> CastMember:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[CastMember]:
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, id: UUID) -> CastMember:
        raise NotImplementedError

    @abstractmethod
    def delete(self, id: UUID) -> None:
        raise NotImplementedError

    @abstractmethod
    def exists_by_ids(self, ids: set[UUID]) -> bool:
        raise NotImplementedError

    @abstractmethod
    def find_missing_ids(self, ids: set[UUID]) -> set[UUID]:
        raise NotImplementedError
