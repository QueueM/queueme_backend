# Generated by Django 5.1.4 on 2025-02-17 11:21

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companyApp', '0007_alter_companydetailsmodel_company_registration_document'),
        ('shopApp', '0010_alter_shopdetailsmodel_name_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyemployeedetailsmodel',
            name='company',
        ),
        migrations.AddField(
            model_name='companyemployeedetailsmodel',
            name='shop',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shopApp.shopdetailsmodel'),
            preserve_default=False,
        ),
    ]
