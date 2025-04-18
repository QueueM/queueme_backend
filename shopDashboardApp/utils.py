import logging
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.utils import timezone
from django.db.models import Avg, Count, Sum
from shopServiceApp.models import ServiceBookingDetailsModel
from shopApp.models import ShopSpecialistDetailsModel
from companyApp.models import CompanyDetailsModel
from employeeApp.models import EmployeeDetailsModel
from customersApp.models import CustomersDetailsModel
from reviewapp.models import Review
from reelsApp.models import ReelsModel
from adsApp.models import ShopAdsImpressionModel
from shopDashboardApp.models import DashboardLog

logger = logging.getLogger(__name__)

def compute_and_broadcast_dashboard(sender, instance, created, deleted, **kwargs):
    now = timezone.now()
    shop = instance.service.shop
    company = shop.company

    def build_metrics(qs, shop=None):
        counts = {
            'waiting': qs.filter(status='requested').count(),
            'in_progress': qs.filter(status='booked').count(),
            'completed': qs.filter(status='completed').count(),
            'cancelled': qs.filter(status='cancelled').count(),
        }
        total_bookings = sum(counts.values())
        avg_dur = qs.filter(status='booked').aggregate(avg=Avg('service__duration'))['avg'] or 0
        est_wait = int(counts['waiting'] * (avg_dur.total_seconds() / 60)) if avg_dur else 0
        total_revenue = qs.aggregate(total=Sum('final_amount'))['total'] or 0.0
        total_specialists = ShopSpecialistDetailsModel.objects.count()
        total_employees = EmployeeDetailsModel.objects.count()
        avg_salary = EmployeeDetailsModel.objects.aggregate(avg=Avg('salary'))['avg'] or 0.0
        total_customers = CustomersDetailsModel.objects.count()
        repeat_custs = qs.values('customer').annotate(c=Count('id')).filter(c__gt=1).count()
        retention_rate = (repeat_custs / total_customers * 100) if total_customers else 0.0
        average_rating = Review.objects.aggregate(avg=Avg('rating'))['avg'] or 0.0
        total_reels_likes = ReelsModel.objects.aggregate(total=Sum('likes'))['total'] or 0
        ad_qs = ShopAdsImpressionModel.objects.filter(ad__shop=shop) if shop else ShopAdsImpressionModel.objects.filter(ad__shop__company=company)
        total_ad_impressions = ad_qs.count()
        total_ad_viewers = ad_qs.values('user').distinct().count()
        total_ad_clicks = ad_qs.filter(impression_type=ShopAdsImpressionModel.IMPRESSION_TYPES.CLICK).values('user').distinct().count()
        top_qs = (
            qs.values('service__name')
            .annotate(bookings=Count('id'))
            .order_by('-bookings')[:5]
        )
        top_services = [{'service': x['service__name'], 'bookings': x['bookings']} for x in top_qs]
        return {
            'timestamp': now,
            'total_bookings': total_bookings,
            'total_revenue': float(total_revenue),
            'total_specialists': total_specialists,
            'total_waiting': counts['waiting'],
            'total_in_progress': counts['in_progress'],
            'total_completed': counts['completed'],
            'total_cancelled': counts['cancelled'],
            'estimated_wait_time': f"{est_wait} minutes",
            'total_employees': total_employees,
            'average_salary': round(avg_salary, 2),
            'total_customers': total_customers,
            'customer_retention_rate': round(retention_rate, 2),
            'average_rating': round(average_rating, 2),
            'total_reels_likes': total_reels_likes,
            'total_ad_impressions': total_ad_impressions,
            'total_ad_viewers': total_ad_viewers,
            'total_ad_clicks': total_ad_clicks,
            'top_services': top_services,
        }

    layer = get_channel_layer()
    shop_qs = ServiceBookingDetailsModel.objects.filter(service__shop=shop)
    shop_data = build_metrics(shop_qs, shop=shop)
    async_to_sync(layer.group_send)(f"queue_dashboard_shop_{shop.id}", {"type": "queue_update", "data": shop_data})
    DashboardLog.objects.create(company=company, shop=shop, **shop_data)
    comp_qs = ServiceBookingDetailsModel.objects.filter(service__shop__company=company)
    comp_data = build_metrics(comp_qs)
    async_to_sync(layer.group_send)(f"queue_dashboard_company_{company.id}", {"type": "queue_update", "data": comp_data})
    DashboardLog.objects.create(company=company, shop=None, **comp_data)
