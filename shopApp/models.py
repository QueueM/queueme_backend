from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from companyApp.models import CompanyDetailsModel
from helpers.phone_utils import normalize_phone_number
from .constants import TargetCustomerChoices, ServicesTypesChoices

class ShopOpeningHoursModel(models.Model):
    shop = models.ForeignKey(
        'shopApp.ShopDetailsModel',
        related_name="opening_hours",
        on_delete=models.CASCADE,
        verbose_name="Shop"
    )
    day = models.CharField(
        max_length=10,
        choices=(
            ('monday', 'Monday'),
            ('tuesday', 'Tuesday'),
            ('wednesday', 'Wednesday'),
            ('thursday', 'Thursday'),
            ('friday', 'Friday'),
            ('saturday', 'Saturday'),
            ('sunday', 'Sunday'),
        ),
        verbose_name="Day of Week"
    )
    open_time = models.TimeField(verbose_name="Opening Time")
    close_time = models.TimeField(verbose_name="Closing Time")
    is_closed = models.BooleanField(default=False, verbose_name="Closed")

    class Meta:
        unique_together = ('shop', 'day')
        verbose_name = "Shop Opening Hour"
        verbose_name_plural = "Shop Opening Hours"
        indexes = [models.Index(fields=['day'])]

    def __str__(self):
        if not self.is_closed:
            return f"{self.shop.shop_name} - {self.day}: {self.open_time} to {self.close_time}"
        return f"{self.shop.shop_name} - {self.day}: Closed"

class ShopDetailsModel(models.Model):
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Owner"
    )
    company = models.ForeignKey(
        CompanyDetailsModel, on_delete=models.CASCADE, verbose_name="Company"
    )
    # Official shop name (unique)
    name = models.CharField(
        max_length=300, unique=True, db_index=True, verbose_name="Unique Name"
    )
    description = models.TextField(
        null=True, blank=True, verbose_name="Description"
    )
    note = models.CharField(
        max_length=300, null=True, blank=True, verbose_name="Note"
    )
    # Renamed for clarity (formerly 'contact_number')
    customer_service_phone = models.CharField(
        max_length=30, null=True, blank=True, verbose_name="Customer Service Phone"
    )
    address = models.CharField(
        max_length=300, null=True, blank=True, verbose_name="Address"
    )
    latitude = models.FloatField(null=True, blank=True, verbose_name="Latitude")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Longitude")
    cover_image = models.ImageField(
        upload_to='images/shop/cover', null=True, verbose_name="Cover Image"
    )
    avatar_image = models.ImageField(
        upload_to='images/shopgallery/', null=True, blank=True, verbose_name="Avatar Image"
    )
    username = models.CharField(
        max_length=20, default="", blank=True, unique=True, verbose_name="Username"
    )
    shop_name = models.CharField(
        max_length=300, default="", db_index=True, verbose_name="Shop Name"
    )
    country = models.CharField(
        max_length=80, default="", blank=True, verbose_name="Country"
    )
    city = models.CharField(
        max_length=300, default="", blank=True, verbose_name="City"
    )
    district = models.CharField(
        max_length=300, default="", blank=True, verbose_name="District"
    )
    customers_type = models.CharField(
        max_length=20,
        choices=TargetCustomerChoices.choices,
        default=TargetCustomerChoices.BOTH,
        verbose_name="Target Customers"
    )
    services_types = models.CharField(
        max_length=20,
        choices=ServicesTypesChoices.choices,
        default=ServicesTypesChoices.IN_SHOP,
        verbose_name="Services Types"
    )
    online_payment_requested = models.BooleanField(
        default=False, verbose_name="Receive Online Payments"
    )
    bank_details_document = models.FileField(
        upload_to='bank_details/', null=True, blank=True, verbose_name="Bank Details Document"
    )
    ONLINE_PAYMENT_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    online_payment_status = models.CharField(
        max_length=20,
        choices=ONLINE_PAYMENT_STATUS_CHOICES,
        default='pending',
        verbose_name="Online Payment Approval Status"
    )
    ai_recommendations = models.JSONField(
        blank=True, null=True, help_text="AI recommendation metadata", verbose_name="AI Recommendations"
    )
    ai_personalization = models.JSONField(
        blank=True, null=True, help_text="AI personalization metadata", verbose_name="AI Personalization"
    )
    created_at = models.DateTimeField(
        default=timezone.now, editable=False,
        help_text="Creation timestamp", verbose_name="Created At"
    )
    # **** New Field: Manager Phone Number ****
    # For the migration, we allow null (so existing rows can remain empty).
    # In your creation serializer, ensure a manager phone number is provided.
    manager_phone_number = models.CharField(
        max_length=20,
        null=True,         # Allow null for migration purposes
        blank=False,
        help_text="Manager Phone Number (used for branch login)",
        unique=True
    )

    def save(self, *args, **kwargs):
        if self.customer_service_phone:
            try:
                self.customer_service_phone = normalize_phone_number(self.customer_service_phone)
            except Exception:
                pass
        # Optionally, you may also normalize manager_phone_number here
        super().save(*args, **kwargs)

    def __str__(self):
        return self.shop_name

class ShopGalleryImagesModel(models.Model):
    shop = models.ForeignKey(
        ShopDetailsModel, on_delete=models.CASCADE, verbose_name="Shop"
    )
    image = models.ImageField(
        upload_to='images/shopgallery', verbose_name="Image"
    )

    class Meta:
        verbose_name = "Shop Gallery Image"
        verbose_name_plural = "Shop Gallery Images"

    def __str__(self):
        return f"Gallery Image {self.id} for {self.shop.shop_name}"

class SpecialistTypesModel(models.Model):
    name = models.CharField(max_length=300, verbose_name="Name")

    class Meta:
        verbose_name = "Specialist Type"
        verbose_name_plural = "Specialist Types"

    def __str__(self):
        return f"({self.id}) {self.name}"

class ShopSpecialistDetailsModel(models.Model):
    SERVICE_LOCATION_CHOICES = [
        ('in_store', 'In Store'),
        ('at_shop', 'At Shop'),
        ('both', 'Both'),
    ]
    speciality = models.CharField(max_length=300, verbose_name="Speciality")
    shop = models.ManyToManyField(ShopDetailsModel, verbose_name="Shops")
    service_location = models.CharField(
        max_length=20,
        choices=SERVICE_LOCATION_CHOICES,
        default='both',
        verbose_name="Service Location"
    )
    specialist_type = models.ManyToManyField(SpecialistTypesModel, verbose_name="Specialist Type")
    services = models.ManyToManyField('shopServiceApp.ShopServiceDetailsModel', verbose_name="Services")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    avatar_image = models.ImageField(
        upload_to='specialist/avatar_image/', null=True, blank=True, verbose_name="Avatar Image"
    )
    rating = models.FloatField(default=0.0, verbose_name="Rating")

    class Meta:
        verbose_name = "Shop Specialist Detail"
        verbose_name_plural = "Shop Specialist Details"

    def __str__(self):
        return f"({self.id}) {self.speciality}"
