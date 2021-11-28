from rest_framework.permissions import BasePermission

from issue_tracking_system.serializers import ProjectsSerializer, ContributorsSerializer


class TestPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author_user_id == request.user


class IsAdminAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.is_superuser)


class IsStaffAuthenticated(BasePermission):

    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated
                    and request.user.is_staff)


class IsProjectAuthor(BasePermission):

    def has_permission(self, request, view):
        project = view.get_object()
        return bool(request.user
                    and request.user.is_authenticated
                    and project.author_user_id == request.user.id)


class IsProjectContributor(BasePermission):

    contributors_serializers = ContributorsSerializer

    def has_permission(self, request, view):
        return bool(request.user
                    and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects if the user is not authenticated
        if not request.user.is_authenticated():
            return False

        if view.action == 'retrieve':
            return True
