# Generated by Django 5.1.4 on 2025-04-09 14:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companyApp', '0013_alter_companydetailsmodel_company_image_and_more'),
        ('shopApp', '0016_shopdetailsmodel_ai_personalization'),
        ('shopDashboardApp', '0004_rename_total_ads_clicks_dashboardlog_total_ad_impressions_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dashboardlog',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AddField(
            model_name='dashboardlog',
            name='branch_name',
            field=models.CharField(blank=True, default='', help_text='Denormalized shop/branch name for this snapshot', max_length=300),
        ),
        migrations.AddField(
            model_name='dashboardlog',
            name='company_name',
            field=models.CharField(blank=True, default='', help_text='Denormalized company name for this snapshot', max_length=300),
        ),
        migrations.AlterField(
            model_name='dashboardlog',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_logs', to='companyApp.companydetailsmodel'),
        ),
        migrations.AlterField(
            model_name='dashboardlog',
            name='date_range',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='dashboardlog',
            name='estimated_wait_time',
            field=models.CharField(blank=True, default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='dashboardlog',
            name='shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='dashboard_logs', to='shopApp.shopdetailsmodel'),
        ),
        migrations.AlterField(
            model_name='dashboardlog',
            name='top_services',
            field=models.JSONField(blank=True, default=list, help_text='List of top services with booking counts', null=True),
        ),
    ]
