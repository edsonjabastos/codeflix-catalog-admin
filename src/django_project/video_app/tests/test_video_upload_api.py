from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.test import APIClient

from core.castmember.domain.castmember import CastMember
from core.category.domain.category import Category
from core.genre.domain.genre import Genre
from core.video.domain.value_objects import MediaStatus, MediaType
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


@pytest.mark.django_db
class TestVideoUploadAPI:
    @patch(
        "django_project.adapters.storage.file_checksum_service.FileChecksumService.compute",
        return_value="test-checksum",
    )
    def test_upload_video_media_via_api(
        self,
        _mock_checksum,
        api_client: APIClient,
        category_movie: Category,
        genre_action: Genre,
        cast_member_actor: CastMember,
        category_repository: DjangoORMCategoryRepository,
        genre_repository: DjangoORMGenreRepository,
        cast_member_repository: DjangoORMCastMemberRepository,
        video_repository: DjangoORMVideoRepository,
    ) -> None:
        category_repository.save(category_movie)
        genre_repository.save(genre_action)
        cast_member_repository.save(cast_member_actor)

        create_response = api_client.post(
            "/api/videos/",
            data={
                "title": "Upload Test Video",
                "description": "Video for upload API test",
                "launch_year": 2024,
                "duration": "60.0",
                "rating": "L",
                "categories": [str(category_movie.id)],
                "genres": [str(genre_action.id)],
                "cast_members": [str(cast_member_actor.id)],
            },
        )
        assert create_response.status_code == HTTP_201_CREATED
        video_id = create_response.data["id"]

        upload_file = SimpleUploadedFile(
            name="sample.mp4",
            content=b"fake-video-content",
            content_type="video/mp4",
        )

        upload_response = api_client.patch(
            f"/api/videos/{video_id}/",
            data={"video_file": upload_file, "media_type": "VIDEO"},
            format="multipart",
        )

        assert upload_response.status_code == HTTP_200_OK

        video = video_repository.get_by_id(video_id)
        assert video is not None
        assert video.video is not None
        assert video.video.name == "sample.mp4"
        assert video.video.checksum == "test-checksum"
        assert video.video.status == MediaStatus.PENDING
        assert video.video.media_type == MediaType.VIDEO
