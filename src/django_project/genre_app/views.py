from re import U
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

from core.genre.application.use_cases.create_genre import (
    CreateGenre,
)
from core.genre.application.use_cases.delete_genre import (
    DeleteGenre,
)
from core.genre.application.exceptions import (
    GenreNotFound,
    InvalidGenre,
    RelatedCategoriesNotFound,
)

# from core.genre.application.use_cases.get_genre import (
#     GetGenre,
# )
from core.genre.application.use_cases.list_genre import (
    ListGenre,
)
from core.genre.application.use_cases.update_genre import (
    UpdateGenre,
)
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.genre_app.repository import DjangoORMGenreRepository
from django_project.genre_app.serializers import (
    # CreateGenreRequestSerializer,
    # DeleteGenreRequestSerializer,
    CreateGenreInputSerializer,
    CreateGenreResponseSerializer,
    ListGenreOutputSerializer,
    # PatchGenreRequestSerializer,
    # RetrieveGenreRequestSerializer,
    # RetrieveGenreResponseSerializer,
    # CreateGenreResponseSerializer,
    # UpdateGenreRequestSerializer,
)


class GenreViewSet(viewsets.ViewSet):

    def list(self, request: Request) -> Response:
        use_case = ListGenre(genre_repository=DjangoORMGenreRepository())
        input: ListGenre.Input = ListGenre.Input()
        output: ListGenre.Output = use_case.execute(input)

        serializer: ListGenreOutputSerializer = ListGenreOutputSerializer(
            instance=output
        )

        return Response(
            status=HTTP_200_OK,
            data=serializer.data,
        )

    def create(self, request: Request) -> Response:
        serializer: CreateGenreInputSerializer = CreateGenreInputSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        input: CreateGenre.Input = CreateGenre.Input(**serializer.validated_data)

        use_case: CreateGenre = CreateGenre(
            genre_repository=DjangoORMGenreRepository(),
            category_repository=DjangoORMCategoryRepository(),
        )
        try:
            output = use_case.execute(input=input)
        except (InvalidGenre, RelatedCategoriesNotFound) as e:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(e)},
            )

        return Response(
            status=HTTP_201_CREATED,
            data=CreateGenreResponseSerializer(instance=output).data,
        )

    # def retrieve(self, request: Request, pk: str | None = None) -> Response:
    #     serializer: RetrieveGenreRequestSerializer = RetrieveGenreRequestSerializer(
    #         data={"id": pk}
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     use_case: GetGenre = GetGenre(repository=DjangoORMGenreRepository())

    #     try:
    #         result = use_case.execute(
    #             request=GetGenreRequest(id=serializer.validated_data["id"])
    #         )
    #     except GenreNotFound:
    #         return Response(status=HTTP_404_NOT_FOUND)

    #     output: RetrieveGenreResponseSerializer = RetrieveGenreResponseSerializer(
    #         instance=result
    #     )

    #     return Response(
    #         status=HTTP_200_OK,
    #         data=output.data,
    #     )

    # def update(self, request: Request, pk: UUID) -> Response:
    #     serializer: UpdateGenreRequestSerializer = UpdateGenreRequestSerializer(
    #         data={**request.data, "id": pk}
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     input: UpdateGenreRequest = UpdateGenreRequest(**serializer.validated_data)
    #     use_case: UpdateGenre = UpdateGenre(repository=DjangoORMGenreRepository())
    #     try:
    #         use_case.execute(input=input)
    #     except GenreNotFound:
    #         return Response(status=HTTP_404_NOT_FOUND)

    #     return Response(status=HTTP_204_NO_CONTENT)

    # def partial_update(self, request: Request, pk: UUID) -> Response:
    #     print(request.data)
    #     serializer: PatchGenreRequestSerializer = PatchGenreRequestSerializer(
    #         data={**request.data, "id": pk}
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     input: UpdateGenreRequest = UpdateGenreRequest(**serializer.validated_data)

    #     use_case: UpdateGenre = UpdateGenre(repository=DjangoORMGenreRepository())

    #     try:
    #         use_case.execute(input=input)
    #     except GenreNotFound:
    #         return Response(status=HTTP_404_NOT_FOUND)

    #     return Response(status=HTTP_204_NO_CONTENT)

    # def destroy(self, request: Request, pk: UUID) -> Response:
    #     serializer: DeleteGenreRequestSerializer = DeleteGenreRequestSerializer(
    #         data={"id": pk}
    #     )
    #     serializer.is_valid(raise_exception=True)

    #     input: DeleteGenreRequest = DeleteGenreRequest(**serializer.validated_data)
    #     use_case: DeleteGenre = DeleteGenre(repository=DjangoORMGenreRepository())

    #     try:
    #         use_case.execute(request=input)
    #     except GenreNotFound:
    #         return Response(status=HTTP_404_NOT_FOUND)

    #     return Response(status=HTTP_204_NO_CONTENT)
