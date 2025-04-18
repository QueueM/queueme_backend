# File: shopServiceApp/models.py

from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from companyApp.models import CompanyDetailsModel
from shopApp.models import ShopDetailsModel

# ──────────────────────────────────────────────────────────────────────────────
# Move TextChoices out into their own top‐level class
# ──────────────────────────────────────────────────────────────────────────────
class ServiceTypeEnum(models.TextChoices):
    IN_SHOP = 'in_shop', 'In Shop'
    AT_HOME = 'at_home', 'At Home'
    BOTH    = 'both',    'Both'


class ShopServiceCategoryModel(models.Model):
    name         = models.CharField(max_length=200)
    created_at   = models.DateTimeField(default=timezone.now, editable=False)
    forecast_data = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name        = "Shop Service Category"
        verbose_name_plural = "Shop Service Categories"

    def __str__(self):
        return self.name


class ShopServiceTimeSlotModel(models.Model):
    class DayChoices(models.TextChoices):
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
    day        = models.CharField(max_length=20, choices=DayChoices.choices)
    start_time = models.TimeField()
    end_time   = models.TimeField()
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        verbose_name        = "Service Time Slot"
        verbose_name_plural = "Service Time Slots"

    def __str__(self):
        return f"{self.service.name} - {self.day} ({self.start_time} to {self.end_time})"


class ShopServiceDetailsModel(models.Model):
    shop        = models.ForeignKey(
        ShopDetailsModel,
        on_delete=models.CASCADE,
        related_name='services'
    )
    category    = models.ForeignKey(
        ShopServiceCategoryModel,
        on_delete=models.CASCADE,
        related_name='services'
    )
    service_type = models.CharField(
        max_length=20,
        choices=ServiceTypeEnum.choices,
        default=ServiceTypeEnum.IN_SHOP
    )
    name          = models.CharField(max_length=300)
    name_arabic   = models.CharField(max_length=300, default='', blank=True)
    description   = models.TextField(blank=True)
    price         = models.DecimalField(max_digits=10, decimal_places=2)
    duration      = models.DurationField(default=timedelta(), help_text='Duration of service')
    is_available  = models.BooleanField(default=False)
    specialists   = models.ManyToManyField(
        'shopApp.ShopSpecialistDetailsModel',
        related_name='services_assigned',
        blank=True
    )
    created_at    = models.DateTimeField(default=timezone.now, editable=False)
    forecast_data = models.JSONField(blank=True, null=True)

    class Meta:
        verbose_name        = "Shop Service Detail"
        verbose_name_plural = "Shop Service Details"

    def __str__(self):
        return f"{self.name} @ {self.shop.shop_name}"


class ServiceBookingDetailsModel(models.Model):
    class StatusChoices(models.TextChoices):
        REQUESTED = 'requested', 'Requested'
        BOOKED    = 'booked',    'Booked'
        COMPLETED = 'completed', 'Completed'
        CANCELLED = 'cancelled', 'Cancelled'

    class PaymentStatusChoices(models.TextChoices):
        UNPAID  = 'unpaid',  'Unpaid'
        PENDING = 'pending', 'Pending'
        PAID    = 'paid',    'Paid'

    user           = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings', null=True, blank=True)
    customer       = models.ForeignKey('customersApp.CustomersDetailsModel', on_delete=models.CASCADE)
    service        = models.ForeignKey(ShopServiceDetailsModel, on_delete=models.CASCADE, related_name='bookings')
    booking_date   = models.DateField()
    booking_time   = models.TimeField()
    price          = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    final_amount   = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    status         = models.CharField(max_length=20, choices=StatusChoices.choices, default=StatusChoices.REQUESTED)
    payment_status = models.CharField(max_length=20, choices=PaymentStatusChoices.choices, default=PaymentStatusChoices.UNPAID)
    created_at     = models.DateTimeField(default=timezone.now, editable=False)
    fraud_flag     = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.price is None:
            self.price = self.service.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name        = "Service Booking Detail"
        verbose_name_plural = "Service Booking Details"

    def __str__(self):
        return f"Booking {self.id} for {self.service.name}"


class ServiceBookingDiscountCouponsModel(models.Model):
    class DiscountType(models.TextChoices):
        PERCENTAGE = 'percentage', 'Percentage'
        AMOUNT     = 'amount',     'Amount'

    shop              = models.ForeignKey(ShopDetailsModel, on_delete=models.CASCADE, related_name='discount_coupons')
    code              = models.CharField(max_length=20, unique=True)
    discount_type     = models.CharField(max_length=10, choices=DiscountType.choices)
    discount_value    = models.DecimalField(max_digits=10, decimal_places=2)
    start_date        = models.DateTimeField(default=timezone.now)
    end_date          = models.DateTimeField()
    max_usage         = models.PositiveIntegerField(default=1)
    is_active         = models.BooleanField(default=True)
    apply_to_all_services = models.BooleanField(default=False)
    services          = models.ManyToManyField(ShopServiceDetailsModel, blank=True, related_name='eligible_coupons')

    def is_valid(self):
        now = timezone.now()
        return (self.is_active and self.start_date <= now <= self.end_date)

    class Meta:
        verbose_name        = "Service Booking Discount Coupon"
        verbose_name_plural = "Service Booking Discount Coupons"

    def __str__(self):
        return self.code


