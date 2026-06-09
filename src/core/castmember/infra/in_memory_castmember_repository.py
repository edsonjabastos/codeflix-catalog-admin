from typing import List
from uuid import UUID

from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository


class InMemoryCastMemberRepository(CastMemberRepository):
    def __init__(self, castmembers: List[CastMember] = None) -> None:
        self.castmembers: List[CastMember] = castmembers or []

    def save(self, castmember: CastMember) -> None:
        self.castmembers.append(castmember)

    def get_by_id(self, id: UUID) -> CastMember | None:
        return next(
            (castmember for castmember in self.castmembers if castmember.id == id),
            None,
        )

    def delete(self, id: UUID) -> None:
        castmember: CastMember = self.get_by_id(id=id)
        if castmember:
            self.castmembers.remove(castmember)

    def update(self, castmember: CastMember) -> None:
        castmember_to_be_updated: CastMember = self.get_by_id(id=castmember.id)
        if castmember_to_be_updated:
            castmember_to_be_updated_index: int = self.castmembers.index(
                castmember_to_be_updated
            )
            self.castmembers[castmember_to_be_updated_index] = castmember

    def list(self) -> List[CastMember]:
        return [castmember for castmember in self.castmembers]

    def exists_by_ids(self, ids: set[UUID]) -> bool:
        if not ids:
            return True
        existing = {castmember.id for castmember in self.castmembers}
        return ids.issubset(existing)

    def find_missing_ids(self, ids: set[UUID]) -> set[UUID]:
        if not ids:
            return set()
        existing = {castmember.id for castmember in self.castmembers}
        return ids - existing
