from typing import List
from uuid import UUID
from core.castmember.domain.castmember import CastMember
from core.castmember.domain.castmember_repository import CastMemberRepository
from django_project.castmember_app.models import CastMember as CastMemberORM

from django.db import transaction


class DjangoORMCastMemberRepository(CastMemberRepository):
    def __init__(self, castmember_orm: CastMemberORM | None = None):
        self.castmember_orm: CastMemberORM | None = castmember_orm or CastMemberORM

    def save(self, castmember: CastMember) -> None:
        with transaction.atomic():
            # CastMemberORM.objects.create(
            #     id=castmember.id, name=castmember.name, type=castmember.type
            # )
            castmember_model = CastMemberModelMapper.to_model(castmember)
            castmember_model.save()
        return None

    def get_by_id(self, id: UUID) -> CastMember:
        try:
            castmember_model = self.castmember_orm.objects.get(id=id)
        except self.castmember_orm.DoesNotExist:
            return None
        # return CastMember(
        #     id=castmember_model.id,
        #     name=castmember_model.name,
        #     type=castmember_model.type,
        # )
        return CastMemberModelMapper.to_entity(castmember_model)

    def delete(self, id: UUID) -> None:
        self.castmember_orm.objects.filter(id=id).delete()

        return None

    def list(self) -> List[CastMember]:
        return [
            # CastMember(
            #     id=castmember_model.id,
            #     name=castmember_model.name,
            #     type=castmember_model.type,
            # )
            # for castmember_model in CastMemberORM.objects.all()
            CastMemberModelMapper.to_entity(castmember_model)
            for castmember_model in self.castmember_orm.objects.all()
        ]

    def update(self, castmember: CastMember) -> CastMember:
        try:
            self.castmember_orm.objects.get(id=castmember.id)
        except self.castmember_orm.DoesNotExist:
            return None

        with transaction.atomic():
            self.castmember_orm.objects.filter(id=castmember.id).update(
                name=castmember.name, type=castmember.type
            )

        return None


class CastMemberModelMapper:
    @staticmethod
    def to_entity(castmember_model: CastMemberORM) -> CastMember:
        return CastMember(
            id=castmember_model.id,
            name=castmember_model.name,
            type=castmember_model.type,
        )

    @staticmethod
    def to_model(castmember: CastMember) -> CastMemberORM:
        return CastMemberORM(
            id=castmember.id, name=castmember.name, type=castmember.type
        )
