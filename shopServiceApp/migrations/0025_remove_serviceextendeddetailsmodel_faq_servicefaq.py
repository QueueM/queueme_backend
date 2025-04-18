# Generated by Django 5.1.4 on 2025-04-10 14:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopServiceApp', '0024_remove_serviceextendeddetailsmodel_overview_image_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceextendeddetailsmodel',
            name='faq',
        ),
        migrations.CreateModel(
            name='ServiceFAQ',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.CharField(help_text='The FAQ question', max_length=300)),
                ('answer', models.TextField(help_text='The answer to the FAQ question')),
                ('order_index', models.PositiveIntegerField(default=0, help_text='Order index for display')),
                ('extended_details', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='faqs', to='shopServiceApp.serviceextendeddetailsmodel', verbose_name='Extended Details')),
            ],
            options={
                'verbose_name': 'Service FAQ',
                'verbose_name_plural': 'Service FAQs',
                'ordering': ['order_index'],
            },
        ),
    ]
