from django.shortcuts import render

# Create your views here.
from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import NotificationModel
from .serializers import NotificationsSerializer
from .filters import NotificationFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet

from rest_framework import filters
class NotificationsViewSet(CustomBaseModelViewSet):
    queryset = NotificationModel.objects.all()
    serializer_class = NotificationsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = NotificationFilter
    # def get_serializer_context(self):
    #     context = super().get_serializer_context()
    #     context['user'] = self.request.user  # Pass the user into the context
    #     return context
    
    # def get_queryset(self):
    #     """
    #     This view should return the company details associated with the current user.
    #     """
    #     return ShopDetailsModel.objects.filter(company=self.request.user.company)