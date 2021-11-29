from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import AllowAny

from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from accounts.permissions import IsAdminAuthenticated

# class ConnectionView(ModelViewSet):
#     '''View used to manage user's log in.'''

#     serializer_class = CustomUserSerializer

#     email = request.POST['email']
#     password = request.POST['password']
#     user = authenticate(request, email=email, password=password)
#     if user is not None:
#         login(request, user)
#         # Redirect to a success page.
#         ...
#     else:
#         # Return an 'invalid login' error message.
#         ...


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = CustomUserSerializer


# class UserListView(viewsets.ReadOnlyModelViewSet):
class UserListView(generics.ListAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAdminAuthenticated,)
    serializer_class = CustomUserSerializer


class UserManagementView(viewsets.GenericViewSet,
                         mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin,
                         mixins.DestroyModelMixin):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAdminAuthenticated,)
    serializer_class = CustomUserSerializer


class UserDetailView(generics.RetrieveAPIView):
    queryset = CustomUser.objects.all()
    permission_classes = (IsAdminAuthenticated,)
    serializer_class = CustomUserSerializer
