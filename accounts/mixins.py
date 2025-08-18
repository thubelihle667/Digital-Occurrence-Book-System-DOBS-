from rest_framework.permissions import BasePermission
from rest_framework.response import Response

class RoleRequiredMixin(BasePermission):
    """
    DRF permission class to restrict access based on user roles.
    """
    allowed_roles = []

    def has_permission(self, request, view):
        user = request.user
        if not user.is_authenticated:
            return False
        return user.role in self.allowed_roles
