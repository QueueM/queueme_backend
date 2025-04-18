# Generated by Django 5.1.4 on 2025-02-14 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0009_alter_shopdetailsmodel_avatar_image_and_more'),
        ('shopServiceApp', '0007_servicebookingdetailsmodel_customer_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shopservicedetailsmodel',
            name='time_slots',
        ),
        migrations.AlterField(
            model_name='shopservicedetailsmodel',
            name='specialists',
            field=models.ManyToManyField(blank=True, null=True, related_name='services_assigned', to='shopApp.shopspecialistdetailsmodel'),
        ),
    ]
