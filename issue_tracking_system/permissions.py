from rest_framework.permissions import BasePermission

from issue_tracking_system.serializers import ProjectsSerializer, ContributorsSerializer


class IsProjectAuthor(BasePermission):
    '''Permission fro project's author.'''

    def has_permission(self, request, view):
        # This permissions only allow the project's author
        project = view.get_object()
        return bool(request.user
                    and request.user.is_authenticated
                    and project.author_user_id == request.user.id)



class IsProjectContributor(BasePermission):

    def has_permission(self, request, view):
        if view.action == 'list' or view.action == 'retrieve':
            return bool(request.user
                        and request.user.is_authenticated)
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on project since this user is a contributor
        # not the author.
        return False