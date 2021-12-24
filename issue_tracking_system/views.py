from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.exceptions import MethodNotAllowed

from django.shortcuts import get_object_or_404

from .models import (
    Projects, Contributors, Issues, Comments)
from .serializers import (
    ProjectsSerializer, ProjectsDetailSerializer,
    ContributorsSerializer, ManageContributorSerializer,
    IssuesSerializer, IssuesDetailSerializer, IssuesUpdateSerializer,
    CommentsSerializer, CommentsUpdateSerializer)
from .permissions import (
    ProjectPermission, ObjectPermission)

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
        detail=False, methods=['post', 'get'],
        url_path='(?P<project_id>[0-9]+)/users')
    def manage_contributor(self, request, project_id):
        '''This method aims to manage contributors.'''

        # Check if the user is a project's contributor
        # and has project's permission.
        project = self.check_project_permission(request, self, project_id)

        # Add a contributor to the project
        if request.method == 'POST':
            # Validate data
            serializer = ManageContributorSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # Get user by email
            user = get_object_or_404(
                CustomUser,
                email=serializer.validated_data['email'])
            # Create contributor
            contributor = Contributors.objects.create(
                user=user,
                project=project,
                permission='Read_Only',
                role='contributor'
                )
            return Response(
                ContributorsSerializer(contributor).data,
                status=status.HTTP_200_OK,
                headers={'contributor': 'added'})

        # Get project's contributors list
        elif request.method == 'GET':
            # Get project's contributors
            queryset = Contributors.objects.filter(project__id=project_id)
            serializer = ContributorsSerializer(queryset, many=True)
            return Response(serializer.data)

    @action(
        detail=False, methods=['delete'],
        url_path='(?P<project_id>[0-9]+)/users/(?P<user_id>[0-9]+)')
    def delete_contributor(self, request, project_id, user_id):
        '''This method aims to removed a project's contributor.'''

        # Check if the user is a project's contributor
        # and has project's permission.
        project = self.check_project_permission(request, self, project_id)
        # Get user by id
        user = get_object_or_404(CustomUser, pk=user_id)
        # Removed contributor of this project
        contributor = get_object_or_404(
            Contributors,
            user=user,
            project=project)
        contributor.delete()
        return Response(
            CustomUserSerializer(user).data,
            status=status.HTTP_200_OK,
            headers={'contributor': 'removed'})

    def check_project_permission(self, request, view, project_id):
        '''This method aims to ensure that the user is a project's contributor
        and has project's permission.
        This method return the project.
        '''

        # Get project by id
        project = get_object_or_404(Projects, id=project_id)
        # Check if the user is a contributor of this project
        check_if_project_contributor(request, project)
        # If request method is not create
        if request.method not in ('POST',):
            # Check if the user has permissions
            self.check_object_permissions(request, project)
        return project


class IssueView(APIView):
    '''View which manage all issue's actions.'''

    permission_classes = (ObjectPermission,)

    def post(self, request, project_id):
        """
        Create a project's issue.
        """

        # Check if the user is a project's contributor
        self.check_issue_permission(request, self, project_id)
        # Check if request data is valid
        serializer = IssuesDetailSerializer(data=request.data)
        if serializer.is_valid():
            # Get or set assignee
            assignee = self.get_or_set_assignee(request, request.user)
            # Create the issue
            issue = Issues.objects.create(
                title=serializer.validated_data['title'],
                description=serializer.validated_data['description'],
                tag=serializer.validated_data['tag'],
                priority=serializer.validated_data['priority'],
                status=serializer.validated_data['status'],
                project=get_object_or_404(Projects, id=project_id),
                author=request.user,
                assignee=assignee)
            serializer = IssuesDetailSerializer(issue)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, issue_id=None):
        """
        Return a list or detail of project's issues.
        """

        # Check if the user is a project's contributor
        # and has issue's permission.
        self.check_issue_permission(request, self, project_id)
        # Check if a list is required
        if issue_id is None:
            # Get all issues of this project
            issues = Issues.objects.filter(project__id=project_id)
            serializer = IssuesSerializer(issues, many=True)
        # Or if its a detail request
        else:
            # Get issue by id
            issue = get_object_or_404(Issues, pk=issue_id)
            serializer = IssuesDetailSerializer(issue)
        return Response(serializer.data)

    def put(self, request, project_id, issue_id):
        """
        Update a project's issue.
        """

        # Check if the user is a project's contributor
        # and has project's permission.
        issue = self.check_issue_permission(
            request, self,
            project_id, issue_id)
        # Get the request data or keep those on the issue
        data = self.get_or_keep_issue_data(issue, request)
        # Check if request data is valid
        serializer = IssuesUpdateSerializer(data=data)
        if serializer.is_valid():
            # Udate the issue
            self.update_issue(issue, serializer.validated_data)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
                headers={'issue': 'update'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id):

        # Check if the user is a project's contributor
        # and has issue's permission.
        issue = self.check_issue_permission(
            request, self,
            project_id, issue_id)
        serializer = IssuesDetailSerializer(issue)
        issue.delete()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers={'issue': 'delete'})

    def get_or_set_assignee(self, request, assignee):
        '''This method aims to get the assignee from request,
        or, if he's not provided, return the one provided.
        '''

        email = request.data.get('assignee')
        if email is not None:
            assignee = get_object_or_404(CustomUser, email=email)
        return assignee

    def get_or_keep_issue_data(self, issue: Issues, request):
        '''This method aims to get the update value of an issue,
        or, if there are not provided, it keeps the issue value.
        '''

        data = {}
        data['title'] = request.data.get('title') or issue.title
        data['description'] = (
            request.data.get('description') or issue.description)
        data['tag'] = request.data.get('tag') or issue.tag
        data['priority'] = request.data.get('priority') or issue.priority
        data['status'] = request.data.get('status') or issue.status
        data['project'] = issue.project.id
        data['author'] = issue.author.id
        # Get or set assignee
        assignee = self.get_or_set_assignee(request, issue.assignee)
        data['assignee'] = assignee.id
        return data

    def update_issue(self, issue, validated_data):
        '''This method aims to update an issue'''

        issue.title = validated_data['title']
        issue.description = validated_data['description']
        issue.tag = validated_data['tag']
        issue.priority = validated_data['priority']
        issue.status = validated_data['status']
        issue.assignee = validated_data['assignee']
        issue.save()

    def check_issue_permission(
            self, request, view,
            project_id, issue_id=None):
        '''This method aims to ensure that the user is a project's contributor
        and has issue's permission.
        This method return the issue or None.
        '''

        # Get project by id
        project = get_object_or_404(Projects, id=project_id)
        # Check if the user is a contributor of this project
        check_if_project_contributor(request, project)
        # If its an update or detail method
        if issue_id:
            # Get issue by id
            issue = get_object_or_404(Issues, id=issue_id)
            # If request method is not create
            if request.method not in ('POST',):
                # Check if the user has permissions
                view.check_object_permissions(request, issue)
            return issue


