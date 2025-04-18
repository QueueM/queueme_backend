# followApp/views.py
from rest_framework import viewsets, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from .models import ShopFollow
from .serializers import ShopFollowSerializer, FeedItemSerializer
from shopApp.models import ShopDetailsModel
from reelsApp.models import ReelsModel
from storiesApp.models import StoryModel
from shopServiceApp.models import ShopServiceDetailsModel, ServiceBookingDiscountCouponsModel
from notificationsapp.models import NotificationModel

class ShopFollowViewSet(viewsets.ModelViewSet):
    """
    followApp:
      POST   /follow/follows/         → follow a shop
      GET    /follow/follows/         → list your follows
      DELETE /follow/follows/{id}/    → unfollow
    """
    queryset = ShopFollow.objects.all()             # ← give Spectacular a base queryset
    serializer_class = ShopFollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # per‑user filter
        customer = self.request.user.customersdetailsmodel
        return ShopFollow.objects.filter(customer=customer)

class FeedView(APIView):
    """
    GET /follow/feed/ → aggregated feed of reels, stories, services, discounts & notifications
    """
    permission_classes = [IsAuthenticated]
    serializer_class = FeedItemSerializer           # ← tell Spectacular which serializer to use

    def get(self, request):
        customer = request.user.customersdetailsmodel
        followed_ids = ShopFollow.objects.filter(customer=customer).values_list('shop_id', flat=True)
        items = []

        # Reels
        for r in ReelsModel.objects.filter(shop_id__in=followed_ids):
            items.append({
                'id': r.id,
                'content_type': 'reel',
                'created_at': r.created_at,
                'data': {
                    'video_url': r.video.url if r.video else '',
                    'caption': r.caption,
                    'shop': r.shop.shop_name,
                    'like_count': r.like_count(),
                }
            })

        # Stories
        for s in StoryModel.objects.filter(shop_id__in=followed_ids):
            items.append({
                'id': s.id,
                'content_type': 'story',
                'created_at': s.created_at,
                'data': {
                    'media_url': s.video.url if s.video else (s.image.url if s.image else ''),
                    'caption': s.caption,
                    'expires_at': s.expires_at,
                    'shop': s.shop.shop_name,
                    'view_count': s.view_count(),
                }
            })

        # Services
        for svc in ShopServiceDetailsModel.objects.filter(shop_id__in=followed_ids):
            items.append({
                'id': svc.id,
                'content_type': 'service',
                'created_at': svc.created_at,
                'data': {
                    'name': svc.name,
                    'description': svc.description,
                    'shop': svc.shop.shop_name,
                }
            })

        # Discounts
        for d in ServiceBookingDiscountCouponsModel.objects.filter(shop_id__in=followed_ids):
            items.append({
                'id': d.id,
                'content_type': 'discount',
                'created_at': d.start_date,
                'data': {
                    'code': d.code,
                    'discount_value': d.discount_value,
                    'shop': d.shop.shop_name,
                }
            })

        # Notifications
        owners = ShopDetailsModel.objects.filter(id__in=followed_ids).values_list('owner', flat=True)
        for n in NotificationModel.objects.filter(user__in=owners):
            items.append({
                'id': n.id,
                'content_type': 'notification',
                'created_at': n.created_at,
                'data': {
                    'title': n.title,
                    'message': n.message,
                    'from_shop_owner': n.user.username,
                }
            })

        # sort & return
        sorted_feed = sorted(items, key=lambda x: x['created_at'], reverse=True)
        return Response(self.serializer_class(sorted_feed, many=True).data, status=status.HTTP_200_OK)
