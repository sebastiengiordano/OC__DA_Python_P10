from rest_framework import routers
from django.urls import path, include

from rest_framework import routers

from .views import ProjectView, IssueView


router = routers.SimpleRouter()
router.register('projects', ProjectView, basename='projects')

app_name = 'issue_tracking_system'

urlpatterns = [
    path('', include(router.urls)),
    path(
        'projects/<int:project_id>/issues/',
        IssueView.as_view(),
        name='issue_create_list'),
    path(
        'projects/<int:project_id>/issues/<int:issue_id>/',
        IssueView.as_view(),
        name='issue_update_detail'),
]
