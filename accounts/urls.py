from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts import views

router = routers.SimpleRouter()
router.register('user', views.UserManagementView, basename='user')

app_name = 'accounts'
urlpatterns = [
    # For login/logout route
    path('', include('rest_framework.urls')),
    # For JWT tokens management
    path('token/obtain/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # For register a new CustomUser
    path('signup/', views.RegisterView.as_view(), name='register'),
    # For get all users list
    # path('user/', views.UserListView.as_view(), name='user'),
    # path('user/{<int>pk}/', views.UserDetailView.as_view(), name='user'),
    # path('user/', views.UserListView.as_view({'get': 'list'}), name='user'),
    path('', include(router.urls)),
]
