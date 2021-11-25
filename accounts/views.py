from django.shortcuts import render
from django.contrib.auth import authenticate, login
from rest_framework import generics
from rest_framework.viewsets import ModelViewSet

from accounts.models import CustomUser
from accounts.serializers import RegistrationSerializer

# class ConnectionView(ModelViewSet):
#     '''View used to manage user's log in.'''
    
#     serializer_class = RegistrationSerializer
    
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
    # permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer


# def signup(request):
#     '''View used to manage user's registration.'''
#     email = request.POST['email']
#     first_name = request.POST['first_name']
#     last_name = request.POST['last_name']
#     password = request.POST['password']
#     password_check = request.POST['password_check']
