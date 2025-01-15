from django.db.models import TextChoices, UUIDField, CharField, Model
from uuid import uuid4

from core.castmember.domain.value_objects import CastMemberType


# class CastMemberType(TextChoices):
#     ACTOR: str = "ACTOR", "Actor"
#     DIRECTOR: str = "DIRECTOR", "Director"


class CastMember(Model):
    app_label: str = "castmember_app"

    id: UUIDField = UUIDField(primary_key=True, default=uuid4)
    name: CharField = CharField(max_length=255)
    type: CharField = CharField(
        max_length=8, choices=[(type.name, type.value) for type in CastMemberType]
    )

    class Meta:
        db_table: str = "cast_members"

    def __str__(self):
        return self.name
