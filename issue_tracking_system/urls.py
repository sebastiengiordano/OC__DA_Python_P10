from rest_framework import routers
from django.urls import path, include

from issue_tracking_system.views import ProjectView


router = routers.SimpleRouter()


app_name = 'issue_tracking_system'
urlpatterns = [
    # path('signup/', views.signup, name='signup'),
    path('projects/', ProjectView, name='login'),
]
