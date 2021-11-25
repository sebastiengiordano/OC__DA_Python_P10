from django.urls import path

from . import views


app_name = 'issue_tracking_system'
urlpatterns = [
    # path('signup/', views.signup, name='signup'),
    path('issue_tracking_system/', views.ProjectView, name='login'),
]