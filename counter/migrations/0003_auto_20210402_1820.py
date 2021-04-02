# Generated by Django 3.1.7 on 2021-04-02 18:20

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counter', '0002_remove_services_notes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='typeofwork',
            name='fix_percent',
            field=models.IntegerField(null=True, validators=[django.core.validators.MinValueValidator(limit_value=1, message='Процент должен быть больше нуля')], verbose_name='Процент от услуги'),
        ),
    ]