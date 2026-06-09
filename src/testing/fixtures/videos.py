import pytest

from django_project.adapters.persistence.django.video_repository import (
    DjangoORMVideoRepository,
)


@pytest.fixture
def video_repository() -> DjangoORMVideoRepository:
    return DjangoORMVideoRepository()
