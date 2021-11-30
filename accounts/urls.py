from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import RegisterView, GetUserView, SetUserView

router = routers.SimpleRouter()
router.register('user', GetUserView, basename='user')
router.register('user', SetUserView, basename='user')

app_name = 'accounts'
urlpatterns = [
    # For login/logout route
    # path('', include('rest_framework.urls')),
    # For JWT tokens management
    path('token/obtain/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # For register a new CustomUser
    path('signup/', RegisterView.as_view(), name='register'),
    # For managed all CustomUsers (action: list, retrieve, update, destroy)
    path('', include(router.urls)),
]
