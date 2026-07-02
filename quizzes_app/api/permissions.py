from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):
    """Custom permission class to grant dedicated rigths."""

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        is_owner = getattr(obj, "user", None)  == user

        is_admin = user.is_superuser
        is_staff = user.is_staff
        return is_owner or is_admin