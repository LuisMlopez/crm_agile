import json

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from customers.models import Customer


class CustomerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = User(username='superuser', password='superuser', is_superuser=True)
        cls.superuser.save()

        cls.user = User(username='test', password='test')
        cls.user.save()

    def setUp(self):
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.user.auth_token.key)
        return super().setUp()

    def test_customer_list_service_forbbiden(self):
        # Stop including any credentials
        self.client.credentials()
        
        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, 401)

    def test_customer_list_service(self):
        # Create customers
        Customer.objects.create(
            name='Customer 1', surname='test', created_by=self.superuser, updated_by=self.superuser
        )
        Customer.objects.create(
            name='Customer 2', surname='test', created_by=self.superuser, updated_by=self.superuser
        )

        response = self.client.get('/api/customers/')
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEqual(len(content), 2)

        expected_customers = ['Customer 1', 'Customer 2']
        expected_fields = [
            'id', 'name', 'surname', 'photo', 'birthday', 'email', 'phone',
            'created_by', 'updated_by', 'created_at', 'updated_at'
        ]
        
        for customer in content:
            # Check that a customer has all expected fields
            for field in expected_fields:
                self.assertIn(field, customer)

            # Check that response customers are expected
            self.assertIn(customer.get('name'), expected_customers)
