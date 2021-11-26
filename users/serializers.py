from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    token = serializers.CharField(source='auth_token.key', read_only=True)
    class Meta:
        model = User
        fields = [
            'id', 'username', 'first_name', 'last_name', 'email', 'password', 'is_active', 'is_staff',
            'date_joined', 'token'
        ]
        read_only_fields = ['date_joined', 'token']
        extra_kwargs = {
            'password': {'write_only': True}
        }
