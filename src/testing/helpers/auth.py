from contextlib import contextmanager
from unittest.mock import MagicMock, patch


@contextmanager
def deny_authentication():
    """Patch auth service to reject requests (for API auth tests)."""
    with patch("django_project.permissions.get_container") as mock_get_container:
        mock_auth = MagicMock()
        mock_auth.is_authenticated.return_value = False
        mock_auth.has_role.return_value = False
        mock_container = MagicMock()
        mock_container.auth_service.return_value = mock_auth
        mock_get_container.return_value = mock_container
        yield
