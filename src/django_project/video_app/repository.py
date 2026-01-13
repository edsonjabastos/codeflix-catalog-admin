from typing import List
from uuid import UUID
from django.db import transaction
from core.video.domain.video import Video
from core.video.domain.video_repository import VideoRepository
from core.video.domain.value_objects import (
    ImageMedia,
    AudioVideoMedia,
    MediaStatus,
    MediaType,
    Rating,
)
from django_project.video_app.models import Video as VideoORM
from django_project.video_app.models import ImageMedia as ImageMediaORM
from django_project.video_app.models import AudioVideoMedia as AudioVideoMediaORM


class DjangoORMVideoRepository(VideoRepository):
    def __init__(self, video_orm: VideoORM | None = None):
        self.video_orm: VideoORM | None = video_orm or VideoORM

    def save(self, video: Video) -> None:
        with transaction.atomic():
            video_model = VideoModelMapper.to_model(video)
            video_model.save()
        return None

    def get_by_id(self, id: UUID) -> Video:
        try:
            video_model = self.video_orm.objects.get(id=id)
        except VideoORM.DoesNotExist:
            return None
        return VideoModelMapper.to_entity(video_model)

    def delete(self, id: UUID) -> None:
        self.video_orm.objects.filter(id=id).delete()
        return None

    def list(self) -> List[Video]:
        return [
            VideoModelMapper.to_entity(video_model)
            for video_model in self.video_orm.objects.all()
        ]

    def update(self, video: Video) -> Video:
        try:
            video_model = self.video_orm.objects.get(id=video.id)
        except self.video_orm.DoesNotExist:
            return None

        with transaction.atomic():
            # Update scalar fields
            video_model.title = video.title
            video_model.description = video.description
            video_model.launch_year = video.launch_year
            video_model.duration = video.duration
            video_model.published = video.published
            video_model.rating = video.rating

            # Save the updated instance (this will UPDATE, not INSERT)
            video_model.save()

            # Update M2M relationships (must be after save)
            video_model.categories.set(video.categories)
            video_model.genres.set(video.genres)
            video_model.cast_members.set(video.cast_members)

            # Handle banner media
            if video.banner:
                if video_model.banner:
                    video_model.banner.delete()
                banner_model = ImageMediaORM(
                    checksum=video.banner.checksum,
                    name=video.banner.name,
                    raw_location=video.banner.location,
                )
                banner_model.save()
                video_model.banner = banner_model
                video_model.save()

            # Handle thumbnail media
            if video.thumbnail:
                if video_model.thumbnail:
                    video_model.thumbnail.delete()
                thumbnail_model = ImageMediaORM(
                    checksum=video.thumbnail.checksum,
                    name=video.thumbnail.name,
                    raw_location=video.thumbnail.location,
                )
                thumbnail_model.save()
                video_model.thumbnail = thumbnail_model
                video_model.save()

            # Handle thumbnail_half media
            if video.thumbnail_half:
                if video_model.thumbnail_half:
                    video_model.thumbnail_half.delete()
                thumbnail_half_model = ImageMediaORM(
                    checksum=video.thumbnail_half.checksum,
                    name=video.thumbnail_half.name,
                    raw_location=video.thumbnail_half.location,
                )
                thumbnail_half_model.save()
                video_model.thumbnail_half = thumbnail_half_model
                video_model.save()

            # Handle trailer media
            if video.trailer:
                if video_model.trailer:
                    video_model.trailer.delete()
                trailer_model = AudioVideoMediaORM(
                    checksum=video.trailer.checksum,
                    name=video.trailer.name,
                    raw_location=video.trailer.raw_location,
                    encoded_location=video.trailer.encoded_location,
                    status=video.trailer.status.name,
                    media_type=video.trailer.media_type.name,
                )
                trailer_model.save()
                video_model.trailer = trailer_model
                video_model.save()

            # Handle video media
            if video.video:
                if video_model.video:
                    video_model.video.delete()
                video_media_model = AudioVideoMediaORM(
                    checksum=video.video.checksum,
                    name=video.video.name,
                    raw_location=video.video.raw_location,
                    encoded_location=video.video.encoded_location,
                    status=video.video.status.name,
                    media_type=video.video.media_type.name,
                )
                video_media_model.save()
                video_model.video = video_media_model
                video_model.save()

        return None


