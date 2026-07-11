from rest_framework.permissions import BasePermission # type: ignore

class IsAdminUser(BasePermission):
    """
    Permiso que solo permite acceso a usuarios con rol 'admin'.
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated and request.user.role == 'admin'