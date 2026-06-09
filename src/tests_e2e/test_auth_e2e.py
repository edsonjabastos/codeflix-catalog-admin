"""E2E authentication tests with real Keycloak."""

import pytest
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.test import APIClient


@pytest.mark.django_db
class TestAuthE2E:
    def test_unauthenticated_request_is_rejected(
        self, unauthenticated_client: APIClient
    ) -> None:
        response = unauthenticated_client.get("/api/categories/")
        assert response.status_code == HTTP_403_FORBIDDEN
