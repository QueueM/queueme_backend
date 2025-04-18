# Generated by Django 5.1.4 on 2025-04-11 20:00

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adsApp', '0011_remove_shopadsmodel_latitude_and_more'),
        ('shopServiceApp', '0027_remove_serviceextendeddetailsmodel_process_step_templates_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopadsmodel',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shopadsmodel',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='shopadsmodel',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='shopServiceApp.shopservicedetailsmodel'),
        ),
        migrations.AddField(
            model_name='shopadsmodel',
            name='target_gender',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('both', 'Both')], default='both', max_length=200),
        ),
        migrations.AlterField(
            model_name='shopadsmodel',
            name='image',
            field=models.ImageField(null=True, upload_to='images/ads/cover'),
        ),
        migrations.DeleteModel(
            name='AdsPayment',
        ),
    ]
