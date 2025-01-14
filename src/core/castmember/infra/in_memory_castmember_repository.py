from typing import List
from uuid import UUID
from core.castmember.domain.castmember_repository import CastMemberRepository
from core.castmember.domain.castmember import CastMember


class InMemoryCastMemberRepository(CastMemberRepository):
    def __init__(self, castmembers: List[CastMember] = None) -> None:
        self.castmembers: List[CastMember] = castmembers or []

    def save(self, castmember: CastMember) -> None:
        self.castmembers.append(castmember)

        return None

    def get_by_id(self, id: UUID) -> CastMember | None:

        return next(
            (castmember for castmember in self.castmembers if castmember.id == id), None
        )

    def delete(self, id: UUID) -> None:
        castmember: CastMember = self.get_by_id(id=id)
        if castmember:
            self.castmembers.remove(castmember)

        return None

    def update(self, castmember: CastMember) -> None:
        castmember_to_be_updated: CastMember = self.get_by_id(id=castmember.id)
        if castmember_to_be_updated:
            # self.delete(id=castmember.id) # alternative way to update
            # self.save(castmember)
            castmember_to_be_updated_index: int = self.castmembers.index(
                castmember_to_be_updated
            )
            self.castmembers[castmember_to_be_updated_index] = castmember

        return None

    def list(self) -> List[CastMember]:

        return [castmember for castmember in self.castmembers]
