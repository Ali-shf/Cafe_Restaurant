from rest_framework.permissions import BasePermission

class IsOwnerOrAdmin(BasePermission):
    """
    Allow access only to staff/superuser users.
    """

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.is_staff or request.user.is_superuser)
        )
