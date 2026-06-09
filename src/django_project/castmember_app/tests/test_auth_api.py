import pytest
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.test import APIClient

from testing.helpers.auth import deny_authentication


@pytest.mark.django_db
class TestCastMemberAuthAPI:
    def test_unauthenticated_request_is_rejected(
        self, unauthenticated_client: APIClient
    ) -> None:
        with deny_authentication():
            response = unauthenticated_client.get("/api/cast_members/")

        assert response.status_code == HTTP_403_FORBIDDEN