class VideoModelMapper:
    @staticmethod
    def to_entity(video: VideoORM) -> Video:
        banner = None
        if video.banner:
            banner = ImageMedia(
                checksum=video.banner.checksum,
                name=video.banner.name,
                location=video.banner.raw_location,
            )

        thumbnail = None
        if video.thumbnail:
            thumbnail = ImageMedia(
                checksum=video.thumbnail.checksum,
                name=video.thumbnail.name,
                location=video.thumbnail.raw_location,
            )

        thumbnail_half = None
        if video.thumbnail_half:
            thumbnail_half = ImageMedia(
                checksum=video.thumbnail_half.checksum,
                name=video.thumbnail_half.name,
                location=video.thumbnail_half.raw_location,
            )

        trailer = None
        if video.trailer:
            trailer = AudioVideoMedia(
                checksum=video.trailer.checksum,
                name=video.trailer.name,
                raw_location=video.trailer.raw_location,
                encoded_location=video.trailer.encoded_location,
                status=MediaStatus[video.trailer.status],
                media_type=MediaType.TRAILER,
            )

        video_media = None
        if video.video:
            video_media = AudioVideoMedia(
                checksum=video.video.checksum,
                name=video.video.name,
                raw_location=video.video.raw_location,
                encoded_location=video.video.encoded_location,
                status=MediaStatus[video.video.status],
                media_type=MediaType.VIDEO,
            )

        return Video(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            published=video.published,
            rating=Rating[video.rating],
            categories={category.id for category in video.categories.all()},
            genres={genre.id for genre in video.genres.all()},
            cast_members={cast_member.id for cast_member in video.cast_members.all()},
            banner=banner,
            thumbnail=thumbnail,
            thumbnail_half=thumbnail_half,
            trailer=trailer,
            video=video_media,
        )

    @staticmethod
    def to_model(video: Video) -> VideoORM:
        video_model = VideoORM(
            id=video.id,
            title=video.title,
            description=video.description,
            launch_year=video.launch_year,
            duration=video.duration,
            # opened=True,  # Default value or need to be added to the domain entity
            published=video.published,
            rating=video.rating,
        )

        # The M2M relationships need to be handled after the model is saved
        video_model.categories.set(video.categories)
        video_model.genres.set(video.genres)
        video_model.cast_members.set(video.cast_members)

        # Handle media relationships
        if video.banner:
            banner_model = ImageMediaORM(
                checksum=video.banner.checksum,
                name=video.banner.name,
                raw_location=video.banner.location,
            )
            banner_model.save()
            video_model.banner = banner_model

        if video.thumbnail:
            thumbnail_model = ImageMediaORM(
                checksum=video.thumbnail.checksum,
                name=video.thumbnail.name,
                raw_location=video.thumbnail.location,
            )
            thumbnail_model.save()
            video_model.thumbnail = thumbnail_model

        if video.thumbnail_half:
            thumbnail_half_model = ImageMediaORM(
                checksum=video.thumbnail_half.checksum,
                name=video.thumbnail_half.name,
                raw_location=video.thumbnail_half.location,
            )
            thumbnail_half_model.save()
            video_model.thumbnail_half = thumbnail_half_model

        if video.trailer:
            trailer_model = AudioVideoMediaORM(
                checksum=video.trailer.checksum,
                name=video.trailer.name,
                raw_location=video.trailer.raw_location,
                encoded_location=video.trailer.encoded_location,
                status=video.trailer.status.name,
                media_type=video.trailer.media_type.name,
            )
            trailer_model.save()
            video_model.trailer = trailer_model

        if video.video:
            video_media_model = AudioVideoMediaORM(
                checksum=video.video.checksum,
                name=video.video.name,
                raw_location=video.video.raw_location,
                encoded_location=video.video.encoded_location,
                status=video.video.status.name,
                media_type=video.video.media_type.name,
            )
            video_media_model.save()
            video_model.video = video_media_model

        return video_model

    @staticmethod
    def to_entity(model: VideoORM) -> Video:
        video = Video(
            id=model.id,
            title=model.title,
            description=model.description,
            launch_year=model.launch_year,
            # opened=model.opened,
            duration=model.duration,
            rating=model.rating,
            published=model.published,
            categories=set(model.categories.values_list("id", flat=True)),
            genres=set(model.genres.values_list("id", flat=True)),
            cast_members=set(model.cast_members.values_list("id", flat=True)),
        )

        if model.video:
            video.video = AudioVideoMedia(
                name=model.video.name,
                checksum=model.video.checksum,
                raw_location=model.video.raw_location,
                encoded_location=model.video.encoded_location,
                status=MediaStatus[model.video.status],
                media_type=MediaType[model.video.media_type],
            )

        if model.trailer:
            video.trailer = AudioVideoMedia(
                name=model.trailer.name,
                checksum=model.trailer.checksum,
                raw_location=model.trailer.raw_location,
                encoded_location=model.trailer.encoded_location,
                status=MediaStatus[model.trailer.status],
                media_type=MediaType[model.trailer.media_type],
            )

        return video
