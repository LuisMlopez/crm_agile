from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class BaseTests(TestCase):
    def test_create_tocket_on_create_user(self):
        user = User(username='test', password='test')
        user.save()

        self.assertTrue(Token.objects.filter(user=user).exists())


