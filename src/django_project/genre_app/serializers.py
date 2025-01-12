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
