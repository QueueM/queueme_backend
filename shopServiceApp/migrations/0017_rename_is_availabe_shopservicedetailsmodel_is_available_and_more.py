# Generated by Django 5.1.4 on 2025-04-08 09:30

import datetime
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0015_rename_service_locatioin_shopspecialistdetailsmodel_service_location_and_more'),
        ('shopServiceApp', '0016_servicebookingdetailsmodel_rating'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='shopservicedetailsmodel',
            old_name='is_availabe',
            new_name='is_available',
        ),
        migrations.RemoveField(
            model_name='servicebookingdetailsmodel',
            name='booking_place',
        ),
        migrations.RemoveField(
            model_name='servicebookingdetailsmodel',
            name='cancellation_reason',
        ),
        migrations.RemoveField(
            model_name='servicebookingdetailsmodel',
            name='discount_coupon',
        ),
        migrations.RemoveField(
            model_name='servicebookingdetailsmodel',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='servicebookingdetailsmodel',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='servicebookingdetailsmodel',
            name='specialist',
        ),
        migrations.RemoveField(
            model_name='shopservicedetailsmodel',
            name='max_price',
        ),
        migrations.RemoveField(
            model_name='shopservicedetailsmodel',
            name='min_price',
        ),
        migrations.RemoveField(
            model_name='shopservicedetailsmodel',
            name='unit',
        ),
        migrations.AddField(
            model_name='servicebookingdetailsmodel',
            name='fraud_flag',
            field=models.BooleanField(default=False, help_text='Flag if booking is potentially fraudulent'),
        ),
        migrations.AddField(
            model_name='shopservicecategorymodel',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Creation timestamp'),
        ),
        migrations.AddField(
            model_name='shopservicecategorymodel',
            name='forecast_data',
            field=models.JSONField(blank=True, help_text='AI forecast metadata for this category', null=True),
        ),
        migrations.AddField(
            model_name='shopservicedetailsmodel',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Creation timestamp'),
        ),
        migrations.AddField(
            model_name='shopservicedetailsmodel',
            name='forecast_data',
            field=models.JSONField(blank=True, help_text='AI forecast metadata for this service', null=True),
        ),
        migrations.AddField(
            model_name='shopservicetimeslotmodel',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Creation timestamp'),
        ),
        migrations.AlterField(
            model_name='servicebookingdetailsmodel',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, help_text='Creation timestamp'),
        ),
        migrations.AlterField(
            model_name='servicebookingdetailsmodel',
            name='final_amount',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='servicebookingdetailsmodel',
            name='price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='servicebookingdetailsmodel',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to='shopServiceApp.shopservicedetailsmodel'),
        ),
        migrations.AlterField(
            model_name='servicebookingdetailsmodel',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bookings', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='servicebookingdiscountcouponsmodel',
            name='apply_to_all_services',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='servicebookingdiscountcouponsmodel',
            name='code',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='servicebookingdiscountcouponsmodel',
            name='discount_value',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='servicebookingdiscountcouponsmodel',
            name='max_usage',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='servicebookingdiscountcouponsmodel',
            name='services',
            field=models.ManyToManyField(blank=True, related_name='eligible_coupons', to='shopServiceApp.shopservicedetailsmodel'),
        ),
        migrations.AlterField(
            model_name='servicebookingdiscountcouponsmodel',
            name='shop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='discount_coupons', to='shopApp.shopdetailsmodel'),
        ),
        migrations.AlterField(
            model_name='shopservicedetailsmodel',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='services', to='shopServiceApp.shopservicecategorymodel'),
        ),
        migrations.AlterField(
            model_name='shopservicedetailsmodel',
            name='description',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='shopservicedetailsmodel',
            name='duration',
            field=models.DurationField(default=datetime.timedelta(0), help_text='Duration of service'),
        ),
        migrations.AlterField(
            model_name='shopservicedetailsmodel',
            name='name_arabic',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AlterField(
            model_name='shopservicedetailsmodel',
            name='specialists',
            field=models.ManyToManyField(blank=True, related_name='services_assigned', to='shopApp.shopspecialistdetailsmodel'),
        ),
        migrations.AlterField(
            model_name='shopservicegallerymodel',
            name='service',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gallery', to='shopServiceApp.shopservicedetailsmodel'),
        ),
    ]
