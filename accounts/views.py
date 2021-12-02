from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from accounts.models import CustomUser
from accounts.serializers import \
    CustomUserSerializer, CreateCustomUserSerializer
from accounts.permissions import IsAdminAuthenticated


class RegisterView(generics.CreateAPIView):
    '''Class which manage the create action.'''

    queryset = CustomUser.objects.all()
    permission_classes = (IsAdminAuthenticated,)
    serializer_class = CreateCustomUserSerializer


class UserView(viewsets.GenericViewSet,
                mixins.ListModelMixin,
                mixins.RetrieveModelMixin,
                mixins.UpdateModelMixin,
                mixins.DestroyModelMixin):
    '''Class which manage the
    list, retrieve, update and destroy actions.
    '''
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminAuthenticated]
        return [permission() for permission in permission_classes]
