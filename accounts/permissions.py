from rest_framework import permissions


class IsClient(permissions.BasePermission):
    """Allows access only to users with CLIENT role."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'CLIENT'
        )


class IsFreelancer(permissions.BasePermission):
    """Allows access only to users with FREELANCER role."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'FREELANCER'
        )


class IsAdminRole(permissions.BasePermission):
    """Allows access only to users with ADMIN role."""

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.role == 'ADMIN'
        )


class IsOwnerOrAdmin(permissions.BasePermission):
    """Allows access to the object owner or admin users."""

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'ADMIN':
            return True
        # Check for 'user' attribute first, then check if obj IS a user
        if hasattr(obj, 'user'):
            return obj.user == request.user
        return obj == request.user
