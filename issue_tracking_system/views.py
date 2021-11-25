from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet

from issue_tracking_system.serializers import ProjectsSerializer

class ProjectView(ModelViewSet):
    '''View used to manage Project.'''
    
    serializer_class = ProjectsSerializer
