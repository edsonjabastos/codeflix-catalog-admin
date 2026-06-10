"""
Global pytest configuration and fixtures for all tests.

Provides JWT mocking for fast tests, marker auto-registration, and shared clients.
E2E-specific Keycloak fixtures live in tests_e2e/conftest.py.
"""

from unittest.mock import MagicMock, patch

import pytest
from rest_framework.test import APIClient

pytest_plugins = [
    "testing.fixtures.categories",
    "testing.fixtures.genres",
    "testing.fixtures.castmembers",
    "testing.fixtures.videos",
]

TEST_BEARER_TOKEN = "Bearer test-token"


def is_e2e_test(item) -> bool:
    """Tests that must use real Keycloak instead of the JWT mock."""
    if item.get_closest_marker("e2e"):
        return True
    return "tests_e2e" in str(item.fspath)


def pytest_collection_modifyitems(config, items):
    """Assign markers from directory layout so tests are selectable by layer."""
    for item in items:
        path = str(item.fspath).replace("\\", "/")

        if "tests_e2e" in path:
            item.add_marker(pytest.mark.e2e)
            continue

        if "_app/tests/" in path or "_app/test/" in path:
            item.add_marker(pytest.mark.api)
            continue

        if "/adapters/" in path and "/tests/" in path:
            if "integration" in path or "test_video_conversion_integration" in path:
                item.add_marker(pytest.mark.integration)
            else:
                item.add_marker(pytest.mark.unit)
            continue

        if "/integration/" in path:
            item.add_marker(pytest.mark.integration)
            continue

        if any(
            segment in path
            for segment in (
                "/unit/",
                "/domain/",
                "/in_memory/tests/",
            )
        ):
            item.add_marker(pytest.mark.unit)
            continue

        if "/core/" in path and "/tests/" in path:
            item.add_marker(pytest.mark.unit)


@pytest.fixture(autouse=True)
def mock_jwt_auth(request):
    """
    Mock JWT authentication for fast tests.

    Treats any non-empty Authorization header as an authenticated admin user.
    E2E and consumer tests skip this fixture and use real Keycloak.
    """
    if is_e2e_test(request.node) or request.node.get_closest_marker("real_auth"):
        yield None
        return

    with patch("django_project.permissions.get_container") as mock_get_container:
        mock_container = MagicMock()
        mock_auth = MagicMock()
        mock_auth.is_authenticated.return_value = True
        mock_auth.has_role.return_value = True
        mock_container.auth_service.return_value = mock_auth
        mock_get_container.return_value = mock_container
        yield mock_get_container


@pytest.fixture
def api_client() -> APIClient:
    """APIClient with a test bearer token (works with mock_jwt_auth)."""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=TEST_BEARER_TOKEN)
    return client


@pytest.fixture
def unauthenticated_client() -> APIClient:
    """APIClient without authentication headers."""
    return APIClient()
