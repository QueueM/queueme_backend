# Generated by Django 5.1.4 on 2025-04-11 12:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adsApp', '0008_alter_shopadsmodel_image_alter_shopadsmodel_service_and_more'),
        ('shopServiceApp', '0027_remove_serviceextendeddetailsmodel_process_step_templates_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopadsmodel',
            name='budget_spent',
            field=models.DecimalField(decimal_places=2, default=0, help_text='Total budget spent on this ad', max_digits=10),
        ),
        migrations.AddField(
            model_name='shopadsmodel',
            name='creative_variants',
            field=models.JSONField(blank=True, help_text='Configurations of creative variants for A/B testing', null=True),
        ),
        migrations.AddField(
            model_name='shopadsmodel',
            name='dynamic_adjustments',
            field=models.JSONField(blank=True, help_text='Dynamic parameters adjusted by ML in real-time', null=True),
        ),
        migrations.AddField(
            model_name='shopadsmodel',
            name='frequency_cap',
            field=models.PositiveIntegerField(default=10, help_text='Max number of times a single user can view the ad per time window'),
        ),
        migrations.AddField(
            model_name='shopadsmodel',
            name='ml_model_id',
            field=models.CharField(blank=True, help_text='Identifier for the ML model used for creative optimization', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='shopadsmodel',
            name='ml_model_version',
            field=models.CharField(blank=True, help_text='Version of the ML model', max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='shopadsmodel',
            name='priority',
            field=models.PositiveIntegerField(default=0, help_text='Priority score for ad display order; higher values indicate higher priority'),
        ),
        migrations.AddField(
            model_name='shopadsmodel',
            name='time_window',
            field=models.DurationField(blank=True, help_text='Time window for frequency capping (e.g., 24 hours)', null=True),
        ),
        migrations.AddField(
            model_name='shopadsmodel',
            name='user_segmentation_data',
            field=models.JSONField(blank=True, help_text='Additional segmentation data for detailed targeting', null=True),
        ),
        migrations.AlterField(
            model_name='shopadsmodel',
            name='image',
            field=models.ImageField(null=True, upload_to='images/ads/cover'),
        ),
        migrations.AlterField(
            model_name='shopadsmodel',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopServiceApp.shopservicedetailsmodel'),
        ),
        migrations.DeleteModel(
            name='ShopAdsExtraFeaturesModel',
        ),
    ]
