# Generated by Django 5.1.4 on 2025-02-17 12:31

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shopApp', '0010_alter_shopdetailsmodel_name_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='EmployeeDetailsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
                ('phone_number', models.CharField(max_length=200)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('avatar_image', models.ImageField(blank=True, null=True, upload_to='employee/avatar_image/')),
                ('is_active', models.BooleanField()),
                ('employee_id', models.CharField(editable=False, max_length=20, unique=True)),
                ('shop', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopApp.shopdetailsmodel')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EmployeeWorkingHoursModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('monday', 'Monday'), ('tuesday', 'Tuesday'), ('wednesday', 'Wednesday'), ('thursday', 'Thursday'), ('friday', 'Friday'), ('saturday', 'Saturday'), ('sunday', 'Sunday')], max_length=10)),
                ('start_time', models.TimeField()),
                ('end_time', models.TimeField()),
                ('is_closed', models.BooleanField(default=False)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='opening_hours', to='employeeApp.employeedetailsmodel')),
            ],
            options={
                'unique_together': {('employee', 'day')},
            },
        ),
    ]
