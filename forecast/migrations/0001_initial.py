# Generated by Django 3.0.3 on 2020-02-13 21:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cities',
            fields=[
                ('name', models.CharField(max_length=50, primary_key=True, serialize=False, unique=True)),
            ],
            options={
                'verbose_name_plural': 'Cities',
            },
        ),
        migrations.CreateModel(
            name='Forecast',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('humidity', models.FloatField()),
                ('pressure', models.FloatField()),
                ('temperature', models.FloatField()),
                ('forecast_for', models.IntegerField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forecast.Cities')),
            ],
        ),
    ]
