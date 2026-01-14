"""
Keycloak token acquisition helper for E2E tests and scripts.

This module provides utilities to programmatically obtain JWT tokens from Keycloak
using the OAuth2 Resource Owner Password Credentials (direct grant) flow.
"""

import os
import requests
from typing import Optional

import dotenv

dotenv.load_dotenv()


class KeycloakTokenError(Exception):
    """Raised when token acquisition fails."""
    pass


def get_keycloak_token(
    host: Optional[str] = None,
    realm: Optional[str] = None,
    client_id: Optional[str] = None,
    username: Optional[str] = None,
    password: Optional[str] = None,
    timeout: int = 10,
) -> str:
    """
    Acquire an access token from Keycloak using direct grant flow.
    
    All parameters default to values from environment variables if not provided.
    
    Args:
        host: Keycloak host (default: localhost:8080)
        realm: Realm name (default: DEFAULT_PROJECT_REALM env var)
        client_id: Client ID (default: DEFAULT_REALM_CLIENT_ID env var)
        username: Username (default: DEFAULT_REALM_ADMIN_USER env var)
        password: Password (default: DEFAULT_REALM_ADMIN_PASSWORD env var)
        timeout: Request timeout in seconds
        
    Returns:
        str: The access token
        
    Raises:
        KeycloakTokenError: If token acquisition fails
    """
    # Use environment variables as defaults
    host = host or os.getenv("KEYCLOAK_HOST", "localhost:8080")
    realm = realm or os.getenv("DEFAULT_PROJECT_REALM", "codeflix")
    client_id = client_id or os.getenv("DEFAULT_REALM_CLIENT_ID", "codeflix-frontend")
    username = username or os.getenv("DEFAULT_REALM_ADMIN_USER", "admin")
    password = password or os.getenv("DEFAULT_REALM_ADMIN_PASSWORD", "admin")
    
    token_url = f"http://{host}/realms/{realm}/protocol/openid-connect/token"
    
    try:
        response = requests.post(
            token_url,
            data={
                "grant_type": "password",
                "client_id": client_id,
                "username": username,
                "password": password,
            },
            timeout=timeout,
        )
        response.raise_for_status()
        
        token_data = response.json()
        access_token = token_data.get("access_token")
        
        if not access_token:
            raise KeycloakTokenError("No access_token in response")
            
        return access_token
        
    except requests.exceptions.ConnectionError as e:
        raise KeycloakTokenError(
            f"Cannot connect to Keycloak at {token_url}. "
            "Make sure Keycloak is running (docker compose up -d keycloak)"
        ) from e
    except requests.exceptions.HTTPError as e:
        error_detail = ""
        try:
            error_detail = response.json().get("error_description", response.text)
        except:
            error_detail = response.text
        raise KeycloakTokenError(
            f"Keycloak token request failed: {e}. Detail: {error_detail}"
        ) from e
    except requests.exceptions.Timeout as e:
        raise KeycloakTokenError(
            f"Keycloak request timed out after {timeout}s"
        ) from e


def get_token_with_retry(max_retries: int = 30, retry_delay: float = 2.0, **kwargs) -> str:
    """
    Acquire a token with retries, useful when waiting for Keycloak to start.
    
    Args:
        max_retries: Maximum number of retry attempts
        retry_delay: Seconds to wait between retries
        **kwargs: Arguments to pass to get_keycloak_token()
        
    Returns:
        str: The access token
        
    Raises:
        KeycloakTokenError: If all retries fail
    """
    import time
    
    last_error = None
    for attempt in range(max_retries):
        try:
            return get_keycloak_token(**kwargs)
        except KeycloakTokenError as e:
            last_error = e
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
    
    raise KeycloakTokenError(
        f"Failed to get token after {max_retries} attempts. Last error: {last_error}"
    )


if __name__ == "__main__":
    # CLI usage: python -m core._shared.infrastructure.auth.keycloak_token_helper
    try:
        token = get_keycloak_token()
        print(token)
    except KeycloakTokenError as e:
        print(f"Error: {e}", file=__import__("sys").stderr)
        exit(1)
