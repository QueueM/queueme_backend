from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny  # Import AllowAny for public access
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Avg, Sum
from django.db.models.functions import TruncDate, TruncHour, TruncWeek, TruncMonth

from shopDashboardApp.models import DashboardLog
from shopDashboardApp.serializers import DashboardLogSerializer
from shopDashboardApp.filters import DashboardLogFilter

class DashboardLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint for retrieving and aggregating dashboard log data.
    
    Supports filtering by companyid, shopid, and date range via query parameters,
    plus a custom 'trends' action that computes aggregated values and percent changes.
    """
    queryset = DashboardLog.objects.all()
    serializer_class = DashboardLogSerializer
    filterset_class = DashboardLogFilter
    permission_classes = [AllowAny]  # Change this based on your security requirements

    @action(detail=False, methods=['get'])
    def trends(self, request):
        # Start with the filtered queryset (the filter is applied automatically)
        qs = self.filter_queryset(self.get_queryset())
        
        # Retrieve optional query parameters for aggregation
        metric = request.query_params.get('metric', 'total_bookings')
        granularity = request.query_params.get('granularity', 'daily')

        # Parse the date range; if not provided, default to the last 30 days.
        df = request.query_params.get('date_from')
        dt = request.query_params.get('date_to')
        if df and dt:
            start = datetime.strptime(df, '%Y-%m-%d').date()
            end = datetime.strptime(dt, '%Y-%m-%d').date()
        else:
            end = timezone.now().date()
            start = end - timedelta(days=29)

        # Select the truncation function based on granularity.
        if granularity == 'hourly':
            trunc = TruncHour('timestamp')
        elif granularity == 'weekly':
            trunc = TruncWeek('timestamp')
        elif granularity == 'monthly':
            trunc = TruncMonth('timestamp')
        else:
            trunc = TruncDate('timestamp')

        # Aggregate data for the current period.
        data = (
            qs.filter(timestamp__date__gte=start, timestamp__date__lte=end)
              .annotate(period=trunc)
              .values('period')
              .annotate(value=Sum(metric) if metric.startswith('total_') else Avg(metric))
              .order_by('period')
        )
        labels = [entry['period'].isoformat() for entry in data]
        values = [entry['value'] or 0 for entry in data]

        # Reverse the arrays if you prefer ascending order.
        labels = labels[::-1]
        values = values[::-1]

        # Calculate the previous period's data for comparison.
        period_length = (end - start) + timedelta(days=1)
        prev_start = start - period_length - timedelta(days=1)
        prev_end = start - timedelta(days=1)
        prev_data = (
            qs.filter(timestamp__date__gte=prev_start, timestamp__date__lte=prev_end)
              .annotate(period=trunc)
              .values('period')
              .annotate(value=Sum(metric) if metric.startswith('total_') else Avg(metric))
              .order_by('period')
        )
        prev_map = {entry['period'].isoformat(): entry['value'] or 0 for entry in prev_data}

        # Calculate the percentage delta between the current and previous periods.
        deltas = []
        for lbl, val in zip(labels, values):
            prev_val = prev_map.get(lbl, 0)
            delta = ((val - prev_val) / prev_val * 100) if prev_val else None
            deltas.append(round(delta, 2) if delta is not None else None)
        deltas = deltas[::-1]  # Reverse if needed

        # Create an example comparison object – here, the sum of values is used.
        comparison = {'total_revenue': sum(values)}

        response_data = {
            'labels': labels,
            'values': values,
            'delta_percent': deltas,
            'metric': metric,
            'granularity': granularity,
            'total_bookings': values,  # Placeholder; adjust per your logic.
            'comparison': comparison
        }
        return Response(response_data)
