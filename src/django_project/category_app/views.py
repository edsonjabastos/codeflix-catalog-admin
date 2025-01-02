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
                    "id": "9bcf7e5a-3f4c-4f8a-8f9b-1b7e5f3b7c9b",
                    "name": "Movie",
                    "description": "Movie category",
                    "is_active": True,
                },
                {
                    "id": "9bcf7e5a-3f4c-4f8a-8f9b-1b7e5f3b7c9b",
                    "name": "Documentary",
                    "description": "Documentary category",
                    "is_active": True,
                },
            ],
        )
