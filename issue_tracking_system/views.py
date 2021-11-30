from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response

from issue_tracking_system.serializers import ProjectsSerializer
from issue_tracking_system.permissions import IsAdminAuthenticated, \
    IsStaffAuthenticated, IsProjectAuthor, IsProjectContributor


class GetProjectView(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin):
    '''View used to display all projects or to see project detail.'''

    serializer_class = ProjectsSerializer
    permission_classes = [
        IsAdminAuthenticated,
        IsStaffAuthenticated,
        IsProjectAuthor,
        IsProjectContributor]


class SetProjectView(viewsets.GenericViewSet,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
    '''View used to update or delete Project.'''

    serializer_class = ProjectsSerializer
    permission_classes = [
        IsAdminAuthenticated,
        IsStaffAuthenticated,
        IsProjectAuthor]


class CreateProjectView(viewsets.GenericViewSet,
                     mixins.CreateModelMixin):
    '''View for creating a new project.'''

    serializer_class = ProjectsSerializer
    permission_classes = [
        IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
