from rest_framework.serializers import (
    Serializer,
    UUIDField,
    CharField,
    BooleanField,
    ListField,
    IntegerField,
)


class GenreOutputSerializer(Serializer):
    id: UUIDField = UUIDField()
    name: CharField = CharField(max_length=255, allow_blank=False)
    is_active: BooleanField = BooleanField()
    categories: ListField = ListField(child=UUIDField())


class ListGenreOutputMetaSerializer(Serializer):
    current_page: IntegerField = IntegerField()
    per_page: IntegerField = IntegerField()
    total: IntegerField = IntegerField()


class ListGenreOutputSerializer(Serializer):
    data: GenreOutputSerializer = GenreOutputSerializer(many=True)
    meta: ListGenreOutputMetaSerializer = ListGenreOutputMetaSerializer()


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


class DeleteGenreInputSerializer(Serializer):
    id: UUIDField = UUIDField()


class UpdateGenreInputSerializer(Serializer):
    id: UUIDField = UUIDField()
    name: CharField = CharField(max_length=255, allow_blank=False)
    is_active: BooleanField = BooleanField()
    categories: SetField = SetField(child=UUIDField())
