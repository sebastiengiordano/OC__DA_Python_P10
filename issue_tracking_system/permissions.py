from rest_framework.permissions import BasePermission

from issue_tracking_system.serializers import ContributorsSerializer


class IsProjectAuthor(BasePermission):
    '''Permission for project's author.'''

    def has_permission(self, request, view):
        # This permissions only allow the project's author
        project = view.get_object()
        return bool(request.user
                    and request.user.is_authenticated
                    and project.author_user_id == request.user.id)


class IsProjectContributor(BasePermission):
    '''Permission for project's contributor.'''

    def has_permission(self, request, view):
        project = view.get_object()
        contributors = project.project_contributor.all()
        serializer = ContributorsSerializer(contributors, many=True)
        if view.action == 'list' or view.action == 'retrieve':
            return bool(request.user
                        and request.user.is_authenticated
                        and request.user.id in serializer.data['user_id'])
        else:
            return False

    def has_object_permission(self, request, view, obj):
        # Deny actions on project since this user is a contributor
        # not the author.
        return False
