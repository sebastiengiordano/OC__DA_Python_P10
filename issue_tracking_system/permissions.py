from rest_framework.permissions import BasePermission, SAFE_METHODS


class ProjectPermission(BasePermission):
    '''Permission for projects.'''

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Admin has all permissions
        if request.user.is_admin:
            return True

        # Author has all permissions
        if obj.author == request.user:
            return True

        # Contributors could only has read action
        if request.method in SAFE_METHODS:
            return True

        return False


class ObjectPermission(BasePermission):
    '''Permission for issues.'''

    def has_permission(self, request, view):
        return bool(request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Admin has all permissions
        if request.user.is_admin:
            return True

        # Author has all permissions
        if obj.author == request.user:
            return True

        # Contributors could only has read action
        if request.method in SAFE_METHODS:
            return True

        return False
