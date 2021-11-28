from rest_framework.viewsets import ModelViewSet, mixins, generics
from rest_framework.permissions import IsAuthenticated

from issue_tracking_system.serializers import ProjectsSerializer
from issue_tracking_system.permissions import IsAdminAuthenticated, \
    IsStaffAuthenticated, IsProjectAuthor, IsProjectContributor


class ProjectView(generics.GenericAPIView
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    '''View used to manage Project.'''

    serializer_class = ProjectsSerializer
    permission_classes = [
        IsAdminAuthenticated,
        IsStaffAuthenticated,
        IsProjectAuthor,
        IsProjectContributor]

class CreateProjectView(generics.CreateAPIView):
    '''View for creating a new project.'''

    serializer_class = ProjectsSerializer
    permission_classes = [
        IsAuthenticated]
