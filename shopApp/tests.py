from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from shopApp.models import ShopDetailsModel
from companyApp.models import CompanyDetailsModel

class ShopAppAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='shoptest', password='testpass')
        self.company = CompanyDetailsModel.objects.create(user=self.user, name='Test Company')
        ShopDetailsModel.objects.create(
            owner=self.user,
            company=self.company,
            name='TestShop',
            shop_name='Test Shop'
        )
        self.client.force_authenticate(user=self.user)

    def test_shop_list_api(self):
        url = reverse('shopApp:shops-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        json_data = resp.json()
        results = json_data.get("results", json_data)
        self.assertTrue(len(results) > 0, "No shops found.")
        data = results[0]
        self.assertIn('ai_recommendations', data, "AI recommendations field missing.")
        self.assertIn('ai_personalization', data, "AI personalization field missing.")
