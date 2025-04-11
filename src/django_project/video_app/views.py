from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from core.video.application.use_cases.create_video_without_media import (
    CreateVideoWithoutMedia,
)
from core.video.application.exceptions import InvalidVideo, RelatedEntitiesNotFound
from django_project.video_app.repository import DjangoORMVideoRepository
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.repository import DjangoORMGenreRepository
from django_project.castmember_app.repository import DjangoORMCastMemberRepository

from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
)


from django_project.video_app.serializers import (
    CreateVideoInputSerializer,
    CreateVideoOutputSerializer,
)


class VideoViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer: CreateVideoInputSerializer = CreateVideoInputSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        input_data = serializer.validated_data

        # Create the Input object for use case
        input_obj = CreateVideoWithoutMedia.Input(
            title=input_data["title"],
            description=input_data["description"],
            launch_year=input_data["launch_year"],
            duration=input_data["duration"],
            rating=input_data["rating"],
            categories=input_data["categories"],
            genres=input_data["genres"],
            cast_members=input_data["cast_members"],
        )

        # Create use case instance
        use_case = CreateVideoWithoutMedia(
            video_repository=DjangoORMVideoRepository(),
            category_repository=DjangoORMCategoryRepository(),
            genre_repository=DjangoORMGenreRepository(),
            cast_member_repository=DjangoORMCastMemberRepository(),
        )

        try:
            output = use_case.execute(input=input_obj)
        except (InvalidVideo, RelatedEntitiesNotFound) as e:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(e)},
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateVideoOutputSerializer(instance=output).data,
        )
