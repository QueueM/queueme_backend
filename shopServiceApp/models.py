# shopServiceApp/models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from companyApp.models import CompanyDetailsModel

class ShopServiceCategoryModel(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        help_text="Creation timestamp"
    )
    forecast_data = models.JSONField(
        blank=True, null=True,
        help_text="AI forecast metadata for this category"
    )

    def __str__(self):
        return self.name

class ShopServiceTimeSlotModel(models.Model):
    class DAY_CHOICES(models.TextChoices):
        MONDAY    = 'monday',    'Monday'
        TUESDAY   = 'tuesday',   'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY  = 'thursday',  'Thursday'
        FRIDAY    = 'friday',    'Friday'
        SATURDAY  = 'saturday',  'Saturday'
        SUNDAY    = 'sunday',    'Sunday'

    service    = models.ForeignKey(
                     'shopServiceApp.ShopServiceDetailsModel',
                     on_delete=models.CASCADE,
                     related_name='available_time_slots'
                 )
    day        = models.CharField(max_length=20, choices=DAY_CHOICES.choices)
    start_time = models.TimeField()
    end_time   = models.TimeField()
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        help_text="Creation timestamp"
    )

    def __str__(self):
        return f"{self.service.name} - {self.day} ({self.start_time} to {self.end_time})"

class ShopServiceDetailsModel(models.Model):
    class SERVICES_TYPES_CHOICES(models.TextChoices):
        IN_SHOP = 'in_shop', 'In Shop'
        AT_HOME = 'at_home', 'At Home'
        BOTH    = 'both',    'Both'

    shop          = models.ForeignKey(
                        'shopApp.ShopDetailsModel',
                        on_delete=models.CASCADE,
                        related_name='services'
                    )
    category      = models.ForeignKey(
                        ShopServiceCategoryModel,
                        on_delete=models.CASCADE,
                        related_name='services'
                    )
    service_type  = models.CharField(
                        max_length=20,
                        choices=SERVICES_TYPES_CHOICES.choices,
                        default=SERVICES_TYPES_CHOICES.IN_SHOP
                    )
    name          = models.CharField(max_length=300)
    name_arabic   = models.CharField(max_length=300, default='', blank=True)
    description   = models.TextField(blank=True)
    price         = models.DecimalField(max_digits=10, decimal_places=2)
    duration      = models.DurationField(
                        default=timedelta(),   # provides a default for existing rows
                        help_text='Duration of service'
                    )
    is_available  = models.BooleanField(default=False)
    specialists   = models.ManyToManyField(
                        'shopApp.ShopSpecialistDetailsModel',
                        related_name='services_assigned',
                        blank=True
                    )
    created_at    = models.DateTimeField(
                        default=timezone.now,
                        editable=False,
                        help_text="Creation timestamp"
                    )
    forecast_data = models.JSONField(
                        blank=True, null=True,
                        help_text="AI forecast metadata for this service"
                    )

    def __str__(self):
        return f"{self.name} @ {self.shop.shop_name}"

class ServiceBookingDetailsModel(models.Model):
    class STATUS_CHOICES(models.TextChoices):
        REQUESTED = 'requested', 'Requested'
        BOOKED    = 'booked',    'Booked'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    class PAYMENT_STATUS_CHOICES(models.TextChoices):
        UNPAID  = 'unpaid',  'Unpaid'
        PENDING = 'pending', 'Pending'
        PAID    = 'paid',    'Paid'

    user           = models.ForeignKey(
                         User,
                         on_delete=models.CASCADE,
                         related_name='bookings',
                         null=True, blank=True
                     )
    customer       = models.ForeignKey(
                         'customersApp.CustomersDetailsModel',
                         on_delete=models.CASCADE
                     )
    service        = models.ForeignKey(
                         ShopServiceDetailsModel,
                         on_delete=models.CASCADE,
                         related_name='bookings'
                     )
    booking_date   = models.DateField()
    booking_time   = models.TimeField()
    price          = models.DecimalField(
                         max_digits=10, decimal_places=2,
                         blank=True, null=True
                     )
    final_amount   = models.DecimalField(
                         max_digits=10, decimal_places=2,
                         default=0.0
                     )
    status         = models.CharField(
                         max_length=20,
                         choices=STATUS_CHOICES.choices,
                         default=STATUS_CHOICES.REQUESTED
                     )
    payment_status = models.CharField(
                         max_length=20,
                         choices=PAYMENT_STATUS_CHOICES.choices,
                         default=PAYMENT_STATUS_CHOICES.UNPAID
                     )
    created_at     = models.DateTimeField(
                         default=timezone.now,
                         editable=False,
                         help_text="Creation timestamp"
                     )
    fraud_flag     = models.BooleanField(
                         default=False,
                         help_text="Flag if booking is potentially fraudulent"
                     )

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.service.price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Booking {self.id} for {self.service.name}"

class ServiceBookingDiscountCouponsModel(models.Model):
    class DISCOUNT_TYPE_CHOICES(models.TextChoices):
        PERCENTAGE = 'percentage', 'Percentage'
        AMOUNT     = 'amount',     'Amount'

    shop                 = models.ForeignKey(
                               'shopApp.ShopDetailsModel',
                               on_delete=models.CASCADE,
                               related_name='discount_coupons'
                           )
    code                 = models.CharField(max_length=20, unique=True)
    discount_type        = models.CharField(
                               max_length=10,
                               choices=DISCOUNT_TYPE_CHOICES.choices
                           )
    discount_value       = models.DecimalField(max_digits=10, decimal_places=2)
    start_date           = models.DateTimeField(default=timezone.now)
    end_date             = models.DateTimeField()
    max_usage            = models.PositiveIntegerField(default=1)
    is_active            = models.BooleanField(default=True)
    apply_to_all_services = models.BooleanField(default=False)
    services             = models.ManyToManyField(
                               ShopServiceDetailsModel,
                               blank=True,
                               related_name='eligible_coupons'
                           )

    def is_valid(self):
        now = timezone.now()
        return (
            self.is_active
            and self.start_date <= now <= self.end_date
            and self.bookings.count() < self.max_usage
        )

    def __str__(self):
        return self.code

class ShopServiceGalleryModel(models.Model):
    service = models.ForeignKey(
                  ShopServiceDetailsModel,
                  on_delete=models.CASCADE,
                  related_name='gallery'
              )
    file    = models.FileField(upload_to='shop/service/gallery')

    def __str__(self):
        return f"Gallery item for {self.service.name}"
