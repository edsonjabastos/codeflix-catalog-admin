# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


class CategoryViewSet(viewsets.ViewSet):

    def list(self, request: Request) -> Response:
        return Response(
            status=HTTP_200_OK,
            data=[
                {
                    "id": "6fd173e3-9fd2-4443-add0-ee83c27d4936",
                    "name": "Movie",
                    "description": "Movie category",
                    "is_active": True,
                },
                {
                    "id": "c8b17960-69c0-4254-a569-3715cfbfc114",
                    "name": "Documentary",
                    "description": "Documentary category",
                    "is_active": True,
                },
            ],
        )
