from rest_framework import viewsets
from rest_framework.serializers import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404

from issue_tracking_system.models import Projects, Contributors
from issue_tracking_system.serializers import ProjectsSerializer, ProjectsDetailSerializer
from issue_tracking_system.permissions import ProjectPermission

from accounts.models import CustomUser


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if self.action == 'retrieve' and self.detail_serializer_class is not None:
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectView(MultipleSerializerMixin, viewsets.ModelViewSet):
    '''Class which manage all project's actions.
    '''

    serializer_class = ProjectsSerializer
    detail_serializer_class = ProjectsDetailSerializer

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
        # Return user's projects
        queryset = Contributors.objects.filter(user=user)
        projects_id = [query.project.id for query in queryset]
        return Projects.objects.filter(pk__in=projects_id)

    @action(detail=True, methods=['post'], url_path='<int:project_id>/users/')
    def add_contributor(self, request, project_id):
        # Check if email field is valid
        user_email = request.data.get('email')
        if user_email is None or user_email == "":
            raise ValidationError(
                {'email': ['This field may not be blank.']})
        # Get user by email
        user = get_object_or_404(CustomUser, email=user_email)
        # Get project by id
        project = get_object_or_404(Projects, id=project_id)
        # Create contributor
        self.get_object().add_contributor(user, project)
        return Response()