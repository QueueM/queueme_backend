# shopApp/models.py
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from companyApp.models import CompanyDetailsModel  # Assumes this exists

class ShopOpeningHoursModel(models.Model):
    """
    Represents the opening hours for a shop on a given day.
    """
    class DAYS_OF_WEEK(models.TextChoices):
        MONDAY    = 'monday', 'Monday'
        TUESDAY   = 'tuesday', 'Tuesday'
        WEDNESDAY = 'wednesday', 'Wednesday'
        THURSDAY  = 'thursday', 'Thursday'
        FRIDAY    = 'friday', 'Friday'
        SATURDAY  = 'saturday', 'Saturday'
        SUNDAY    = 'sunday', 'Sunday'

    shop = models.ForeignKey(
        'shopApp.ShopDetailsModel',
        related_name="opening_hours",
        on_delete=models.CASCADE,
        verbose_name="Shop"
    )
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK.choices, verbose_name="Day of Week")
    open_time = models.TimeField(verbose_name="Opening Time")
    close_time = models.TimeField(verbose_name="Closing Time")
    is_closed = models.BooleanField(default=False, verbose_name="Closed")

    class Meta:
        unique_together = ('shop', 'day')
        verbose_name = "Shop Opening Hour"
        verbose_name_plural = "Shop Opening Hours"
        indexes = [
            models.Index(fields=['day']),
        ]

    def __str__(self):
        if not self.is_closed:
            return f"{self.shop.shop_name} - {self.day}: {self.open_time} to {self.close_time}"
        return f"{self.shop.shop_name} - {self.day}: Closed"


