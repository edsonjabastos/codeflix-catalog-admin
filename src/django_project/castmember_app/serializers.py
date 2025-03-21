from rest_framework.serializers import (
    Serializer,
    UUIDField,
    CharField,
    ChoiceField,
    IntegerField,
)

# from django_project.castmember_app.models import CastMemberType
from core.castmember.domain.value_objects import CastMemberType


class CastMemberTypeField(ChoiceField):
    def __init__(self, **kwargs):
        # Utilizamos o "choices" do DRF, que permite um conjunto de opções limitado para um certo campo.
        choices = [(type.name, type.value) for type in CastMemberType]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        # Valor vindo da API como "str" é convertido para o StrEnum
        return CastMemberType(super().to_internal_value(data))

    def to_representation(self, value):
        # O valor vindo do nosso domínio é convertido para uma string na API
        return str(super().to_representation(value))


class CastMemberOutputSerializer(Serializer):
    id: UUIDField = UUIDField()
    name: CharField = CharField(max_length=255, allow_blank=False)
    type: CastMemberTypeField = CastMemberTypeField(required=True)


class ListCastMemberOutputMetaSerializer(Serializer):
    current_page: IntegerField = IntegerField()
    per_page: IntegerField = IntegerField()
    total: IntegerField = IntegerField()


class ListCastMemberOutputSerializer(Serializer):
    data: CastMemberOutputSerializer = CastMemberOutputSerializer(many=True)
    meta: ListCastMemberOutputMetaSerializer = ListCastMemberOutputMetaSerializer()

class CreateCastMemberInputSerializer(Serializer):
    name: CharField = CharField(max_length=255, allow_blank=False)
    type: CastMemberTypeField = CastMemberTypeField(required=True)


class CreateCastMemberOutputSerializer(Serializer):
    id: UUIDField = UUIDField()


class DeleteCastMemberInputSerializer(Serializer):
    id: UUIDField = UUIDField()


class UpdateCastMemberInputSerializer(Serializer):
    id: UUIDField = UUIDField(required=True)
    name: CharField = CharField(max_length=255, allow_blank=False, required=False)
    type: CastMemberTypeField = CastMemberTypeField(required=True)
