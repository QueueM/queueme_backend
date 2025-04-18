from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from shopApp.models import ShopDetailsModel
from adsApp.models import ShopAdsModel
from companyApp.models import CompanyDetailsModel

class AdsAppTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='adtester', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.company = CompanyDetailsModel.objects.create(name="Test Company", user=self.user)
        self.shop = ShopDetailsModel.objects.create(
            name="Test Shop",
            credits=10,
            company=self.company,
            owner=self.user
        )
        self.ad = ShopAdsModel.objects.create(
            shop=self.shop,
            title="Test Ad",
            description="A test ad.",
            budget=100,
            end_date="2030-01-01T00:00:00Z",
            target_gender="both"
        )

    def test_fetch_ad(self):
        url = reverse("shopadsmodel-fetch-ad")
        response = self.client.get(url, {"latitude": "10.0", "longitude": "10.0"})
        self.assertEqual(response.status_code, 200)
