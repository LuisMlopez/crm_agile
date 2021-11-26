from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User

from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
        A ViewSet for viewing, creating and editing users.
        Only a staff user can use this services.

        list:

        >
        > **Description**
        >
        > Allow list all users
        >

        create:

        >
        > **Description**
        >
        > Allow create a new user.
        >

        read:

        >
        > **Description**
        >
        > Read an user information using the user ID.
        >

        update:

        >
        > **Description**
        >
        > Update an user. The username and password fields are always required. 
        > Use the partial_update method to update an user without sendig required fields.
        >

        partial_update:

        >
        > **Description**
        >
        > Allow update an user information without sendig the required fields.
        > Use this service to change the user admin status.
        >

        delete:

        >
        > **Description**
        >
        > Allow remove an user.
        >
        
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
