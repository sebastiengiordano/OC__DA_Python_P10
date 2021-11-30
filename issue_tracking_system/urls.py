from rest_framework import routers
from django.urls import path, include

from rest_framework import routers

from issue_tracking_system.views import \
    GetProjectView, SetProjectView, CreateProjectView


router = routers.SimpleRouter()
router.register('projects', GetProjectView, basename='get_projects')
router.register('projects', SetProjectView, basename='set_projects')
router.register('projects', CreateProjectView, basename='create_projects')


app_name = 'issue_tracking_system'
urlpatterns = [
    path('', include(router.urls)),
]
