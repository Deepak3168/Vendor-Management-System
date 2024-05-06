from django.test import TestCase

# Create your tests here.
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from .models import UserData

class AuthenticationTest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_registration(self):
        url = reverse('sign_up')
        data = {
            'name': 'testuser',
            'email': 'test@example.com',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.access_token = response.data.get('access')
        def test_login(self):
            response = self.client.post(self.login_url, {
                'email': 'test@example.com',
                'password': 'testpassword123'
            }, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.refresh_token = response.data.get('refresh')
            self.assertIn('access', response.data)
            self.assertIn('refresh', response.data)
            def test_logout(self):
                logout_url = reverse('auth_logout')
                refresh_token =self.refresh_token
                response = self.client.post(logout_url, {"refresh_token": refresh_token}, format='json')
                self.assertEqual(response.status_code, status.HTTP_205_RESET_CONTENT)




