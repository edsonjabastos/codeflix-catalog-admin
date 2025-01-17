from rest_framework.serializers import (
    Serializer,
    UUIDField,
    CharField,
    BooleanField,
    IntegerField,
)


class CategoryResponseSerializer(Serializer):
    id: UUIDField = UUIDField()
    name: CharField = CharField(max_length=255)
    description: CharField = CharField()
    is_active: BooleanField = BooleanField()


class ListCategoryOutputMetaSerializer(Serializer):
    current_page: IntegerField = IntegerField()
    per_page: IntegerField = IntegerField()
    total: IntegerField = IntegerField()


class ListCategoryResponseSerializer(Serializer):
    data: CategoryResponseSerializer = CategoryResponseSerializer(many=True)
    meta: ListCategoryOutputMetaSerializer = ListCategoryOutputMetaSerializer()


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


class DeleteCategoryRequestSerializer(Serializer):
    id: UUIDField = UUIDField()


class PatchCategoryRequestSerializer(Serializer):
    id: UUIDField = UUIDField()
    name: CharField = CharField(max_length=255, allow_blank=False, required=False)
    description: CharField = CharField(required=False)
    is_active: BooleanField = BooleanField(required=False)
