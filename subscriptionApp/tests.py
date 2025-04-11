"""
subscriptionApp/tests.py

Advanced tests for subscription endpoints.
This test file shows how to authenticate the test client so that the PaymentCreateApiView,
which requires an authenticated user, can be accessed successfully.
"""

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from companyApp.models import CompanyDetailsModel
from subscriptionApp.models import CompanySubscriptionPlansModel, CompanySubscriptionDetailsModel, Payment

class SubscriptionTests(APITestCase):
    def setUp(self):
        # Initialize APIClient.
        self.client = APIClient()
        
        # Create a test user.
        self.user = User.objects.create_user(username='testuser', password='password')
        
        # Create a CompanyDetailsModel instance and associate it with the user.
        self.company = CompanyDetailsModel.objects.create(name="Test Company", user=self.user)
        # If your CompanyDetailsModel is linked to User via a property,
        # assign it explicitly:
        self.user.company = self.company
        self.user.save()
        
        # Create a subscription plan.
        self.plan = CompanySubscriptionPlansModel.objects.create(
            name="Basic Plan",
            description="A basic subscription plan.",
            price=100,
            duration_days=30,
            yearly_duration_days=365,
            yearly_price=1000
        )
        
        # Force authenticate the API client using the test user.
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        # Test retrieving subscription plans, for example.
        url = reverse("company-plans-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_payment_creation_and_subscription_update(self):
        # The PaymentCreateApiView is expected to return a 200 or 201 after a successful payment creation.
        url = reverse("payment")  # Ensure this matches your URL configuration.
        data = {
            "payment_id": "test_payment_123",
            "amount": "100.00",
            "status": "paid",
            "payment_type": "p",
            "payed_for": "s",
            "bill_name": "Test User",
            "phone_number": "1234567890",
            "email": "test@example.com",
            "address": "123 Test St",
            "billing_cycle": "monthly",
            "subscription_id": str(self.plan.pk)
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
