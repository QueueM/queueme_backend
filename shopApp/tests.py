from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from shopApp.models import ShopDetailsModel
from companyApp.models import CompanyDetailsModel

class ShopAppAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        # Create a user
        self.user = User.objects.create_user(username='shoptest', password='testpass')
        # Create a valid company for the shop.
        self.company = CompanyDetailsModel.objects.create(
            user=self.user,
            name='Test Company'
        )
        # Create a sample shop with valid company and user.
        ShopDetailsModel.objects.create(
            owner=self.user,
            company=self.company,
            name='TestShop',
            shop_name='Test Shop'
        )
        self.client.force_authenticate(user=self.user)

    def test_shop_list_api(self):
        # Reverse lookup for the endpoint. Adjust the name if your router uses a different name.
        url = reverse('shopApp:shops-list')
        resp = self.client.get(url)
        self.assertEqual(resp.status_code, 200)
        json_data = resp.json()
        # If using DRF pagination, the results are under "results"
        results = json_data.get("results", json_data)
        self.assertTrue(len(results) > 0, "No shops found.")
        data = results[0]
        self.assertIn('ai_recommendations', data, "AI recommendations field missing.")
        self.assertIn('ai_personalization', data, "AI personalization field missing.")
