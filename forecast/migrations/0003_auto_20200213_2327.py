# Generated by Django 3.0.3 on 2020-02-13 23:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forecast', '0002_auto_20200213_2145'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forecast',
            name='forecast_for',
            field=models.BigIntegerField(),
        ),
    ]
