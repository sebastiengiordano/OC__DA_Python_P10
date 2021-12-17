from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.exceptions import MethodNotAllowed

from django.shortcuts import get_object_or_404

from .models import (
    Projects, Contributors, Issues)
from .serializers import (
    ProjectsSerializer, ProjectsDetailSerializer,
    ContributorsSerializer, ManageContributorSerializer,
    IssuesSerializer, IssuesDetailSerializer)
from .permissions import (
    ProjectPermission, IssuePermission)

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer


class MultipleSerializerMixin:
    '''Class used to set serializer according to action.'''

    detail_serializer_class = None

    def get_serializer_class(self):
        if (
                self.action == 'retrieve'
                and self.detail_serializer_class is not None):
            return self.detail_serializer_class
        return super().get_serializer_class()


class ProjectView(MultipleSerializerMixin, viewsets.ModelViewSet):
    '''View which manage all project's actions.'''

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
            permission_classes = (IsAuthenticated,)
        else:
            permission_classes = (ProjectPermission,)
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


class IssueView(APIView):
    '''View which manage all issue's actions.'''

    permission_classes = (IssuePermission,)

    def post(self, request, project_id):
        """
        Create a project's issue.
        """
        # Get project by id
        project = get_object_or_404(Projects, id=project_id)
        # Check if the user is a contributor of this project
        self.check_if_project_contributor(request, project)
        # Check if request data is valid
        serializer = IssuesDetailSerializer(data=request.data)
        if serializer.is_valid():
            # Get or set assignee
            email = request.data.get('assignee')
            if email is None:
                assignee = request.user
            else:
                assignee = get_object_or_404(CustomUser, email=email)
            # Create the issue
            issue = Issues.objects.create(
                title=serializer.validated_data['title'],
                description=serializer.validated_data['description'],
                tag=serializer.validated_data['tag'],
                priority=serializer.validated_data['priority'],
                status=serializer.validated_data['status'],
                project=project,
                author=request.user,
                assignee=assignee
            )
            serializer = IssuesDetailSerializer(issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, issue_id=None):
        """
        Return a list or detail of project's issues.
        """

        # Get project by id
        project = get_object_or_404(Projects, id=project_id)
        # Check if the user is a contributor of this project
        self.check_if_project_contributor(request, project)
        # Check if a list is required
        if issue_id is None:
            # Get all issue of this project
            issues = Issues.objects.filter(project=project)
            serializer = IssuesSerializer(issues, many=True)
        # Or if its a detail request
        else:
            # Get issue by id
            issue = get_object_or_404(Issues, pk=issue_id)
            serializer = IssuesDetailSerializer(issue)
        return Response(serializer.data)

    def check_if_project_contributor(self, request, project):
        is_contributor = Contributors.objects.filter(
            user=request.user,
            project=project)
        if not is_contributor:
            raise MethodNotAllowed(
                f'{request.method} is not allowed since you\'re'
                ' not a contributor of that project.')
