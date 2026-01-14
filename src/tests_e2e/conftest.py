"""
E2E test fixtures providing authenticated API clients.

These tests require Keycloak to be running with the configured realm/user.
"""

import pytest
from rest_framework.test import APIClient

from core._shared.infrastructure.auth.keycloak_token_helper import (
    get_keycloak_token,
    get_token_with_retry,
    KeycloakTokenError,
)


@pytest.fixture(scope="session")
def keycloak_token() -> str:
    """
    Session-scoped fixture that acquires a token from Keycloak once per test session.
    
    Uses retry logic to wait for Keycloak to be ready (useful in CI/CD).
    """
    try:
        # Use retry to handle Keycloak startup delay
        token = get_token_with_retry(max_retries=5, retry_delay=2.0)
        return token
    except KeycloakTokenError as e:
        pytest.skip(f"Keycloak not available for E2E tests: {e}")


@pytest.fixture
def authenticated_client(keycloak_token: str) -> APIClient:
    """
    Provides an APIClient pre-configured with a valid JWT token from Keycloak.
    """
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f"Bearer {keycloak_token}")
    return client


@pytest.fixture
def api_client(authenticated_client: APIClient) -> APIClient:
    """
    Alias for authenticated_client to maintain compatibility with existing test code.
    
    E2E tests that use `api_client = APIClient()` directly will now use
    this fixture automatically when the test method accepts `api_client` as parameter.
    """
    return authenticated_client
