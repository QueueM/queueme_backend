# companyApp/migrations/0012_alter_companydetailsmodel_forecast_data.py

from django.db import migrations, models
from django.core.serializers.json import DjangoJSONEncoder

class Migration(migrations.Migration):

    dependencies = [
        ('companyApp', '0011_alter_companydetailsmodel_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companydetailsmodel',
            name='forecast_data',
            field=models.JSONField(
                encoder=DjangoJSONEncoder,
                default=dict,
                null=True,
                blank=True,
                help_text='AI forecast metadata (will JSON‑encode datetimes/timestamps)'
            ),
        ),
    ]

