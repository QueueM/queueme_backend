from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from companyApp.models import CompanyDetailsModel
from subscriptionApp.models import CompanySubscriptionPlansModel, CompanySubscriptionDetailsModel

class SubscriptionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='password')
        self.company = CompanyDetailsModel.objects.create(name="Test Company", user=self.user)
        self.user.company = self.company
        self.user.save()
        self.plan = CompanySubscriptionPlansModel.objects.create(
            name="Basic Plan",
            description="A basic subscription plan.",
            price=100,
            duration_days=30,
            yearly_duration_days=365,
            yearly_price=1000
        )
        self.client.force_authenticate(user=self.user)

    def test_create_subscription(self):
        url = reverse("company-plans-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_payment_creation_and_subscription_update(self):
        url = reverse("subscription-initiate-payment")
        data = {
            "plan": str(self.plan.pk),
            "amount": "100.00",
            "billing_cycle": "monthly",
            "source": {
                "name": "Test User",
                "number": "4111111111111111",
                "cvc": "123",
                "month": 12,
                "year": 2029
            }
        }
        response = self.client.post(url, data, format='json')
        self.assertIn(response.status_code, [200, 201])
