# Generated by Django 5.1.4 on 2025-04-09 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopDashboardApp', '0010_dashboardlog_total_comments_per_reel_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dashboardlog',
            name='total_comments_per_reel',
            field=models.IntegerField(default=0),
        ),
    ]
