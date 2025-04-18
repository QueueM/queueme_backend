# Generated by Django 5.1.4 on 2024-12-26 08:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companyApp', '0002_companyemployeedetailsmodel'),
        ('shopApp', '0003_shopdetailsmodel_address_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='companydetailsmodel',
            name='address',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companydetailsmodel',
            name='company_image',
            field=models.ImageField(default='', upload_to='images/companylogo'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companydetailsmodel',
            name='description',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companydetailsmodel',
            name='is_verified',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companydetailsmodel',
            name='status',
            field=models.CharField(choices=[('accepted', 'Accepted'), ('Rejected', 'Rejected'), ('created', 'created')], default='created', max_length=30),
        ),
        migrations.AddField(
            model_name='companyemployeedetailsmodel',
            name='designation',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companyemployeedetailsmodel',
            name='phone_number',
            field=models.CharField(default='', max_length=30),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='companyemployeedetailsmodel',
            name='salary',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='CompanyEmployeeRoleManagementModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('can_create_product', models.BooleanField(default=False)),
                ('can_edit_product', models.BooleanField(default=False)),
                ('can_list_product', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='companyApp.companyemployeedetailsmodel')),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopApp.shopdetailsmodel')),
            ],
        ),
    ]
