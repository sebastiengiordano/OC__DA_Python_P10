from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from rest_framework.decorators import action

from issue_tracking_system.models import Projects, Contributors
from issue_tracking_system.serializers import ProjectsSerializer
from issue_tracking_system.permissions import ProjectPermission


class ProjectView(viewsets.ModelViewSet):
    '''Class which manage all project's actions.
    '''

    serializer_class = ProjectsSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view require.

        All authentified persons can create a project.
        Project's author can used all others actions.
        Project's contributors have only read permissions.
        Admin has all permissions.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [ProjectPermission]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        # Get the current user
        user = self.request.user
        # Retrun user's projects
        queryset = Contributors.objects.filter(user=user)
        projects_id = [query.id for query in queryset]
        return Projects.objects.filter(pk__in=projects_id)

    # @action(detail=True, methods=['post'])
    # def disable(self, request, pk):
    #     self.get_object().disable()
    #     return Response()