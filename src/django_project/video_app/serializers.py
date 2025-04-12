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
    ValidationError,
)

from django_project.castmember_app.models import CastMember
from django_project.category_app.models import Category
from django_project.genre_app.models import Genre
from django.core.exceptions import ObjectDoesNotExist


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
        return value if value else None


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

    def validate_categories(self, value):
        # Validate that all category UUIDs exist in the database
        invalid_categories = []
        for category_id in value:
            try:
                Category.objects.get(id=category_id)
            except ObjectDoesNotExist:
                invalid_categories.append(category_id)
        if invalid_categories:
            raise ValidationError(
                f"Invalid categorie(s) with provided ID(s) not found: {", ".join(f"'{str(invalid_category)}'" for invalid_category in invalid_categories)}"
            )
        return value

    def validate_genres(self, value):
        # Validate that all genre UUIDs exist in the database
        invalid_genres = []
        for genre_id in value:
            try:
                Genre.objects.get(id=genre_id)
            except ObjectDoesNotExist:
                invalid_genres.append(genre_id)
        if invalid_genres:
            raise ValidationError(
                f"Invalid genre(s) with provided ID(s) not found: {", ".join(f"'{str(invalid_genre)}'" for invalid_genre in invalid_genres)}"
            )
        return value

    def validate_cast_members(self, value):
        # Validate that all cast member UUIDs exist in the database
        invalid_cast_members = []
        for cast_member_id in value:
            try:
                CastMember.objects.get(id=cast_member_id)
            except ObjectDoesNotExist:
                invalid_cast_members.append(cast_member_id)
        if invalid_cast_members:
            raise ValidationError(
                f"Invalid cast member(s) with provided ID(s) not found: {", ".join(f"'{str(invalid_cast_member)}'" for invalid_cast_member in invalid_cast_members)}"
            )
        return value


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


class GetVideoInputSerializer(Serializer):
    id = UUIDField()

class GetVideoOutputSerializer(Serializer):
    data = VideoOutputSerializer(source="*")