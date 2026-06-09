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
from core.video.application.use_cases.get_video import GetVideo
from core.video.application.use_cases.upload_video import UploadVideo
from core.video.domain.value_objects import MediaType
from django_project.adapters.composition.container import get_container
from django_project.video_app.serializers import (
    CreateVideoInputSerializer,
    CreateVideoOutputSerializer,
    GetVideoInputSerializer,
    GetVideoOutputSerializer,
)
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)
from django_project.permissions import IsAuthenticated, IsAdmin


class VideoViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated & IsAdmin]

    def create(self, request: Request) -> Response:
        serializer: CreateVideoInputSerializer = CreateVideoInputSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        input_data = serializer.validated_data

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

        try:
            output = get_container().create_video_without_media().execute(input=input_obj)
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

        try:
            result: GetVideo.Output = get_container().get_video().execute(
                input=GetVideo.Input(id=serializer.validated_data["id"])
            )
        except VideoNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        output: GetVideoOutputSerializer = GetVideoOutputSerializer(instance=result)

        return Response(
            status=HTTP_200_OK,
            data=output.data,
        )

    def partial_update(self, request: Request, pk: UUID | None = None) -> Response:
        file = request.FILES.get("video_file")
        content = file.read()
        content_type = file.content_type

        media_type_str = request.data.get("media_type", "VIDEO")
        try:
            media_type = MediaType[media_type_str]
        except KeyError:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={
                    "error": f"Invalid media_type: {media_type_str}. Must be VIDEO or TRAILER."
                },
            )

        try:
            get_container().upload_video().execute(
                input=UploadVideo.Input(
                    video_id=pk,
                    file_name=file.name,
                    content=content,
                    content_type=content_type,
                    media_type=media_type,
                )
            )
        except VideoNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_200_OK)

    def list(self, request: Request) -> Response:
        raise NotImplementedError("List method is not implemented.")

    def destroy(self, request: Request, pk: str | None = None) -> Response:
        raise NotImplementedError("Destroy method is not implemented.")

    def update(self, request: Request, pk: str | None = None) -> Response:
        raise NotImplementedError("Update method is not implemented.")
