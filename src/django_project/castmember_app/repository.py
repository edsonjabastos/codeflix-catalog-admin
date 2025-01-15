from typing import List
from uuid import UUID
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository
from django_project.castmember_app.models import CastMember as CastMemberModel
from django_project.castmember_app.models import CastMemberType

from django.db import transaction


class DjangoORMCastMemberRepository(CastMemberRepository):

    def save(self, castmember: CastMember) -> None:
        with transaction.atomic():
            CastMemberModel.objects.create(
                id=castmember.id, name=castmember.name, type=castmember.type
            )

        return None

    def get_by_id(self, id: UUID) -> CastMember:
        try:
            castmember_model = CastMemberModel.objects.get(id=id)
        except CastMemberModel.DoesNotExist:
            return None
        return CastMember(
            id=castmember_model.id,
            name=castmember_model.name,
            type=castmember_model.type,
        )

    def delete(self, id: UUID) -> None:
        CastMemberModel.objects.filter(id=id).delete()

        return None

    def list(self) -> List[CastMember]:
        return [
            CastMember(
                id=castmember_model.id,
                name=castmember_model.name,
                type=castmember_model.type,
            )
            for castmember_model in CastMemberModel.objects.all()
        ]

    def update(self, castmember: CastMember) -> CastMember:
        try:
            CastMemberModel.objects.get(id=castmember.id)
        except CastMemberModel.DoesNotExist:
            return None

        with transaction.atomic():
            CastMemberModel.objects.filter(id=castmember.id).update(
                name=castmember.name, type=castmember.type
            )

        return castmember
