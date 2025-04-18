from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Payment

class PaymentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_demo_payment(self):
        url = reverse("demo-payment")
        response = self.client.get(url, {'payment_for': 'subscription', 'amount': 100})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("demo_payment", response.data)
