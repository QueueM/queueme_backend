# shopApp/views.py
from rest_framework import viewsets, filters, status
from rest_framework.decorators import action  # Import action
from rest_framework.response import Response
from django.utils import timezone
from datetime import datetime, timedelta
from django.db.models import Avg, Sum
from django.db.models.functions import TruncDate, TruncHour, TruncWeek, TruncMonth
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import AllowAny

# DashboardLog imports from shopDashboardApp
from shopDashboardApp.serializers import DashboardLogSerializer
from shopDashboardApp.models import DashboardLog
from shopDashboardApp.filters import DashboardLogFilter

# Filters for shopApp
from .filters import (
    DashboardLogFilter as ShopDashboardLogFilter,
    ShopDetailsViewsetFilter,
    ShopGalleryImagesFilter,
    ShopSpecialistDetailsFilter,
)

# Models from shopApp
from .models import (
    ShopDetailsModel,
    ShopGalleryImagesModel,
    ShopSpecialistDetailsModel,
    SpecialistTypesModel,
)

# Serializers from shopApp
from .serializers import (
    ShopDetailsModelSerializer,
    ShopGalleryImagesModelSerializer,
    ShopSpecialistDetailsModelSerializer,
    SpecialistTypesSerializer,
)

class DashboardLogViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-only API for DashboardLog entries with an additional 'trends' action.
    """
    queryset = DashboardLog.objects.all()
    serializer_class = DashboardLogSerializer
    filterset_class = DashboardLogFilter
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def trends(self, request):
        qs = self.filter_queryset(self.get_queryset())
        metric = request.query_params.get('metric', 'total_bookings')
        granularity = request.query_params.get('granularity', 'daily')

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

class ShopDetailsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing ShopDetails.
    Filtering logic:
      - If "shopId" is provided in query params, return only that shop.
      - If "companyId" is provided and no shopId, return shops for that company.
      - Otherwise, return all shops.
    """
    queryset = ShopDetailsModel.objects.all()
    serializer_class = ShopDetailsModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ShopDetailsViewsetFilter
    search_fields = ['shop_name', 'owner__username']
    ordering_fields = ['created_at', 'shop_name']
    permission_classes = [AllowAny]

    def get_queryset(self):
        qs = super().get_queryset()
        shop_id_param = self.request.query_params.get('shopId') or self.request.query_params.get('shopid')
        company_id_param = self.request.query_params.get('companyId') or self.request.query_params.get('companyid')
        
        if shop_id_param:
            try:
                shop_id = int(shop_id_param)
                qs = qs.filter(id=shop_id)
            except ValueError:
                pass
        elif company_id_param:
            try:
                company_id = int(company_id_param)
                qs = qs.filter(company__id=company_id)
            except ValueError:
                pass
        
        return qs

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['user'] = self.request.user
        return context

class ShopGalleryImagesModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing ShopGalleryImages.
    """
    queryset = ShopGalleryImagesModel.objects.all()
    serializer_class = ShopGalleryImagesModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ShopGalleryImagesFilter
    search_fields = ['shop__shop_name']
    ordering_fields = ['id']
    permission_classes = [AllowAny]

class ShopSpecialistDetailsModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing ShopSpecialistDetails.
    """
    queryset = ShopSpecialistDetailsModel.objects.all()
    serializer_class = ShopSpecialistDetailsModelSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ShopSpecialistDetailsFilter
    search_fields = ['speciality', 'employee__name']
    ordering_fields = ['id', 'rating']
    permission_classes = [AllowAny]

class SpecialistTypesModelViewSet(viewsets.ModelViewSet):
    """
    API endpoint for managing SpecialistTypes.
    """
    queryset = SpecialistTypesModel.objects.all()
    serializer_class = SpecialistTypesSerializer
    permission_classes = [AllowAny]
