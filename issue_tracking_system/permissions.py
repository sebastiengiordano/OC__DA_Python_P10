from rest_framework.permissions import BasePermission

from issue_tracking_system.serializers import ProjectsSerializer, ContributorsSerializer


class IsProjectAuthor(BasePermission):

    def has_permission(self, request, view):
        # This permissions only allow the project's author
        project = view.get_object()
        return bool(request.user
                    and request.user.is_authenticated
                    and project.author_user_id == request.user.id)

    def has_object_permission(self, request, view, obj):
        # As this permissions is checked after the has_permission method,
        # since the project's author is already identified,
        # this method could allow action on this object.
        return True
        # return obj.author_user_id == request.user.id


class IsProjectContributor(BasePermission):

    contributors_serializers = ContributorsSerializer

    def has_permission(self, request, view):
        if view.action == 'list' or view.action == 'retrieve':
            return bool(request.user
                        and request.user.is_authenticated)
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on objects since this user is a contributor
        # not the author.
        return False