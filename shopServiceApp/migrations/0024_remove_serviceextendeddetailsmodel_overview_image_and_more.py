# Generated by Django 5.1.4 on 2025-04-10 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopServiceApp', '0023_remove_serviceextendeddetailsmodel_aftercare_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceextendeddetailsmodel',
            name='overview_image',
        ),
        migrations.RemoveField(
            model_name='serviceextendeddetailsmodel',
            name='overview_title',
        ),
        migrations.AlterField(
            model_name='serviceprocessstep',
            name='title',
            field=models.CharField(help_text='Title of the process step', max_length=200),
        ),
        migrations.CreateModel(
            name='ServiceOverview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(help_text='Title of the overview item', max_length=200)),
                ('image', models.ImageField(blank=True, help_text='Optional image for the overview item', null=True, upload_to='service_overview/')),
                ('description', models.TextField(blank=True, help_text='Optional description for the overview item')),
                ('order_index', models.PositiveIntegerField(default=0, help_text='Order index for display')),
                ('extended_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='overviews', to='shopServiceApp.serviceextendeddetailsmodel', verbose_name='Extended Details')),
            ],
            options={
                'verbose_name': 'Service Overview',
                'verbose_name_plural': 'Service Overviews',
                'ordering': ['order_index'],
            },
        ),
    ]
