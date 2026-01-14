"""
Global pytest configuration and fixtures for all tests.

This module provides:
- mock_jwt_auth: Auto-used fixture that mocks JWT authentication for unit/integration tests
- authenticated_client: APIClient with real Keycloak token for E2E tests
- keycloak_token: Session-scoped fixture for cached token acquisition
"""

import os
import pytest
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient

# Check if we're running E2E tests (need real Keycloak or/and RabbitMQ consumer)
E2E_TEST_MARKERS = ["e2e", "integration"]


def is_e2e_test(item) -> bool:
    """Check if a test item is marked as E2E or integration test."""
    for marker in item.iter_markers():
        if marker.name in E2E_TEST_MARKERS:
            return True
    # Also check if test is in tests_e2e directory
    if "tests_e2e" in str(item.fspath):
        return True
    return False


@pytest.fixture(autouse=True)
def mock_jwt_auth(request):
    """
    Automatically mock JWT authentication for all tests EXCEPT E2E tests.
    
    This fixture patches JwtAuthService to always return authenticated=True
    and has_role=True, allowing unit/integration tests to run without
    Keycloak dependency.
    
    E2E tests (in tests_e2e/ directory or marked with @pytest.mark.e2e)
    will skip this mock and use real authentication.
    """
    # Skip mocking for E2E tests - they need real Keycloak
    if is_e2e_test(request.node):
        yield None
        return

    with patch("django_project.permissions.JwtAuthService") as mock_jwt:
        mock_instance = MagicMock()
        mock_instance.is_authenticated.return_value = True
        mock_instance.has_role.return_value = True
        mock_jwt.return_value = mock_instance
        yield mock_jwt


@pytest.fixture(scope="session")
def keycloak_token() -> str:
    """
    Session-scoped fixture that acquires a token from Keycloak once per test session.
    
    Uses OAuth2 Resource Owner Password Credentials (direct grant) flow.
    Requires Keycloak to be running and configured with the realm/user from .env
    
    Returns:
        str: The access token from Keycloak
    """
    from core._shared.infrastructure.auth.keycloak_token_helper import get_keycloak_token
    
    try:
        token = get_keycloak_token()
        return token
    except Exception as e:
        pytest.skip(f"Keycloak not available: {e}")


@pytest.fixture
def authenticated_client(keycloak_token: str) -> APIClient:
    """
    Provides an APIClient pre-configured with a valid JWT token from Keycloak.
    
    Use this fixture for E2E tests that need to make authenticated API calls.
    
    Example:
        def test_create_category(authenticated_client):
            response = authenticated_client.post("/api/categories/", data={...})
            assert response.status_code == 201
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {keycloak_token}")
    return client


@pytest.fixture
def unauthenticated_client() -> APIClient:
    """
    Provides an APIClient without authentication.
    
    Use this fixture to test that endpoints properly reject unauthenticated requests.
    """
    return APIClient()
