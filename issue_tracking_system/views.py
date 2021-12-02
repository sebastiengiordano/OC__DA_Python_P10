from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from issue_tracking_system.serializers import ProjectsSerializer
from accounts.permissions import IsAdminAuthenticated
from issue_tracking_system.permissions import \
    IsProjectAuthor, IsProjectContributor


class ProjectView(viewsets.ModelViewSet):
    '''Class which manage all project's actions.
    '''

    serializer_class = ProjectsSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        
        All authentified persons can create a project.
        Project's author can used all others actions.
        Project's contributor have only read permissions.
        """
        if self.action == 'create':
            permission_classes = [IsAuthenticated]
        elif self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsProjectAuthor, IsProjectContributor, IsAdminAuthenticated]
        else:
            permission_classes = [IsProjectAuthor, IsAdminAuthenticated]
        return [permission() for permission in permission_classes]
