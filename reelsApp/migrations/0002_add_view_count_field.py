# reelsApp/migrations/0002_alter_analytics_to_json.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('reelsApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reelsmodel',
            name='analytics_data',
            field=models.JSONField(blank=True, null=True, default=dict),
        ),
    ]
