# Generated by Django 5.2 on 2025-04-22 12:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='fabric',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='productblueprint',
            name='updated',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
