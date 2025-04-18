# Generated by Django 5.1.4 on 2025-03-18 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employeeApp', '0004_alter_employeedetailsmodel_phone_number_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='employeerolemanangementmodel',
            unique_together=set(),
        ),
        migrations.AddField(
            model_name='employeerolemanangementmodel',
            name='employees',
            field=models.ManyToManyField(related_name='roles', to='employeeApp.employeedetailsmodel'),
        ),
        migrations.RemoveField(
            model_name='employeerolemanangementmodel',
            name='employee',
        ),
    ]
