# Generated by Django 5.1.4 on 2025-04-08 14:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeApp', '0007_remove_employeerolemanangementmodel_can_add_bookings_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_add_bookings',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_add_chat',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_add_customers',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_add_employees',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_add_marketing_ads',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_add_reels',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_add_roles',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_add_services',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_add_specialists',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_add_stories',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_delete_bookings',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_delete_chat',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_delete_customers',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_delete_employees',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_delete_marketing_ads',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_delete_reels',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_delete_roles',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_delete_services',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_delete_specialists',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_delete_stories',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_edit_bookings',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_edit_chat',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_edit_customers',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_edit_employees',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_edit_marketing_ads',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_edit_reels',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_edit_roles',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_edit_services',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_edit_specialists',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_edit_stories',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_view_bookings',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_view_chat',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_view_customers',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_view_employees',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_view_marketing_ads',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_view_reels',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_view_roles',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_view_services',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_view_specialists',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='can_view_stories',
            field=models.BooleanField(default=True),
        ),
    ]
