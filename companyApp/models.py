from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.serializers.json import DjangoJSONEncoder

class CompanyDetailsModel(models.Model):
    STATUS_CHOICES = [
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('created',  'Created'),
    ]

    class MERCHANT_TYPE(models.TextChoices):
        FREELANCE = 'freelance', 'Freelance'
        SHOP      = 'shop',      'Shop'

    user                  = models.OneToOneField(
                                User,
                                on_delete=models.CASCADE,
                                related_name='company'
                            )
    name                  = models.CharField(max_length=300)
    company_image         = models.ImageField(
                                upload_to='images/companylogo',
                                null=True, blank=True
                            )
    description           = models.TextField(null=True, blank=True)
    address               = models.TextField(null=True, blank=True)
    is_verified           = models.BooleanField(default=False)
    status                = models.CharField(
                                max_length=30,
                                choices=STATUS_CHOICES,
                                default='created'
                            )
    shops_limit           = models.IntegerField(default=1)
    merchant_type         = models.CharField(
                                max_length=20,
                                choices=MERCHANT_TYPE.choices,
                                default=MERCHANT_TYPE.FREELANCE
                            )
    name_arabic           = models.CharField(max_length=300, default='')
    registration_document = models.FileField(
                                upload_to='company_registration_doc/',
                                null=True, blank=True
                            )
    tax_number            = models.CharField(max_length=30, default='')

    # AI integration fields
    forecast_data = models.JSONField(
        encoder=DjangoJSONEncoder,
        default=dict,
        null=True,
        blank=True,
        help_text='AI forecast metadata (will JSON‑encode datetimes/timestamps)'
    )
    fraud_flag    = models.BooleanField(
                        default=False,
                        help_text='Flag if potential fraud detected'
                    )

    created_at    = models.DateTimeField(
                        default=timezone.now,
                        editable=False,
                        help_text='Creation timestamp'
                    )

    def __str__(self):
        return self.name