class ShopDetailsModel(models.Model):
    """
    Stores the details of a shop/branch.
    """
    class TARGET_CUSTOMER_CHOICES(models.TextChoices):
        MALE   = 'male', 'Male'
        FEMALE = 'female', 'Female'
        BOTH   = 'both', 'Both'

    class SERVICES_TYPES_CHOICES(models.TextChoices):
        IN_SHOP = 'in_shop', 'In Shop'
        AT_HOME  = 'at_home', 'At Home'
        BOTH     = 'both', 'Both'

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Owner"
    )
    company = models.ForeignKey(
        CompanyDetailsModel,
        on_delete=models.CASCADE,
        verbose_name="Company"
    )
    name = models.CharField(max_length=300, unique=True, db_index=True, verbose_name="Unique Name")
    description = models.TextField(null=True, blank=True, verbose_name="Description")
    note = models.CharField(max_length=300, null=True, blank=True, verbose_name="Note")
    contact_number = models.CharField(max_length=30, null=True, blank=True, verbose_name="Contact Number")
    address = models.CharField(max_length=300, null=True, blank=True, verbose_name="Address")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Latitude")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Longitude")
    cover_image = models.ImageField(upload_to='images/shop/cover', null=True, verbose_name="Cover Image")
    avatar_image = models.ImageField(upload_to='images/shopgallery/', null=True, blank=True, verbose_name="Avatar Image")
    username = models.CharField(max_length=20, default="", blank=True, unique=True, verbose_name="Username")
    shop_name = models.CharField(max_length=300, default="", db_index=True, verbose_name="Shop Name")
    country = models.CharField(max_length=80, default="", blank=True, verbose_name="Country")
    city = models.CharField(max_length=300, default="", blank=True, verbose_name="City")
    district = models.CharField(max_length=300, default="", blank=True, verbose_name="District")
    customers_type = models.CharField(
        choices=TARGET_CUSTOMER_CHOICES.choices,
        max_length=20,
        default=TARGET_CUSTOMER_CHOICES.BOTH,
        verbose_name="Target Customers"
    )
    services_types = models.CharField(
        choices=SERVICES_TYPES_CHOICES.choices,
        max_length=20,
        default=SERVICES_TYPES_CHOICES.IN_SHOP,
        verbose_name="Services Types"
    )
    categories = models.ManyToManyField(
        'shopServiceApp.ShopServiceCategoryModel',
        related_name="shops",
        blank=True,
        verbose_name="Categories"
    )
    credits = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Credits for ads and other activities",
        default=0.0,
        verbose_name="Credits"
    )
    ai_recommendations = models.JSONField(
        blank=True,
        null=True,
        help_text="AI recommendation metadata",
        verbose_name="AI Recommendations"
    )
    ai_personalization = models.JSONField(
        blank=True,
        null=True,
        help_text="AI personalization metadata",
        verbose_name="AI Personalization"
    )
    # NEW FIELDS FOR ONLINE PAYMENT
    online_payment_requested = models.BooleanField(
        default=False,
        verbose_name="Receive Online Payments"
    )
    bank_details_document = models.FileField(
        upload_to='bank_details/',
        null=True,
        blank=True,
        verbose_name="Bank Details Document"
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
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        help_text="Creation timestamp",
        verbose_name="Created At"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Shop"
        verbose_name_plural = "Shops"

    def __str__(self):
        return self.shop_name


class ShopPermissionsModel(models.Model):
    """
    Stores permission settings for a shop within a company.
    """
    company = models.ForeignKey(
        CompanyDetailsModel,
        on_delete=models.CASCADE,
        verbose_name="Company"
    )
    shop = models.ForeignKey(
        ShopDetailsModel,
        on_delete=models.CASCADE,
        verbose_name="Shop"
    )
    can_create_product = models.BooleanField(default=False, verbose_name="Can Create Product")
    can_view_product = models.BooleanField(default=True, verbose_name="Can View Product")
    can_edit_product = models.BooleanField(default=False, verbose_name="Can Edit Product")
    can_delete_product = models.BooleanField(default=False, verbose_name="Can Delete Product")

    class Meta:
        verbose_name = "Shop Permission"
        verbose_name_plural = "Shop Permissions"

    def __str__(self):
        return f"Permissions for {self.shop.shop_name}"


class ShopGalleryImagesModel(models.Model):
    """
    Stores gallery images associated with a shop.
    """
    shop = models.ForeignKey(
        ShopDetailsModel,
        on_delete=models.CASCADE,
        verbose_name="Shop"
    )
    image = models.ImageField(upload_to='images/shopgallery', verbose_name="Image")

    class Meta:
        verbose_name = "Shop Gallery Image"
        verbose_name_plural = "Shop Gallery Images"

    def __str__(self):
        return f"Gallery Image {self.id} for {self.shop.shop_name}"


class SpecialistTypesModel(models.Model):
    """
    Stores types or categories of specialists.
    """
    name = models.CharField(max_length=300, verbose_name="Name")

    class Meta:
        verbose_name = "Specialist Type"
        verbose_name_plural = "Specialist Types"

    def __str__(self):
        return f"({self.id}) {self.name}"


class ShopSpecialistDetailsModel(models.Model):
    """
    Stores details about a specialist associated with one or more shops.
    """
    class SERVICE_LOCATION_CHOICES(models.TextChoices):
        IN_STORE = 'in_store', 'In Store'
        AT_SHOP  = 'at_shop', 'At Shop'
        BOTH     = 'both', 'Both'

    speciality = models.CharField(max_length=300, verbose_name="Speciality")
    shop = models.ManyToManyField(ShopDetailsModel, verbose_name="Shops")
    service_location = models.CharField(
        max_length=20,
        choices=SERVICE_LOCATION_CHOICES.choices,
        default=SERVICE_LOCATION_CHOICES.BOTH,
        verbose_name="Service Location"
    )
    specialist_type = models.ManyToManyField(SpecialistTypesModel, verbose_name="Specialist Type")
    services = models.ManyToManyField("shopServiceApp.ShopServiceDetailsModel", verbose_name="Services")
    is_active = models.BooleanField(default=True, verbose_name="Active")
    avatar_image = models.ImageField(
        upload_to='specialist/avatar_image/',
        null=True,
        blank=True,
        verbose_name="Avatar Image"
    )
    rating = models.FloatField(default=0.0, verbose_name="Rating")

    class Meta:
        verbose_name = "Shop Specialist Detail"
        verbose_name_plural = "Shop Specialist Details"

    def __str__(self):
        return f"({self.id}) {self.speciality}"
