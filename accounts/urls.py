from django.urls import path, include

from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from accounts.views import RegisterView, UserView

router = routers.SimpleRouter()
router.register('user', UserView, basename='user')

app_name = 'accounts'
urlpatterns = [
    # For JWT tokens management
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # For register a new CustomUser
    path('signup/', RegisterView.as_view(), name='register'),
    # For managed all CustomUsers (action: list, retrieve, update, destroy)
    path('', include(router.urls)),
]
