# Generated by Django 5.1.4 on 2025-04-11 19:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adsApp', '0010_remove_shopadsmodel_budget_spent_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopadsmodel',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='shopadsmodel',
            name='longitude',
        ),
        migrations.RemoveField(
            model_name='shopadsmodel',
            name='service',
        ),
        migrations.RemoveField(
            model_name='shopadsmodel',
            name='target_gender',
        ),
        migrations.AlterField(
            model_name='shopadsmodel',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/ads/cover'),
        ),
        migrations.CreateModel(
            name='AdsPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=255, unique=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('status', models.CharField(max_length=255)),
                ('payment_type', models.CharField(choices=[('p', 'Payment')], default='p', max_length=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payments', to='adsApp.shopadsmodel')),
            ],
        ),
    ]
