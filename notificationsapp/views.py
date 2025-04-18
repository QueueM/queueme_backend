from customClasses.CustomBaseModelViewSet import CustomBaseModelViewSet
from .models import NotificationModel
from .serializers import NotificationsSerializer
from .filters import NotificationFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

class NotificationsViewSet(CustomBaseModelViewSet):
    queryset = NotificationModel.objects.all()
    serializer_class = NotificationsSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = NotificationFilter
