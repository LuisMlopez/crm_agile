import json

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient


class UsersTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = User(username='superuser', password='superuser', is_staff=True)
        cls.superuser.save()

        cls.user = User(username='test', password='test')
        cls.user.save()

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.superuser.auth_token.key)
        return super().setUp()

    def test_create_tocket_on_create_user(self):
        user = User(username='test 2', password='test')
        user.save()

        self.assertTrue(Token.objects.filter(user=user).exists())

    def test_users_list_service_forbbiden_no_token(self):
        # Stop including any credentials
        self.client.credentials()
        
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 401)

    def test_users_list_service_forbbiden_no_staff(self):
        # Set no admin user Token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 403)

    def test_users_list_service(self):
        current_users_amount = User.objects.count()

        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEqual(len(content), current_users_amount)
