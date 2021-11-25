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

    def test_user_create_service_forbidden_no_token(self):
        # Stop including any credentials
        self.client.credentials()

        payload = {
            'username': 'Pepe',
            'password': '12345'
        }
        
        response = self.client.post('/api/users/', payload, format='json')
        self.assertEqual(response.status_code, 401)

    def test_user_create_service_forbidden_no_staff(self):
        # Set no admin user Token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)

        payload = {
            'username': 'Pepe',
            'password': '12345'
        }
        
        response = self.client.post('/api/users/', payload, format='json')
        self.assertEqual(response.status_code, 403)

    def test_user_create_service(self):
        payload = {
            'username': 'Pepe',
            'password': '12345'
        }

        self.assertFalse(User.objects.filter(username=payload.get('username')).exists())
        
        response = self.client.post('/api/users/', payload, format='json')
        self.assertEqual(response.status_code, 201)

        self.assertTrue(User.objects.filter(username=payload.get('username')).exists())

    def test_user_update_service_forbidden_no_token(self):
        # Stop including any credentials
        self.client.credentials()

        payload = {
            'is_staff': True
        }
        
        response = self.client.put('/api/users/{}/'.format(self.user.id), payload, format='json')
        self.assertEqual(response.status_code, 401)

    def test_user_update_service_forbidden_no_staff(self):
        # Set no admin user Token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)

        payload = {
            'is_staff': True
        }
        
        response = self.client.put('/api/users/{}/'.format(self.user.id), payload, format='json')
        self.assertEqual(response.status_code, 403)

    def test_user_update_service(self):
        payload = {
            'username': self.user.username,
            'password': '1234',
            'is_staff': True
        }

        self.assertFalse(self.user.is_staff)
        
        response = self.client.put('/api/users/{}/'.format(self.user.id), payload, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertTrue(User.objects.get(id=self.user.id).is_staff)

    def test_user_partial_update_service_forbidden_no_token(self):
        # Stop including any credentials
        self.client.credentials()

        payload = {
            'is_staff': True
        }
        
        response = self.client.patch('/api/users/{}/'.format(self.user.id), payload, format='json')
        self.assertEqual(response.status_code, 401)

    def test_user_partial_update_service_forbidden_no_staff(self):
        # Set no admin user Token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)

        payload = {
            'is_staff': True
        }
        
        response = self.client.patch('/api/users/{}/'.format(self.user.id), payload, format='json')
        self.assertEqual(response.status_code, 403)

    def test_user_partial_update_service(self):
        payload = {
            'is_staff': True
        }

        self.assertFalse(self.user.is_staff)
        
        response = self.client.patch('/api/users/{}/'.format(self.user.id), payload, format='json')
        self.assertEqual(response.status_code, 200)

        self.assertTrue(User.objects.get(id=self.user.id).is_staff)

    def test_user_delete_service_forbidden_no_token(self):
        # Stop including any credentials
        self.client.credentials()
        
        response = self.client.delete('/api/users/{}/'.format(self.user.id))
        self.assertEqual(response.status_code, 401)

    def test_user_delete_service_forbidden_no_staff(self):
        # Set no admin user Token
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        
        response = self.client.delete('/api/users/{}/'.format(self.user.id))
        self.assertEqual(response.status_code, 403)

    def test_user_delete_service(self):      
        response = self.client.delete('/api/users/{}/'.format(self.user.id))
        self.assertEqual(response.status_code, 204)

        self.assertFalse(User.objects.filter(id=self.user.id).exists())
        self.assertFalse(Token.objects.filter(user_id=self.user.id).exists())

    def test_users_list_service_forbbiden_user_inactive(self):
        # Inactivate superuser
        self.superuser.is_active = False
        self.superuser.save()
        
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, 401)
