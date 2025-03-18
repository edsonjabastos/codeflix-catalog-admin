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

from core.category.application.use_cases.create_category import (
    CreateCategory,
    CreateCategoryRequest,
)
from core.category.application.use_cases.delete_category import (
    DeleteCategory,
    DeleteCategoryRequest,
)
from core.category.application.use_cases.exceptions import CategoryNotFound
from core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
)
from core.category.application.use_cases.list_category import ListCategory
from core.category.application.use_cases.update_category import (
    UpdateCategory,
    UpdateCategoryRequest,
)
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.serializers import (
    CreateCategoryRequestSerializer,
    DeleteCategoryRequestSerializer,
    ListCategoryResponseSerializer,
    PatchCategoryRequestSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer,
    CreateCategoryResponseSerializer,
    UpdateCategoryRequestSerializer,
)


class CategoryViewSet(viewsets.ViewSet):

    def list(self, request: Request) -> Response:
        order_by: str = request.query_params.get("order_by", "name")
        current_page: int = int(request.query_params.get("current_page", 1))
        input: ListCategory.Input = ListCategory.Input(
            order_by=order_by, current_page=current_page
        )
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output: ListCategory.ListOutput = use_case.execute(input=input)

        serializer: ListCategoryResponseSerializer = ListCategoryResponseSerializer(
            instance=output
        )

        return Response(
            status=HTTP_200_OK,
            data=serializer.data,
        )

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        serializer: RetrieveCategoryRequestSerializer = (
            RetrieveCategoryRequestSerializer(data={"id": pk})
        )
        serializer.is_valid(raise_exception=True)

        use_case: GetCategory = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            result = use_case.execute(
                request=GetCategoryRequest(id=serializer.validated_data["id"])
            )
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        output: RetrieveCategoryResponseSerializer = RetrieveCategoryResponseSerializer(
            instance=result
        )

        return Response(
            status=HTTP_200_OK,
            data=output.data,
        )

    def create(self, request: Request) -> Response:
        serializer: CreateCategoryRequestSerializer = CreateCategoryRequestSerializer(
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        use_case: CreateCategory = CreateCategory(
            repository=DjangoORMCategoryRepository()
        )

        input: CreateCategoryRequest = CreateCategoryRequest(
            **serializer.validated_data
        )
        output = use_case.execute(input)

        return Response(
            status=HTTP_201_CREATED,
            data=CreateCategoryResponseSerializer(instance=output).data,
        )

    def update(self, request: Request, pk: UUID) -> Response:
        serializer: UpdateCategoryRequestSerializer = UpdateCategoryRequestSerializer(
            data={**request.data, "id": pk}
        )
        serializer.is_valid(raise_exception=True)

        input: UpdateCategoryRequest = UpdateCategoryRequest(
            **serializer.validated_data
        )
        use_case: UpdateCategory = UpdateCategory(
            repository=DjangoORMCategoryRepository()
        )
        try:
            use_case.execute(input=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def partial_update(self, request: Request, pk: UUID) -> Response:
        print(request.data)
        serializer: PatchCategoryRequestSerializer = PatchCategoryRequestSerializer(
            data={**request.data, "id": pk}
        )
        serializer.is_valid(raise_exception=True)

        input: UpdateCategoryRequest = UpdateCategoryRequest(
            **serializer.validated_data
        )

        use_case: UpdateCategory = UpdateCategory(
            repository=DjangoORMCategoryRepository()
        )

        try:
            use_case.execute(input=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)

    def destroy(self, request: Request, pk: UUID) -> Response:
        serializer: DeleteCategoryRequestSerializer = DeleteCategoryRequestSerializer(
            data={"id": pk}
        )
        serializer.is_valid(raise_exception=True)

        input: DeleteCategoryRequest = DeleteCategoryRequest(
            **serializer.validated_data
        )
        use_case: DeleteCategory = DeleteCategory(
            repository=DjangoORMCategoryRepository()
        )

        try:
            use_case.execute(request=input)
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        return Response(status=HTTP_204_NO_CONTENT)
