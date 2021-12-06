from rest_framework import routers
from django.urls import path, include

from rest_framework import routers

from issue_tracking_system.views import ProjectView


router = routers.SimpleRouter()
router.register('projects', ProjectView, basename='projects')

app_name = 'issue_tracking_system'

urlpatterns = [
    path('', include(router.urls)),
]
