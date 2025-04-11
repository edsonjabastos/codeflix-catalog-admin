from decimal import Decimal
from core.video.domain.value_objects import Rating, MediaStatus

from rest_framework.serializers import (
    Serializer,
    UUIDField,
    CharField,
    IntegerField,
    DecimalField,
    BooleanField,
    ChoiceField,
    ListField,
)


class SetField(ListField):
    def to_internal_value(self, data):
        return set(super().to_internal_value(data))

    def to_representation(self, value):
        return list(super().to_representation(value))


class RatingField(ChoiceField):
    def __init__(self, **kwargs):
        choices = [(rating.name, rating.name) for rating in Rating]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return Rating[super().to_internal_value(data)]

    def to_representation(self, value):
        return value.name if value else None


class MediaStatusField(ChoiceField):
    def __init__(self, **kwargs):
        choices = [(status.name, status.name) for status in MediaStatus]
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        return MediaStatus[super().to_internal_value(data)]

    def to_representation(self, value):
        return value.name if value else None


class ImageMediaSerializer(Serializer):
    checksum = CharField(max_length=255)
    name = CharField(max_length=255)
    location = CharField(max_length=255)


class AudioVideoMediaSerializer(Serializer):
    checksum = CharField(max_length=255)
    name = CharField(max_length=255)
    raw_location = CharField(max_length=255)
    encoded_location = CharField(max_length=255)
    status = MediaStatusField()


class VideoOutputSerializer(Serializer):
    id = UUIDField()
    title = CharField(max_length=255)
    description = CharField()
    launch_year = IntegerField()
    duration = DecimalField(max_digits=10, decimal_places=2)
    published = BooleanField()
    rating = RatingField()

    categories = SetField(child=UUIDField())
    genres = SetField(child=UUIDField())
    cast_members = SetField(child=UUIDField())

    banner = ImageMediaSerializer(allow_null=True)
    thumbnail = ImageMediaSerializer(allow_null=True)
    thumbnail_half = ImageMediaSerializer(allow_null=True)
    trailer = AudioVideoMediaSerializer(allow_null=True)
    video = AudioVideoMediaSerializer(allow_null=True)


class ListVideoOutputMetaSerializer(Serializer):
    current_page = IntegerField()
    per_page = IntegerField()
    total = IntegerField()


class ListVideoOutputSerializer(Serializer):
    data = VideoOutputSerializer(many=True)
    meta = ListVideoOutputMetaSerializer()


class CreateVideoInputSerializer(Serializer):
    title = CharField(max_length=255, allow_blank=False)
    description = CharField(max_length=1024, allow_blank=False)
    launch_year = IntegerField()
    duration = DecimalField(max_digits=10, decimal_places=2)
    published = BooleanField(default=False)
    rating = RatingField()
    categories = SetField(child=UUIDField(), allow_empty=True)
    genres = SetField(child=UUIDField(), allow_empty=True)
    cast_members = SetField(child=UUIDField(), allow_empty=True)


class CreateVideoOutputSerializer(Serializer):
    id = UUIDField()


class UpdateVideoInputSerializer(Serializer):
    id = UUIDField()
    title = CharField(max_length=255, allow_blank=False)
    description = CharField(max_length=1024, allow_blank=False)
    launch_year = IntegerField()
    duration = DecimalField(max_digits=10, decimal_places=2)
    published = BooleanField()
    rating = RatingField()
    categories = SetField(child=UUIDField(), allow_empty=True)
    genres = SetField(child=UUIDField(), allow_empty=True)
    cast_members = SetField(child=UUIDField(), allow_empty=True)


class DeleteVideoInputSerializer(Serializer):
    id = UUIDField()


class UpdateMediaInputSerializer(Serializer):
    id = UUIDField()
    media_file = CharField()  # This would typically be a FileField in the actual view
