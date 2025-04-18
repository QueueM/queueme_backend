from django.test import TestCase, override_settings
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from shopApp.models import ShopDetailsModel
from companyApp.models import CompanyDetailsModel
from reelsApp.models import ReelsModel, CommentsModel
import tempfile

class ReelsAppTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.company = CompanyDetailsModel.objects.create(user=self.user, name="Test Company")
        self.shop = ShopDetailsModel.objects.create(owner=self.user, company=self.company, name="Test Shop", shop_name="Test Shop")
        self.reel = ReelsModel.objects.create(
            shop=self.shop,
            video=tempfile.NamedTemporaryFile(suffix=".mp4").name,
            caption="Test reel caption"
        )

    def test_reel_like(self):
        url = reverse('reels-like', args=[self.reel.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reel_increment_view(self):
        url = reverse('reels-increment-view', args=[self.reel.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
