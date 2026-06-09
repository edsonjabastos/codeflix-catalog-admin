"""
E2E test fixtures providing authenticated API clients.

These tests require Keycloak to be running with the configured realm/user.
"""

import pytest
from rest_framework.test import APIClient

from django_project.adapters.auth.keycloak_token_helper import (
    get_token_with_retry,
    KeycloakTokenError,
)


@pytest.fixture(scope="session")
def keycloak_token() -> str:
    """Acquire a Keycloak token once per session (with startup retry)."""
    try:
        return get_token_with_retry(max_retries=5, retry_delay=2.0)
    except KeycloakTokenError as e:
        pytest.skip(f"Keycloak not available for E2E tests: {e}")


@pytest.fixture
def authenticated_client(keycloak_token: str) -> APIClient:
    """APIClient with a valid JWT from Keycloak."""
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {keycloak_token}")
    return client


@pytest.fixture
def api_client(authenticated_client: APIClient) -> APIClient:
    """Alias used by existing E2E tests."""
    return authenticated_client
