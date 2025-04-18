from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Avg, Sum
from django.db.models.functions import TruncDate, TruncHour, TruncWeek, TruncMonth
from shopDashboardApp.models import DashboardLog
from shopDashboardApp.serializers import DashboardLogSerializer
from shopDashboardApp.filters import DashboardLogFilter
from companyApp.models import CompanyDetailsModel
from shopApp.models import ShopDetailsModel

def get_user_company(user):
    try:
        return user.company
    except CompanyDetailsModel.DoesNotExist:
        return None

class DashboardLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DashboardLog.objects.all()
    serializer_class = DashboardLogSerializer
    filterset_class = DashboardLogFilter
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        qs = super().get_queryset()
        shopid_param = self.request.query_params.get('shopid')
        company = get_user_company(user)
        if company:
            qs = qs.filter(shop__company=company)
        else:
            qs = qs.filter(shop__owner=user)
        if shopid_param:
            try:
                shopid = int(shopid_param)
                qs = qs.filter(shop_id=shopid)
            except ValueError:
                pass
        return qs

    def list(self, request, *args, **kwargs):
        user = self.request.user
        company = get_user_company(user)
        if company:
            return super().list(request, *args, **kwargs)
        else:
            try:
                shop = ShopDetailsModel.objects.get(owner=user)
            except ShopDetailsModel.DoesNotExist:
                return Response([], status=status.HTTP_200_OK)
            latest_log = DashboardLog.objects.filter(shop=shop).order_by('-timestamp').first()
            if latest_log:
                serializer = self.get_serializer(latest_log)
                return Response([serializer.data], status=status.HTTP_200_OK)
            else:
                return Response([], status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def trends(self, request):
        qs = self.filter_queryset(self.get_queryset())
        metric = request.query_params.get('metric', 'total_bookings')
        granularity = request.query_params.get('granularity', 'daily')
        df = request.query_params.get('date_from')
        dt = request.query_params.get('date_to')
        try:
            if df and dt:
                start = datetime.strptime(df, '%Y-%m-%d').date()
                end = datetime.strptime(dt, '%Y-%m-%d').date()
            else:
                end = timezone.now().date()
                start = end - timedelta(days=29)
        except ValueError:
            end = timezone.now().date()
            start = end - timedelta(days=29)
        if granularity == 'hourly':
            trunc = TruncHour('timestamp')
        elif granularity == 'weekly':
            trunc = TruncWeek('timestamp')
        elif granularity == 'monthly':
            trunc = TruncMonth('timestamp')
        else:
            trunc = TruncDate('timestamp')
        aggregated = (
            qs.filter(timestamp__date__gte=start, timestamp__date__lte=end)
              .annotate(period=trunc)
              .values('period')
              .annotate(value=Sum(metric) if metric.startswith('total_') else Avg(metric))
              .order_by('period')
        )
        labels = [entry['period'].isoformat() for entry in aggregated]
        values = [entry['value'] or 0 for entry in aggregated]
        period_length = (end - start) + timedelta(days=1)
        prev_start = start - period_length
        prev_end = start - timedelta(days=1)
        prev_data = (
            qs.filter(timestamp__date__gte=prev_start, timestamp__date__lte=prev_end)
              .annotate(period=trunc)
              .values('period')
              .annotate(value=Sum(metric) if metric.startswith('total_') else Avg(metric))
              .order_by('period')
        )
        prev_map = {entry['period'].isoformat(): entry['value'] or 0 for entry in prev_data}
        deltas = []
        for lbl, val in zip(labels, values):
            prev_val = prev_map.get(lbl, 0)
            delta = ((val - prev_val) / prev_val * 100) if prev_val else None
            deltas.append(round(delta, 2) if delta is not None else None)
        comparison = {'total_revenue': sum(values)}
        response_data = {
            'labels': labels,
            'values': values,
            'delta_percent': deltas,
            'metric': metric,
            'granularity': granularity,
            'comparison': comparison,
        }
        return Response(response_data)
