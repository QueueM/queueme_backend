# reelsApp/migrations/0005_rename_analytics_to_json.py
from django.db import migrations

class Migration(migrations.Migration):

    dependencies = [
        ('reelsApp', '0004_merge_20250412_0138'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reelsmodel',
            old_name='analytics_data_temp',
            new_name='analytics_data',
        ),
    ]
