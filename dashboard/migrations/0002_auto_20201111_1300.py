# Generated by Django 3.1.3 on 2020-11-11 20:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='device_id',
            field=models.CharField(blank=True, max_length=32),
        ),
        migrations.AddField(
            model_name='device',
            name='hostname',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
