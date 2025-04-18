# reelsApp/migrations/0003_add_analytics_text.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('reelsApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reelsmodel',
            name='analytics_data_temp',
            field=models.TextField(blank=True, null=True),
        ),
    ]
