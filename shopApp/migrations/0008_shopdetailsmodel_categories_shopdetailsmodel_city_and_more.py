# Generated by Django 5.1.4 on 2025-02-08 12:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0007_alter_shopdetailsmodel_avatar_image'),
        ('shopServiceApp', '0006_alter_servicebookingdetailsmodel_cancellation_reason_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shopdetailsmodel',
            name='categories',
            field=models.ManyToManyField(blank=True, null=True, related_name='shops', to='shopServiceApp.shopservicecategorymodel'),
        ),
        migrations.AddField(
            model_name='shopdetailsmodel',
            name='city',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AddField(
            model_name='shopdetailsmodel',
            name='country',
            field=models.CharField(blank=True, default='Saudi Arabia', max_length=80),
        ),
        migrations.AddField(
            model_name='shopdetailsmodel',
            name='customers_type',
            field=models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('both', 'Both')], default='both', max_length=300),
        ),
        migrations.AddField(
            model_name='shopdetailsmodel',
            name='district',
            field=models.CharField(blank=True, default='', max_length=300),
        ),
        migrations.AddField(
            model_name='shopdetailsmodel',
            name='services_types',
            field=models.CharField(choices=[('in_shop', 'In Shop'), ('at_home', 'At Home'), ('both', 'Both')], default='in_shop', max_length=300),
        ),
        migrations.AddField(
            model_name='shopdetailsmodel',
            name='shop_name',
            field=models.CharField(default='Shop Name', max_length=300),
        ),
        migrations.AddField(
            model_name='shopdetailsmodel',
            name='username',
            field=models.CharField(blank=True, default='', max_length=20),
        ),
        migrations.CreateModel(
            name='ShopOpeningHoursModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], max_length=10)),
                ('open_time', models.TimeField()),
                ('close_time', models.TimeField()),
                ('is_closed', models.BooleanField(default=False)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opening_hours', to='shopApp.shopdetailsmodel')),
            ],
            options={
                'unique_together': {('shop', 'day')},
            },
        ),
    ]
