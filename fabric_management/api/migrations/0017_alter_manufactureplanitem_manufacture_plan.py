# Generated by Django 5.2 on 2025-06-10 12:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0016_saleplace_manufactureplanitem_status_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufactureplanitem',
            name='manufacture_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='api.manufactureplan'),
        ),
    ]
