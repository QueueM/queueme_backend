from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from django.utils import timezone
from datetime import timedelta
from companyApp.models import CompanyDetailsModel
from shopApp.models import ShopDetailsModel
from .models import DashboardLog

class DashboardTrendsTest(TestCase):
    def setUp(self):
        user = User.objects.create_user(username="co", password="pw")
        self.company = CompanyDetailsModel.objects.create(user=user, name="Co")
        shop = ShopDetailsModel.objects.create(
            owner=user,
            company=self.company,
            shop_name="MyShop",
            name="MyShop"
        )
        today = timezone.now().date()
        for i in range(3):
            DashboardLog.objects.create(
                timestamp=timezone.now() - timedelta(days=i),
                company=self.company,
                shop=shop,
                total_bookings=i+1,
                total_revenue=(i+1)*10.0,
                total_specialists=1,
                total_waiting=0,
                total_in_progress=0,
                total_completed=i+1,
                total_cancelled=0,
                estimated_wait_time="0m",
                total_employees=2,
                average_salary=50.0,
                total_customers=5,
                customer_retention_rate=50.0,
                average_rating=4.5,
                total_reels_likes=0,
                total_ad_impressions=0,
                total_ad_viewers=0,
                total_ad_clicks=0,
                top_services=[{"service":"Test", "bookings":i+1}],
            )
        self.client = APIClient()
        self.client.force_authenticate(user=user)

    def test_daily_trends(self):
        resp = self.client.get("/dashboard/dashboard-logs/trends/", {"company": self.company.pk, "granularity": "daily"})
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        self.assertEqual(len(data["labels"]), 3)
