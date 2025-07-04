# Generated by Django 5.2 on 2025-06-11 12:10

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0021_rename_slots_resourceplan_total_slots_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='manufactureplanitem',
            name='average_time',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AddField(
            model_name='manufactureplanitem',
            name='resource_plan',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='resource_plan_items', to='api.resourceplan'),
        ),
        migrations.AddField(
            model_name='manufactureplanitem',
            name='used_slots',
            field=models.DecimalField(decimal_places=3, default=0, max_digits=15),
        ),
        migrations.DeleteModel(
            name='ResoucePlanItem',
        ),
    ]
