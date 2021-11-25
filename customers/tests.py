import json

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient

from customers.models import Customer


class CustomerTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.superuser = User(username='superuser', password='superuser', is_staff=True)
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

    def test_customer_create_service_forbidden(self):
        # Stop including any credentials
        self.client.credentials()

        payload = {
            'name': 'Pepe',
            'surname': 'Flores'
        }
        
        response = self.client.post('/api/customers/', payload, format='json')
        self.assertEqual(response.status_code, 401)

    def test_customer_create_service(self):
        payload = {
            'name': 'Pepe',
            'surname': 'Flores'
        }

        self.assertFalse(Customer.objects.filter(name=payload.get('name')).exists())
        
        response = self.client.post('/api/customers/', payload, format='json')
        self.assertEqual(response.status_code, 201)

        self.assertTrue(Customer.objects.filter(name=payload.get('name')).exists())

        customer = Customer.objects.get(name=payload.get('name'))

        self.assertEqual(customer.created_by, self.user)
        self.assertEqual(customer.updated_by, self.user)

    def test_customer_update_service_forbidden(self):
        # Stop including any credentials
        self.client.credentials()

        customer = Customer(
            name='Customer 1', surname='test', created_by=self.superuser, updated_by=self.superuser
        )
        customer.save()

        current_name = customer.name

        payload = {
            'name': 'Pepe',
            'surname': 'Flores'
        }
        
        response = self.client.put('/api/customers/{}/'.format(customer.id), payload, format='json')
        self.assertEqual(response.status_code, 401)

        customer.refresh_from_db()

        self.assertEqual(customer.name, current_name)

    def test_customer_update_service(self):
        customer = Customer(
            name='Customer 1', surname='test', created_by=self.superuser, updated_by=self.superuser
        )
        customer.save()

        self.assertEqual(customer.updated_by, self.superuser)

        current_name = customer.name

        payload = {
            'name': 'Pepe',
            'surname': 'Flores'
        }
        
        response = self.client.put('/api/customers/{}/'.format(customer.id), payload, format='json')
        self.assertEqual(response.status_code, 200)

        customer.refresh_from_db()

        # Check that user who create has not changed
        self.assertEqual(customer.created_by, self.superuser)
        # Check that user who update has changed
        self.assertEqual(customer.updated_by, self.user)
        # Check that customer name has changed
        self.assertEqual(customer.name, payload.get('name'))
        self.assertNotEqual(customer.name, current_name)

    def test_get_customer_information_service_forbidden(self):
        # Stop including any credentials
        self.client.credentials()

        customer = Customer(
            name='Customer 1', surname='test', created_by=self.superuser, updated_by=self.superuser
        )
        customer.save()
        
        response = self.client.get('/api/customers/{}/'.format(customer.id))
        self.assertEqual(response.status_code, 401)

    def test_get_customer_information_service(self):
        customer = Customer(
            name='Customer 1', surname='test', created_by=self.superuser, updated_by=self.superuser
        )
        customer.save()
        
        response = self.client.get('/api/customers/{}/'.format(customer.id))
        self.assertEqual(response.status_code, 200)

        content = json.loads(response.content)
        self.assertEqual(content.get('name'), customer.name)

    def test_delete_customer_service_forbidden(self):
        # Stop including any credentials
        self.client.credentials()

        customer = Customer(
            name='Customer 1', surname='test', created_by=self.superuser, updated_by=self.superuser
        )
        customer.save()
        
        response = self.client.delete('/api/customers/{}/'.format(customer.id))
        self.assertEqual(response.status_code, 401)

        self.assertTrue(Customer.objects.filter(id=customer.id).exists())

    def test_delete_customer_service(self):
        customer = Customer(
            name='Customer 1', surname='test', created_by=self.superuser, updated_by=self.superuser
        )
        customer.save()
        
        response = self.client.delete('/api/customers/{}/'.format(customer.id))
        self.assertEqual(response.status_code, 204)

        self.assertFalse(Customer.objects.filter(id=customer.id).exists())