class CommentView(APIView):
    '''View which manage all comment's actions.'''

    permission_classes = (ObjectPermission,)

    def post(self, request, project_id, issue_id):
        """
        Create a issue's comment.
        """

        # Check if the user is a project's contributor
        self.check_comment_permission(request, self, project_id)
        # Check if request data is valid
        serializer = CommentsSerializer(data=request.data)
        if serializer.is_valid():
            # Create the comment
            comment = Comments.objects.create(
                description=serializer.validated_data['description'],
                author=request.user,
                issue=get_object_or_404(Issues, id=issue_id))
            serializer = CommentsSerializer(comment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, project_id, issue_id, comment_id=None):
        """
        Return a list or detail of project's comments.
        """

        # Check if the user is a project's contributor
        # and has comment's permission.
        self.check_comment_permission(request, self, project_id, comment_id)
        # Check if a list is required
        if comment_id is None:
            # Get all comments of this issue
            comments = Comments.objects.filter(issue__id=issue_id)
            serializer = CommentsSerializer(comments, many=True)
        # Or if its a detail request
        else:
            # Get comment by id
            comment = get_object_or_404(Comments, pk=comment_id)
            serializer = CommentsSerializer(comment)
        return Response(serializer.data)

    def put(self, request, project_id, issue_id, comment_id):
        """
        Update an issue's comment.
        """

        # Check if the user is a project's contributor
        # and has project's permission.
        comment = self.check_comment_permission(
            request, self,
            project_id, comment_id)
        # Get the request data
        description = request.data.get('description')
        # Check if request data is valid
        serializer = CommentsUpdateSerializer(data=description)
        if serializer.is_valid():
            # Udate the comment
            self.update_comment(comment, serializer.validated_data)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
                headers={'comment': 'update'}
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id, comment_id):

        # Check if the user is a project's contributor
        # and has comment's permission.
        comment = self.check_comment_permission(
            request, self,
            project_id, comment_id)
        serializer = CommentsSerializer(comment)
        comment.delete()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
            headers={'comment': 'delete'})

    def update_comment(self, comment: Comments, validated_data):
        '''This method aims to update an comment'''

        comment.description = validated_data['description']
        comment.save()

    def check_comment_permission(
            self, request, view,
            project_id, comment_id=None):
        '''This method aims to ensure that the user is a project's contributor
        and has comment's permission.
        This method return the comment or None.
        '''

        # Get project by id
        project = get_object_or_404(Projects, id=project_id)
        # Check if the user is a contributor of this project
        check_if_project_contributor(request, project)
        # If its an update or detail method
        if comment_id:
            # Get comment by id
            comment = get_object_or_404(Comments, id=comment_id)
            # If request method is not create
            if request.method not in ('POST',):
                # Check if the user has permissions
                view.check_object_permissions(request, comment)
            return comment


def check_if_project_contributor(request, project):
    '''This function aims to check if the user is a project's contributor.'''

    is_contributor = Contributors.objects.filter(
        user=request.user,
        project=project)
    if not is_contributor:
        method = request.method
        raise MethodNotAllowed(
            method=method,
            detail=(
                f'Method {method} is not allowed since '
                'you\'re not a contributor of that project.'))
