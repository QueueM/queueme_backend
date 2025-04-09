from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Avg, Sum
from django.db.models.functions import TruncDate, TruncHour, TruncWeek, TruncMonth

# Import DashboardLog-related serializer and model from the dashboard app
from shopDashboardApp.serializers import DashboardLogSerializer
from shopDashboardApp.models import DashboardLog
from .filters import DashboardLogFilter

# Import shop models and their serializers
from .models import (
    ShopDetailsModel,
    ShopGalleryImagesModel,
    ShopSpecialistDetailsModel,
    SpecialistTypesModel,
)
from .serializers import (
    ShopDetailsModelSerializer,
    ShopGalleryImagesModelSerializer,
    ShopSpecialistDetailsModelSerializer,
    SpecialistTypesSerializer,
)

# -------------------------------------
# DashboardLog ViewSet (for dashboard stats)
# -------------------------------------
class DashboardLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Provides a read-only API for DashboardLog entries with an additional 
    'trends' action that aggregates a specified metric over a date range.
    """
    queryset = DashboardLog.objects.all()
    serializer_class = DashboardLogSerializer
    filterset_class = DashboardLogFilter

    @action(detail=False, methods=['get'])
    def trends(self, request):
        qs = self.filter_queryset(self.get_queryset())
        metric = request.query_params.get('metric', 'total_bookings')
        granularity = request.query_params.get('granularity', 'daily')

        # Parse provided date range; if absent, default to the last 30 days.
        date_from = request.query_params.get('date_from')
        date_to = request.query_params.get('date_to')
        try:
            if date_from and date_to:
                start = datetime.strptime(date_from, '%Y-%m-%d').date()
                end = datetime.strptime(date_to, '%Y-%m-%d').date()
            else:
                end = timezone.now().date()
                start = end - timedelta(days=29)
        except ValueError:
            end = timezone.now().date()
            start = end - timedelta(days=29)

        # Set the truncation function based on the requested granularity.
        if granularity == 'hourly':
            trunc = TruncHour('timestamp')
        elif granularity == 'weekly':
            trunc = TruncWeek('timestamp')
        elif granularity == 'monthly':
            trunc = TruncMonth('timestamp')
        else:
            trunc = TruncDate('timestamp')

        # Aggregate data by period over the chosen date range.
        aggregated = (
            qs.filter(timestamp__date__gte=start, timestamp__date__lte=end)
              .annotate(period=trunc)
              .values('period')
              .annotate(value=Sum(metric) if metric.startswith('total_') else Avg(metric))
              .order_by('period')
        )
        # Extract labels (periods) and values, defaulting to 0 if missing.
        labels = [entry['period'].isoformat() for entry in aggregated]
        values = [entry['value'] or 0 for entry in aggregated]

        # Calculate statistics for the previous equivalent period.
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

        # Build an example comparison dictionary; adjust logic as needed.
        comparison = {'total_revenue': sum(values)}

        response_data = {
            'labels': labels,
            'values': values,
            'delta_percent': deltas,
            'metric': metric,
            'granularity': granularity,
            'total_bookings': values,  # You may compute a separate value if needed.
            'comparison': comparison,
        }
        return Response(response_data)


# -------------------------------------
# ShopDetails ViewSet - Handles CRUD for shops.
# -------------------------------------
class ShopDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing ShopDetails.
    Use the detail endpoint (e.g., GET /shops/8/) to retrieve a shop by its unique ID.
    """
    queryset = ShopDetailsModel.objects.all()
    serializer_class = ShopDetailsModelSerializer
    # If filtering by query parameters (e.g., company, query, id), you should
    # add: filterset_class = ShopDetailsViewsetFilter (from shopApp/filters.py)
    # For maximum efficiency, ensure your filterset and pagination are tuned to your use case.


# -------------------------------------
# ShopGalleryImages ViewSet
# -------------------------------------
class ShopGalleryImagesModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing ShopGalleryImages.
    """
    queryset = ShopGalleryImagesModel.objects.all()
    serializer_class = ShopGalleryImagesModelSerializer


# -------------------------------------
# ShopSpecialistDetails ViewSet
# -------------------------------------
class ShopSpecialistDetailsModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing ShopSpecialistDetails.
    """
    queryset = ShopSpecialistDetailsModel.objects.all()
    serializer_class = ShopSpecialistDetailsModelSerializer


# -------------------------------------
# SpecialistTypes ViewSet
# -------------------------------------
class SpecialistTypesModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing SpecialistTypes.
    """
    queryset = SpecialistTypesModel.objects.all()
    serializer_class = SpecialistTypesSerializer
