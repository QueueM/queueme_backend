from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from companyApp.models import CompanyDetailsModel
from shopApp.models import ShopDetailsModel
from storiesApp.models import StoryModel

class StoriesAppTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.company = CompanyDetailsModel.objects.create(user=self.user, name="Test Company")
        self.shop = ShopDetailsModel.objects.create(owner=self.user, company=self.company, shop_name="Test Shop", name="Test Shop")
        self.story = StoryModel.objects.create(shop=self.shop, caption="Test Story")

    def test_active_stories(self):
        url = reverse('storiesApp:active_stories')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_mark_story_viewed(self):
        url = reverse('storiesApp:mark_viewed', args=[self.story.pk])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.story.refresh_from_db()
        self.assertGreaterEqual(self.story.view_count, 1)
