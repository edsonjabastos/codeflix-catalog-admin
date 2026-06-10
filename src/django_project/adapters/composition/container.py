import os

from config import TMP_BUCKET

from core._shared.application.ports.auth_service import AuthService
from core._shared.application.ports.checksum_service import ChecksumService
from core._shared.application.ports.event_publisher import EventPublisher
from core._shared.application.ports.storage_service import StorageService
from core.castmember.domain.castmember_repository import CastMemberRepository
from core.category.application.use_cases.create_category import CreateCategory
from core.category.application.use_cases.delete_category import DeleteCategory
from core.category.application.use_cases.get_category import GetCategory
from core.category.application.use_cases.list_category import ListCategory
from core.category.application.use_cases.update_category import UpdateCategory
from core.category.domain.category_repository import CategoryRepository
from core.castmember.application.use_cases.create_castmember import CreateCastMember
from core.castmember.application.use_cases.delete_castmember import DeleteCastMember
from core.castmember.application.use_cases.get_castmember import GetCastMember
from core.castmember.application.use_cases.list_castmember import ListCastMember
from core.castmember.application.use_cases.update_castmember import UpdateCastMember
from core.genre.application.use_cases.create_genre import CreateGenre
from core.genre.application.use_cases.delete_genre import DeleteGenre
from core.genre.application.use_cases.get_genre import GetGenre
from core.genre.application.use_cases.list_genre import ListGenre
from core.genre.application.use_cases.update_genre import UpdateGenre
from core.genre.domain.genre_repository import GenreRepository
from core.video.application.use_cases.create_video_without_media import (
    CreateVideoWithoutMedia,
)
from core.video.application.use_cases.get_video import GetVideo
from core.video.application.use_cases.process_audio_video_media import (
    ProcessAudioVideoMedia,
)
from core.video.application.use_cases.upload_video import UploadVideo
from core.video.domain.video_repository import VideoRepository
from django_project.adapters.auth.jwt_auth_service import JwtAuthService
from django_project.adapters.messaging.message_bus import MessageBus
from django_project.adapters.messaging.video_converted_consumer import (
    VideoConvertedRabbitMQConsumer,
)
from django_project.adapters.persistence.django.castmember_repository import (
    DjangoORMCastMemberRepository,
)
from django_project.adapters.persistence.django.category_repository import (
    DjangoORMCategoryRepository,
)
from django_project.adapters.persistence.django.genre_repository import (
    DjangoORMGenreRepository,
)
from django_project.adapters.persistence.django.video_repository import (
    DjangoORMVideoRepository,
)
from django_project.adapters.storage.file_checksum_service import FileChecksumService
from django_project.adapters.storage.local_storage import LocalStorage


class Container:
    def category_repository(self) -> CategoryRepository:
        return DjangoORMCategoryRepository()

    def genre_repository(self) -> GenreRepository:
        return DjangoORMGenreRepository()

    def castmember_repository(self) -> CastMemberRepository:
        return DjangoORMCastMemberRepository()

    def video_repository(self) -> VideoRepository:
        return DjangoORMVideoRepository()

    def storage_service(self) -> StorageService:
        return LocalStorage(bucket=TMP_BUCKET)

    def checksum_service(self) -> ChecksumService:
        return FileChecksumService()

    def event_publisher(self) -> EventPublisher:
        return MessageBus()

    def auth_service(self, token: str = "") -> AuthService:
        return JwtAuthService(token=token)

    def list_category(self) -> ListCategory:
        return ListCategory(repository=self.category_repository())

    def create_category(self) -> CreateCategory:
        return CreateCategory(repository=self.category_repository())

    def get_category(self) -> GetCategory:
        return GetCategory(repository=self.category_repository())

    def update_category(self) -> UpdateCategory:
        return UpdateCategory(repository=self.category_repository())

    def delete_category(self) -> DeleteCategory:
        return DeleteCategory(repository=self.category_repository())

    def list_genre(self) -> ListGenre:
        return ListGenre(repository=self.genre_repository())

    def create_genre(self) -> CreateGenre:
        return CreateGenre(
            genre_repository=self.genre_repository(),
            category_repository=self.category_repository(),
        )

    def get_genre(self) -> GetGenre:
        return GetGenre(repository=self.genre_repository())

    def update_genre(self) -> UpdateGenre:
        return UpdateGenre(
            genre_repository=self.genre_repository(),
            category_repository=self.category_repository(),
        )

    def delete_genre(self) -> DeleteGenre:
        return DeleteGenre(repository=self.genre_repository())

    def list_castmember(self) -> ListCastMember:
        return ListCastMember(repository=self.castmember_repository())

    def create_castmember(self) -> CreateCastMember:
        return CreateCastMember(castmember_repository=self.castmember_repository())

    def get_castmember(self) -> GetCastMember:
        return GetCastMember(castmember_repository=self.castmember_repository())

    def update_castmember(self) -> UpdateCastMember:
        return UpdateCastMember(castmember_repository=self.castmember_repository())

    def delete_castmember(self) -> DeleteCastMember:
        return DeleteCastMember(castmember_repository=self.castmember_repository())

    def create_video_without_media(self) -> CreateVideoWithoutMedia:
        return CreateVideoWithoutMedia(
            video_repository=self.video_repository(),
            category_repository=self.category_repository(),
            genre_repository=self.genre_repository(),
            cast_member_repository=self.castmember_repository(),
        )

    def get_video(self) -> GetVideo:
        return GetVideo(video_repository=self.video_repository())

    def upload_video(self) -> UploadVideo:
        return UploadVideo(
            video_repository=self.video_repository(),
            storage_service=self.storage_service(),
            event_publisher=self.event_publisher(),
            checksum_service=self.checksum_service(),
            storage_base_path=TMP_BUCKET,
        )

    def process_audio_video_media(self) -> ProcessAudioVideoMedia:
        return ProcessAudioVideoMedia(
            video_repository=self.video_repository(),
            event_publisher=self.event_publisher(),
        )

    def video_converted_consumer(self) -> VideoConvertedRabbitMQConsumer:
        return VideoConvertedRabbitMQConsumer(
            use_case=self.process_audio_video_media(),
            host=os.getenv("RABBITMQ_HOST", "localhost"),
            queue=os.getenv("VIDEOS_CONVERTED_QUEUE", "videos.converted"),
        )


_container: Container | None = None


def get_container() -> Container:
    global _container
    if _container is None:
        _container = Container()
    return _container
