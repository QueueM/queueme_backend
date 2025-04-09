from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from .models import CompanyDetailsModel

class CompanyAppAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='test', password='pass')
        CompanyDetailsModel.objects.create(user=self.user, name='TestCo')
        self.client.force_authenticate(user=self.user)

    def test_company_list_includes_ai_fields(self):
        resp = self.client.get('/companyApp/companies/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()[0]
        self.assertIn('forecast_data', data)
        self.assertIn('fraud_flag', data)
