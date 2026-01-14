import os
import dotenv

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from core._shared.infrastructure.auth.jwt_auth_service import JwtAuthService

dotenv.load_dotenv()

class IsAuthenticated(BasePermission):
    message = "Invalid or expired token."

    def has_permission(self, request: Request, view: APIView) -> bool:
        token: str = request.headers.get("Authorization", "")
        if not JwtAuthService(token).is_authenticated():
            return False
        return True


class IsAdmin(BasePermission):
    message = "User does not have admin privileges."

    def has_permission(self, request: Request, view: APIView) -> bool:
        token: str = request.headers.get("Authorization", "")
        if not JwtAuthService(token).has_role(os.getenv("DEFAULT_REALM_ADMIN_ROLE_NAME", "admin")):
            return False
        return True
