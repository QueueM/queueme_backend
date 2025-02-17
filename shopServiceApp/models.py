from django.db import models

# Create your models here.

# from shopApp.models import ShopSpecialistDetailsModel
from django.contrib.auth.models import User
from django.utils.timezone import now
# from django.core.exceptions import ValidationError
from rest_framework.exceptions import ValidationError
class ShopServiceCategoryModel(models.Model):
    name = models.CharField(max_length=200)

class ShopServiceTimeSlotModel(models.Model):
    class DAY_CHOICES(models.TextChoices):
        MONDAY = 'monday', 'Monday'
        TUESDAY = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY = 'thursday', 'Thursday'
        FRIDAY = 'friday', 'Friday'
        SATURDAY = 'saturday', 'Saturday'
        SUNDAY = 'sunday', 'Sunday'

    service = models.ForeignKey("shopServiceApp.ShopServiceDetailsModel", on_delete=models.CASCADE, related_name='available_time_slots')
    day = models.CharField(max_length=20, choices=DAY_CHOICES.choices)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.service.name} - {self.get_day_display()} ({self.start_time}"

class ShopServiceDetailsModel(models.Model):
    class SERVICES_TYPES_CHOICES(models.TextChoices):
        IN_SHOP = 'in_shop', 'In Shop'
        AT_HOME = 'at_home', 'At Home'
        BOTH = 'both', "Both"

    service_type = models.CharField(max_length=20, choices=SERVICES_TYPES_CHOICES.choices, default=SERVICES_TYPES_CHOICES.IN_SHOP)
    name = models.CharField(max_length=300)
    name_arabic = models.CharField(max_length=300, default="")
    description = models.TextField()
    category = models.ForeignKey(ShopServiceCategoryModel, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    min_price = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    max_price = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    duration = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True) #in minutes
    unit = models.CharField(max_length=200)
    number_of_bookings = models.IntegerField()
    is_availabe = models.BooleanField(default=False)
    specialists = models.ManyToManyField("shopApp.ShopSpecialistDetailsModel", related_name="services_assigned", null=True, blank=True)

class ServiceBookingDetailsModel(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        REQUESTED = 'requested', 'Requested'
        BOOKED = 'booked', 'Booked'
        COMPLETED = 'completed', "Completed"
        CANCELLED = 'cancelled', 'Cancelled'
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bokkings", null=True, blank=True)
    customer = models.ForeignKey("customersApp.CustomersDetailsModel", on_delete=models.CASCADE, null=True, blank=True)
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

class ShopServiceGalleryModel(models.Model):
    service = models.ForeignKey("shopServiceApp.ShopServiceDetailsModel", on_delete=models.CASCADE)
    file = models.FileField(upload_to='shop/service/gallery', null=True, blank=True)
