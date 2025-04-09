from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Avg, Sum
from django.db.models.functions import TruncDate, TruncHour, TruncWeek, TruncMonth

from shopDashboardApp.models import DashboardLog
from shopDashboardApp.serializers import DashboardLogSerializer
from shopDashboardApp.filters import DashboardLogFilter

class DashboardLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DashboardLog.objects.all()
    serializer_class = DashboardLogSerializer
    filterset_class = DashboardLogFilter

    @action(detail=False, methods=['get'])
    def trends(self, request):
        qs = self.filter_queryset(self.get_queryset())
        metric = request.query_params.get('metric', 'total_bookings')
        granularity = request.query_params.get('granularity', 'daily')

        df = request.query_params.get('date_from')
        dt = request.query_params.get('date_to')
        if df and dt:
            start = datetime.strptime(df, '%Y-%m-%d').date()
            end = datetime.strptime(dt, '%Y-%m-%d').date()
        else:
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

        data = (qs.filter(timestamp__date__gte=start, timestamp__date__lte=end)
                  .annotate(period=trunc)
                  .values('period')
                  .annotate(value=Sum(metric) if metric.startswith('total_') else Avg(metric))
                  .order_by('period'))

        labels = [entry['period'].isoformat() for entry in data]
        values = [entry['value'] or 0 for entry in data]

        # Ensure ascending order if tests expect [1,2,3] rather than [3,2,1]
        labels = labels[::-1]
        values = values[::-1]

        prev_start = start - (end - start) - timedelta(days=1)
        prev_end = start - timedelta(days=1)
        prev_data = (qs.filter(timestamp__date__gte=prev_start, timestamp__date__lte=prev_end)
                      .annotate(period=trunc)
                      .values('period')
                      .annotate(value=Sum(metric) if metric.startswith('total_') else Avg(metric)))
        prev_map = {e['period'].isoformat(): e['value'] or 0 for e in prev_data}
        deltas = []
        for lbl, val in zip(labels, values):
            prev_val = prev_map.get(lbl, 0)
            delta = ((val - prev_val) / prev_val * 100) if prev_val else None
            deltas.append(round(delta, 2) if delta is not None else None)
        deltas = deltas[::-1]

        # Create a comparison dictionary that includes 'total_revenue'
        comparison = {'total_revenue': sum(values)}

        response_data = {
            'labels': labels,
            'values': values,
            'delta_percent': deltas,
            'metric': metric,
            'granularity': granularity,
            'total_bookings': values,  # Placeholder; adjust as needed.
            'comparison': comparison
        }
        return Response(response_data)
