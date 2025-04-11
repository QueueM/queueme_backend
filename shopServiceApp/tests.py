# shopServiceApp/tests.py
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from companyApp.models import CompanyDetailsModel
from shopApp.models import ShopDetailsModel
from shopServiceApp.models import (
    ShopServiceCategoryModel,
    ShopServiceDetailsModel,
    ServiceBookingDetailsModel
)
from customersApp.models import CustomersDetailsModel  # Use your actual customer model
from datetime import timedelta

User = get_user_model()

class ShopServiceAppAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.client.force_authenticate(user=self.user)
        self.company = CompanyDetailsModel.objects.create(user=self.user, name='TestCo')
        self.shop = ShopDetailsModel.objects.create(
            owner=self.user,
            company=self.company,
            shop_name='TestShop',
            name='Test Shop'
        )
        self.category = ShopServiceCategoryModel.objects.create(name='Cat1')
        self.service = ShopServiceDetailsModel.objects.create(
            shop=self.shop,
            category=self.category,
            name='Service1',
            description='Desc',
            price=50.00,
            duration=timedelta(minutes=30)
        )
        self.customer = CustomersDetailsModel.objects.create(user=self.user, name="Test Customer")

    def test_create_booking_and_fraud_flag(self):
        data = {
            'customer': self.customer.id,
            'service': self.service.id,
            'booking_date': '2025-04-10',
            'booking_time': '10:00:00'
        }
        url = reverse('shopServiceApp:services-bookings-list')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('fraud_flag', response.data)
