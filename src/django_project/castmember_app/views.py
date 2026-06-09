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

from core.castmember.application.use_cases.create_castmember import CreateCastMember
from core.castmember.application.use_cases.delete_castmember import DeleteCastMember
from core.castmember.application.use_cases.list_castmember import ListCastMember
from core.castmember.application.use_cases.update_castmember import UpdateCastMember
from core.castmember.application.exceptions import CastMemberNotFound, InvalidCastMember
from config import DEFAULT_PAGE_SIZE
from django_project.adapters.composition.container import get_container
from django_project.castmember_app.serializers import (
    CreateCastMemberInputSerializer,
    CreateCastMemberOutputSerializer,
    DeleteCastMemberInputSerializer,
    ListCastMemberOutputSerializer,
    UpdateCastMemberInputSerializer,
)
from django_project.permissions import IsAuthenticated, IsAdmin


class CastMemberViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated & IsAdmin]

    def list(self, request: Request) -> Response:
        order_by: str = request.query_params.get("order_by", "name")
        current_page: int = int(request.query_params.get("current_page", 1))
        page_size: int = int(request.query_params.get("page_size", DEFAULT_PAGE_SIZE))
        input: ListCastMember.Input = ListCastMember.Input(
            order_by=order_by, current_page=current_page, page_size=page_size
        )
        output = get_container().list_castmember().execute(input)

        serializer: ListCastMemberOutputSerializer = ListCastMemberOutputSerializer(
            instance=output
        )

        return Response(data=serializer.data, status=HTTP_200_OK)

    def create(self, request: Request) -> Response:
        serializer: CreateCastMemberInputSerializer = CreateCastMemberInputSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        input: CreateCastMember.Input = CreateCastMember.Input(
            **serializer.validated_data
        )

        try:
            output: CreateCastMember.Output = (
                get_container().create_castmember().execute(input)
            )
        except InvalidCastMember as e:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(e)},
            )
        return Response(
            status=HTTP_201_CREATED, data=CreateCastMemberOutputSerializer(output).data
        )

    def destroy(self, request: Request, pk: UUID) -> Response:
        serializer: DeleteCastMemberInputSerializer = DeleteCastMemberInputSerializer(
            data={"id": pk}
        )
        serializer.is_valid(raise_exception=True)

        input: DeleteCastMember.Input = DeleteCastMember.Input(
            **serializer.validated_data
        )

        try:
            get_container().delete_castmember().execute(input)
        except CastMemberNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def update(self, request: Request, pk: UUID) -> Response:
        serializer: UpdateCastMemberInputSerializer = UpdateCastMemberInputSerializer(
            data={**request.data, "id": pk}
        )
        serializer.is_valid(raise_exception=True)

        input: UpdateCastMember.Input = UpdateCastMember.Input(
            **serializer.validated_data
        )

        try:
            get_container().update_castmember().execute(input)
        except CastMemberNotFound as e:
            return Response(
                status=HTTP_404_NOT_FOUND,
                data={"error": str(e)},
            )
        except InvalidCastMember as e:
            return Response(
                status=HTTP_400_BAD_REQUEST,
                data={"error": str(e)},
            )

        return Response(status=HTTP_204_NO_CONTENT)
