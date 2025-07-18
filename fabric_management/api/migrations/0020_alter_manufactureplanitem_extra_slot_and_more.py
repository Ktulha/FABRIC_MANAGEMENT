# Generated by Django 5.2 on 2025-06-11 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_alter_blueprint_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manufactureplanitem',
            name='extra_slot',
            field=models.PositiveIntegerField(default=0, null=True),
        ),
        migrations.AlterField(
            model_name='manufactureplanitem',
            name='priority',
            field=models.CharField(choices=[('low', 'НИЗКИЙ'), ('alarm', 'ТРЕВОГА'), ('high', 'ВЫСОКИЙ'), ('medium', 'СРЕДНИЙ'), ('sometime', 'ПОЗЖЕ')], default='medium', max_length=50),
        ),
        migrations.AlterField(
            model_name='manufactureplanitem',
            name='status',
            field=models.CharField(choices=[('pending', 'В ОЖИДАНИИ'), ('plan', 'ПЛАН'), ('production', 'ПРОИЗВОДСТВО'), ('completed', 'ЗАВЕРШЕНО'), ('failure', 'ОШИБКА')], default='pending', max_length=50),
        ),
        migrations.AlterField(
            model_name='saletransaction',
            name='operation',
            field=models.CharField(choices=[('sale', 'ПРОДАЖА'), ('return', 'ВОЗВРАТ')], default='sale', max_length=50),
        ),
    ]
