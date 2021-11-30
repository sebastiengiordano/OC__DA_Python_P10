from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from accounts.permissions import IsAdminAuthenticated


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAdminAuthenticated,)
    serializer_class = CustomUserSerializer


class GetUserView(viewsets.GenericViewSet,
                  mixins.ListModelMixin,
                  mixins.RetrieveModelMixin):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = CustomUserSerializer


class SetUserView(viewsets.GenericViewSet,
                  mixins.UpdateModelMixin,
                  mixins.DestroyModelMixin):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAdminAuthenticated,)
    serializer_class = CustomUserSerializer
