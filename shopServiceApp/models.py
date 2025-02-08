from django.db import models

# Create your models here.

# from shopApp.models import ShopSpecialistDetailsModel
from django.contrib.auth.models import User
from django.utils.timezone import now
# from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError

class ShopServiceCategoryModel(models.Model):
    name = models.CharField(max_length=200)

class ShopServiceDetailsModel(models.Model):
    name = models.CharField(max_length=300)
    description = models.TextField()
    category = models.ForeignKey(ShopServiceCategoryModel, on_delete=models.CASCADE)
    price = models.FloatField()
    duration = models.FloatField()
    unit = models.CharField(max_length=200)
    number_of_bookings = models.IntegerField()

class ServiceBookingDetailsModel(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        REQUESTED = 'requested', 'Requested'
        BOOKED = 'booked', 'Booked'
        COMPLETED = 'completed', "Completed"
        CANCELLED = 'cancelled', 'Cancelled'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bokkings")
    service = models.ForeignKey(ShopServiceDetailsModel, on_delete=models.CASCADE, related_name="bokkings")
    price = models.FloatField(blank=True)
    specialist = models.ForeignKey("shopApp.ShopSpecialistDetailsModel", on_delete=models.CASCADE, related_name="bokkings", null=True)
    booking_date = models.DateField()
    booking_time = models.TimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES.choices, default=STATUS_CHOICES.REQUESTED)
    discount_coupon = models.CharField(max_length=20, blank=True, default="")
    cancellation_reason = models.TextField(blank=True, default='')
    final_amount = models.DecimalField(
        max_digits=100, decimal_places=2, help_text="Final Amount", default=0.0
    )
    notes = models.TextField()

    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.service.price
        if self.discount_coupon != "":
            if not ServiceBookingDiscountCouponsModel.objects.filter(code=self.discount_coupon).exists():
                raise ValidationError(f"Invalid discount code")
            discount = ServiceBookingDiscountCouponsModel.objects.get(code=self.discount_coupon)
            if not discount.is_valid:
                raise ValidationError(f"Discount code is not valid")
            amount = self.price
            if discount.discount_type == discount.DISCOUNT_TYPE_CHOICES.AMOUNT:
                amount =- discount.discount_value
            else:
                discountAmount = (amount/100)*discount.discount_value
                amount -= discountAmount
            self.final_amount = amount
        else :
            self.final_amount = self.price
        super().save(*args, **kwargs)

class ServiceBookingDiscountCouponsModel(models.Model):
    class DISCOUNT_TYPE_CHOICES(models.TextChoices):
        PERCENTAGE = 'percentage', 'Percentage'
        AMOUNT = 'amount', 'Amount'
    code = models.CharField(max_length=20)
    discount_type = models.CharField(
        max_length=10,
        choices=DISCOUNT_TYPE_CHOICES.choices,
    )
    discount_value = models.DecimalField(
        max_digits=10, decimal_places=2, help_text="Percentage or fixed discount value"
    )
    start_date = models.DateTimeField(default=now)
    end_date = models.DateTimeField()
    max_usage = models.PositiveIntegerField(default=1, help_text="Number of times a coupon can be used")
    is_active = models.BooleanField(default=True)

    def is_valid(self):
        """Check if the coupon is valid based on date, usage, and status."""
        return (
            self.is_active
            and self.start_date <= now() <= self.end_date
            and self.usage_count() < self.max_usage
        )
    
    def usage_count(self):
        """Count how many times the coupon has been used."""
        return self.bokkings.filter(coupon=self).count()