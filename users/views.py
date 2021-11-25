from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User

from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
        A ViewSet for viewing, creating and editing users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
