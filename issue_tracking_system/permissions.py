from rest_framework.permissions import BasePermission


class TestPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated
    def has_object_permission(self, request, view, obj):
        return obj.author_user_id == request.user