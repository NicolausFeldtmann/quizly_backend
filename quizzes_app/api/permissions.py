from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):

    def has_object_permission(self, request, view, obj):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        is_owner = getattr(obj, "user", None) == user
        is_admin = user.is_superuser
        is_staff = user.is_staff

        if request.method in SAFE_METHODS:
            return is_owner or is_staff or is_admin
        return is_owner or is_admin