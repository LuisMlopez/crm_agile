from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User

from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
        list:

        >
        > **Description**
        >
        > Allow list all users.
        > Only a staff user can use this service.
        >

        create:

        >
        > **Description**
        >
        > Allow create a new user.
        > Only a staff user can use this service.
        >

        read:

        >
        > **Description**
        >
        > Read an user information using the user ID.
        > Only a staff user can use this service.
        >

        update:

        >
        > **Description**
        >
        > Update an user. The username and password fields are always required. 
        > Use the partial_update method to update an user without sendig required fields.
        > Only a staff user can use this service.
        >

        partial_update:

        >
        > **Description**
        >
        > Allow update an user information without sendig the required fields.
        > Use this service to change the user admin status.
        > Only a staff user can use this service.
        >

        delete:

        >
        > **Description**
        >
        > Allow remove an user.
        > Only a staff user can use this service.
        >
        
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]
