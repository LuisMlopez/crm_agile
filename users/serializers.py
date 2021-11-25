from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'is_staff',
            'date_joined'
        ]
        read_only_fields = ['date_joined']
