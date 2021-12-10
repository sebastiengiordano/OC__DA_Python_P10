from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action

from django.shortcuts import get_object_or_404

from issue_tracking_system.models import Projects, Contributors
from issue_tracking_system.serializers import \
    ProjectsSerializer, ProjectsDetailSerializer, \
    ContributorsSerializer, ManageContributorSerializer
from issue_tracking_system.permissions import ProjectPermission

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer


class MultipleSerializerMixin:

    detail_serializer_class = None

    def get_serializer_class(self):
        if (
                self.action == 'retrieve'
                and self.detail_serializer_class is not None):
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectView(MultipleSerializerMixin, viewsets.ModelViewSet):
    '''Class which manage all project's actions.
    '''

    serializer_class = ProjectsSerializer
    detail_serializer_class = ProjectsDetailSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of
        permissions that this view require.

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

    @action(
        detail=False, methods=['post', 'get', 'delete'],
        url_path='(?P<project_id>[0-9]+)/users')
    def manage_contributor(self, request, project_id):
        # Add a contributor to the project
        if request.method == 'POST':
            # Validate data
            serializer = ManageContributorSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Get user by email
            user = get_object_or_404(
                CustomUser,
                email=serializer.validated_data['email'])
            # Get project by id
            project = get_object_or_404(Projects, id=project_id)
            # Check if the user has permissions
            self.check_object_permissions(request, project)
            # Create contributor
            contributor = Contributors.objects.create(
                user=user,
                project=project,
                permission='Read_Only',
                role='contributor'
                )
            return Response(ContributorsSerializer(contributor).data)

        # Get project's contributors list
        elif request.method == 'GET':
            queryset = Contributors.objects.filter(project__id=project_id)
            serializer = ContributorsSerializer(queryset, many=True)
            return Response(serializer.data)

        # Get project's contributors list
        elif request.method == 'DELETE':
            # Validate data
            serializer = ManageContributorSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Get user by email
            user = get_object_or_404(
                CustomUser,
                email=serializer.validated_data['email'])
            # Get project by id
            project = get_object_or_404(Projects, id=project_id)
            # Check if the user has permissions
            self.check_object_permissions(request, project)
            # Removed contributor of this project
            contributor = get_object_or_404(
                Contributors,
                user=user,
                project=project).delete()
            return Response(CustomUserSerializer(user).data)
