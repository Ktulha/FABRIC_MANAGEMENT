# Generated by Django 5.2 on 2025-06-10 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0013_alter_manufactureplan_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='product_name',
            field=models.CharField(max_length=255, null=True, unique=True),
        ),
    ]
