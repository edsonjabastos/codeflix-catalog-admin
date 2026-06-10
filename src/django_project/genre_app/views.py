from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
)

from core.genre.application.use_cases.create_genre import CreateGenre
from core.genre.application.use_cases.delete_genre import DeleteGenre
from core.genre.application.use_cases.get_genre import GetGenre
from core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)
from core.genre.application.use_cases.list_genre import ListGenre
from core.genre.application.use_cases.update_genre import UpdateGenre
from config import DEFAULT_PAGE_SIZE
from django_project.adapters.composition.container import get_container
from django_project.genre_app.serializers import (
    CreateGenreInputSerializer,
    CreateGenreResponseSerializer,
    DeleteGenreInputSerializer,
    ListGenreOutputSerializer,
    RetrieveGenreRequestSerializer,
    RetrieveGenreResponseSerializer,
    UpdateGenreInputSerializer,
)
from django_project.permissions import IsAuthenticated, IsAdmin


class GenreViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated & IsAdmin]

    def list(self, request: Request) -> Response:
        order_by: str = request.query_params.get("order_by", "name")
        current_page: int = int(request.query_params.get("current_page", 1))
        page_size: int = int(request.query_params.get("page_size", DEFAULT_PAGE_SIZE))
        input: ListGenre.Input = ListGenre.Input(
            order_by=order_by, current_page=current_page, page_size=page_size
        )
        output = get_container().list_genre().execute(input)

        serializer: ListGenreOutputSerializer = ListGenreOutputSerializer(
            instance=output
        )

        return Response(
            status=HTTP_200_OK,
            data=serializer.data,
        )

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        serializer: RetrieveGenreRequestSerializer = RetrieveGenreRequestSerializer(
            data={"id": pk}
        )
        serializer.is_valid(raise_exception=True)

        try:
            result: GetGenre.Output = get_container().get_genre().execute(
                input=GetGenre.Input(id=serializer.validated_data["id"])
            )
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        output: RetrieveGenreResponseSerializer = RetrieveGenreResponseSerializer(
            instance=result
        )

        return Response(
            status=HTTP_200_OK,
            data=output.data,
        )

    def create(self, request: Request) -> Response:
        serializer: CreateGenreInputSerializer = CreateGenreInputSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        input: CreateGenre.Input = CreateGenre.Input(**serializer.validated_data)

        try:
            output = get_container().create_genre().execute(input=input)
        except (InvalidGenre, RelatedCategoriesNotFound) as e:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(e)},
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateGenreResponseSerializer(instance=output).data,
        )

    def destroy(self, request: Request, pk: UUID) -> Response:
        serializer: DeleteGenreInputSerializer = DeleteGenreInputSerializer(
            data={"id": pk}
        )
        serializer.is_valid(raise_exception=True)

        input: DeleteGenre.Input = DeleteGenre.Input(**serializer.validated_data)

        try:
            get_container().delete_genre().execute(input=input)
        except GenreNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def update(self, request: Request, pk: UUID) -> Response:
        serializer: UpdateGenreInputSerializer = UpdateGenreInputSerializer(
            data={**request.data, "id": pk}
        )
        serializer.is_valid(raise_exception=True)
        input: UpdateGenre.Input = UpdateGenre.Input(**serializer.validated_data)
        try:
            get_container().update_genre().execute(input=input)
        except GenreNotFound as e:
            return Response(status=HTTP_404_NOT_FOUND, data={"error": str(e)})
        except (InvalidGenre, RelatedCategoriesNotFound) as e:
            return Response(status=HTTP_400_BAD_REQUEST, data={"error": str(e)})
        return Response(status=HTTP_204_NO_CONTENT)
