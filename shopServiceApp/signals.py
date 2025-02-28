

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import ServiceBookingDetailsModel, ShopServiceDetailsModel, ServiceBookingDiscountCouponsModel, ShopServiceGalleryModel
from notificationsapp.models import NotificationModel

@receiver(post_save, sender=ServiceBookingDetailsModel)
def booking_created_updated_notification(sender, instance, created, **kwargs):
    if created:
        NotificationModel.objects.create(
            user=instance.customer.user,  
            title="Booking Requested",
            message=f"Booking requested by {instance.customer.user.username} for service {instance.service.name} at shop {instance.service.shop.name}"
        )
    else :
        NotificationModel.objects.create(
            user=instance.customer.user,  
            title="Booking updated",
            message=f"Booking updated by {instance.customer.user.username}, status : {instance.status},   for service {instance.service.name} at shop {instance.service.shop.name}"
        )

@receiver(post_save, sender=ServiceBookingDiscountCouponsModel)
def discount_coupon_created_updated_notification(sender, instance, created, **kwargs):
    if created:
        NotificationModel.objects.create(
            user=instance.shop.company.user,  
            title="Discount Coupon Created",
            message=f"Discount coupon created {instance.code}"
        )
    else :
        NotificationModel.objects.create(
            user=instance.shop.company.user,  
            title="Discount Coupon Updated",
            message=f"Discount coupon updated {instance.code}"
        )

@receiver(post_save, sender=ShopServiceDetailsModel)
def Service_created_updated_notification(sender, instance, created, **kwargs):
    if created:
        NotificationModel.objects.create(
            user=instance.shop.company.user,  
            title="Service Created",
            message=f"Service created {instance.name} for shop {instance.shop.name}"
        )
    else :
        NotificationModel.objects.create(
            user=instance.shop.company.user,  
            title="Service Updated",
            message=f"Service updated {instance.name} for shop {instance.shop.name}"
        )

@receiver(post_save, sender=ShopServiceGalleryModel)
def service_gallery_created_updated_notification(sender, instance, created, **kwargs):
    if created:
        NotificationModel.objects.create(
            user=instance.shop.company.user,  # Assuming Shop model has an owner field
            title="Added to Serivce Gallery",
            message=f"Added to gallery of service {instance.service.name}"
        )
    else :
        NotificationModel.objects.create(
            user=instance.shop.company.user,  # Assuming Shop model has an owner field
            title="Updated to Serivce Gallery",
            message=f"Updated to gallery of service {instance.service.name}"
        )

