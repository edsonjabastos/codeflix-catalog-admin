from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from core.video.application.use_cases.create_video_without_media import (
    CreateVideoWithoutMedia,
)
from core.video.application.exceptions import (
    InvalidVideo,
    RelatedEntitiesNotFound,
    VideoNotFound,
)
from django_project.video_app.repository import DjangoORMVideoRepository
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.repository import DjangoORMGenreRepository
from django_project.castmember_app.repository import DjangoORMCastMemberRepository

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)


from django_project.video_app.serializers import (
    CreateVideoInputSerializer,
    CreateVideoOutputSerializer,
    GetVideoInputSerializer,
    GetVideoOutputSerializer,
    VideoOutputSerializer,
)
from core.video.application.use_cases.get_video import GetVideo


class VideoViewSet(viewsets.ViewSet):
    def create(self, request: Request) -> Response:
        serializer: CreateVideoInputSerializer = CreateVideoInputSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        input_data = serializer.validated_data

        # request_data = request.data
        input_data = {
            "title": input_data.get("title"),
            "description": input_data.get("description"),
            "launch_year": input_data.get("launch_year"),
            "duration": input_data.get("duration"),
            "rating": input_data.get("rating"),
            "categories": input_data.get("categories"),
            "genres": input_data.get("genres"),
            "cast_members": input_data.get("cast_members"),
        }

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

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        serializer: GetVideoInputSerializer = GetVideoInputSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case: GetVideo = GetVideo(video_repository=DjangoORMVideoRepository())

        try:
            result: GetVideo.Output = use_case.execute(
                input=GetVideo.Input(id=serializer.validated_data["id"])
            )
        except VideoNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        output: GetVideoOutputSerializer = GetVideoOutputSerializer(instance=result)

        return Response(
            status=HTTP_200_OK,
            data=output.data,
        )
