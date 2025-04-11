from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from companyApp.models import CompanyDetailsModel

class CompanyAppAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user for the company.
        self.user = User.objects.create_user(username='test', password='pass')
        # Create a company record associated with the user.
        CompanyDetailsModel.objects.create(
            user=self.user,
            name='TestCo'
        )
        self.client.force_authenticate(user=self.user)

    def test_company_list_includes_ai_fields(self):
        # Reverse lookup for companies list; adjust if your router's name is different.
        url = reverse('companyApp:companies-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        json_data = resp.json()
        # Check pagination structure: results might be under "results".
        results = json_data.get("results", json_data)
        self.assertTrue(len(results) > 0, "No companies found in the response.")
        data = results[0]
        self.assertIn('forecast_data', data, "Forecast data field missing.")
        self.assertIn('fraud_flag', data, "Fraud flag field missing.")