class ShopServiceGalleryModel(models.Model):
    service = models.ForeignKey(ShopServiceDetailsModel, on_delete=models.CASCADE, related_name='gallery')
    file    = models.FileField(upload_to='shop/service/gallery')

    class Meta:
        verbose_name        = "Shop Service Gallery Item"
        verbose_name_plural = "Shop Service Gallery Items"

    def __str__(self):
        return f"Gallery item for {self.service.name}"

class ServiceExtendedDetailsModel(models.Model):
    """
    Holds extended details for a service.
    Linked one-to-one with ShopServiceDetailsModel.
    """
    service     = models.OneToOneField(
                      ShopServiceDetailsModel,
                      on_delete=models.CASCADE,
                      related_name='extended_details',
                      verbose_name='Service'
                  )
    detailed_description = models.TextField(
                               blank=True,
                               null=True,
                               help_text="A detailed description of the service.",
                               verbose_name="Detailed Description"
                           )
    updated_at  = models.DateTimeField(
                      default=timezone.now,
                      verbose_name="Updated At"
                  )

    class Meta:
        verbose_name = "Service Extended Detail"
        verbose_name_plural = "Service Extended Details"

    def __str__(self):
        return f"{self.service.name} - Extended Details"

class ServiceOverview(models.Model):
    extended_details = models.ForeignKey(
                           ServiceExtendedDetailsModel,
                           on_delete=models.CASCADE,
                           related_name='overviews',
                           verbose_name='Extended Details'
                       )
    title            = models.CharField(
                           max_length=200,
                           help_text="Title of the overview item"
                       )
    image            = models.ImageField(
                           upload_to='service_overview/',
                           blank=True,
                           null=True,
                           help_text="Optional image for the overview item"
                       )
    description      = models.TextField(
                           blank=True,
                           help_text="Optional description for the overview item"
                       )
    order_index      = models.PositiveIntegerField(
                           default=0,
                           help_text="Order index for display"
                       )

    class Meta:
        ordering = ['order_index']
        verbose_name = "Service Overview"
        verbose_name_plural = "Service Overviews"

    def __str__(self):
        return f"Overview: {self.title}"

class ServiceFAQ(models.Model):
    extended_details = models.ForeignKey(
                           ServiceExtendedDetailsModel,
                           on_delete=models.CASCADE,
                           related_name='faqs',
                           verbose_name='Extended Details'
                       )
    question         = models.CharField(
                           max_length=300,
                           help_text="The FAQ question"
                       )
    answer           = models.TextField(
                           help_text="The answer to the FAQ question"
                       )
    order_index      = models.PositiveIntegerField(
                           default=0,
                           help_text="Order index for display"
                       )

    class Meta:
        ordering = ['order_index']
        verbose_name = "Service FAQ"
        verbose_name_plural = "Service FAQs"

    def __str__(self):
        return f"FAQ: {self.question}"

class ServiceProcessStep(models.Model):
    extended_details = models.ForeignKey(
                           ServiceExtendedDetailsModel,
                           on_delete=models.CASCADE,
                           related_name='process_steps',
                           verbose_name='Extended Details'
                       )
    order_index      = models.PositiveIntegerField(
                           default=0,
                           help_text="Order index for display"
                       )
    title            = models.CharField(
                           max_length=200,
                           help_text="Title of the process step"
                       )
    image            = models.ImageField(
                           upload_to='service_process_steps/',
                           blank=True,
                           null=True,
                           help_text="Optional image for the step"
                       )
    description      = models.TextField(
                           blank=True,
                           help_text="Description of this process step"
                       )

    class Meta:
        ordering = ['order_index']
        verbose_name = "Service Process Step"
        verbose_name_plural = "Service Process Steps"

    def __str__(self):
        return f"Step {self.order_index}: {self.title}"

class ServiceBenefit(models.Model):
    extended_details = models.ForeignKey(
                           ServiceExtendedDetailsModel,
                           on_delete=models.CASCADE,
                           related_name='benefits',
                           verbose_name='Extended Details'
                       )
    benefit_text     = models.CharField(max_length=300)
    order_index      = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order_index']
        verbose_name = "Service Benefit"
        verbose_name_plural = "Service Benefits"

    def __str__(self):
        return f"Benefit: {self.benefit_text}"

class ServiceAftercareTip(models.Model):
    extended_details = models.ForeignKey(
                           ServiceExtendedDetailsModel,
                           on_delete=models.CASCADE,
                           related_name='aftercare_tips',
                           verbose_name='Extended Details'
                       )
    tip_text         = models.CharField(max_length=300)
    order_index      = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order_index']
        verbose_name = "Service Aftercare Tip"
        verbose_name_plural = "Service Aftercare Tips"

    def __str__(self):
        return f"Aftercare Tip: {self.tip_text}"
