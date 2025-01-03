from rest_framework.serializers import (
    Serializer,
    UUIDField,
    CharField,
    BooleanField,
)


class CategoryResponseSerializer(Serializer):
    id: UUIDField = UUIDField()
    name: CharField = CharField(max_length=255)
    description: CharField = CharField()
    is_active: BooleanField = BooleanField()


class ListCategoryResponseSerializer(Serializer):
    data: CategoryResponseSerializer = CategoryResponseSerializer(many=True)


class RetrieveCategoryRequestSerializer(Serializer):
    id: UUIDField = UUIDField()


class RetrieveCategoryResponseSerializer(Serializer):
    data: CategoryResponseSerializer = CategoryResponseSerializer(source="*")


class CreateCategoryRequestSerializer(Serializer):
    name: CharField = CharField(max_length=255, allow_blank=False)
    description: CharField = CharField()
    is_active: BooleanField = BooleanField(default=True)


class CreateCategoryResponseSerializer(Serializer):
    id: UUIDField = UUIDField()


class UpdateCategoryRequestSerializer(Serializer):
    id: UUIDField = UUIDField()
    name: CharField = CharField(max_length=255, allow_blank=False)
    description: CharField = CharField()
    is_active: BooleanField = BooleanField()
