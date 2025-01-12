from rest_framework.serializers import (
    Serializer,
    UUIDField,
    CharField,
    BooleanField,
    ListField,
)


class GenreGenreOutputSerializer(Serializer):
    id: UUIDField = UUIDField()
    name: CharField = CharField(max_length=255, allow_blank=False)
    is_active: BooleanField = BooleanField()
    categories: ListField = ListField(child=UUIDField())


class ListGenreOutputSerializer(Serializer):
    data: GenreGenreOutputSerializer = GenreGenreOutputSerializer(many=True)


# can be done with serializer method field too
class SetField(ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_representation(value))


class CreateGenreInputSerializer(Serializer):
    name: CharField = CharField(max_length=255, allow_blank=False)
    is_active: BooleanField = BooleanField(default=True)
    categories: SetField = SetField(child=UUIDField())


class CreateGenreResponseSerializer(Serializer):
    id: UUIDField = UUIDField()
