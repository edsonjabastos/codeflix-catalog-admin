from uuid import UUID
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND

from core.category.application.use_cases.exceptions import CategoryNotFound
from core.category.application.use_cases.get_category import (
    GetCategory,
    GetCategoryRequest,
)
from core.category.application.use_cases.list_category import (
    ListCategory,
    ListCategoryRequest,
)
from django_project.category_app.repository import DjangoORMCategoryRepository
from django_project.category_app.serializers import (
    ListCategoryResponseSerializer,
    RetrieveCategoryRequestSerializer,
    RetrieveCategoryResponseSerializer,
)


class CategoryViewSet(viewsets.ViewSet):

    def list(self, request: Request) -> Response:
        input = ListCategoryRequest()
        use_case = ListCategory(repository=DjangoORMCategoryRepository())
        output = use_case.execute(input)

        serializer = ListCategoryResponseSerializer(instance=output)

        return Response(
            status=HTTP_200_OK,
            data=serializer.data,
        )

    def retrieve(self, request: Request, pk: str | None = None) -> Response:
        serializer = RetrieveCategoryRequestSerializer(data={"id": pk})
        serializer.is_valid(raise_exception=True)

        use_case = GetCategory(repository=DjangoORMCategoryRepository())

        try:
            result = use_case.execute(
                request=GetCategoryRequest(id=serializer.validated_data["id"])
            )
        except CategoryNotFound:
            return Response(status=HTTP_404_NOT_FOUND)

        output = RetrieveCategoryResponseSerializer(instance=result)

        return Response(
            status=HTTP_200_OK,
            data=output.data,
        )
