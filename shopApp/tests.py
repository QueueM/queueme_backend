# shopApp/tests.py
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()

class ShopAppAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='shoptest', password='testpass')
        self.client.force_authenticate(user=self.user)

    def test_shop_list_api(self):
        response = self.client.get('/shopApp/shops/')
        self.assertEqual(response.status_code, 200)
