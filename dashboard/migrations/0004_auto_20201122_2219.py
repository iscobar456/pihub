# Generated by Django 3.1.3 on 2020-11-23 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_auto_20201122_1952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='device',
            name='private_key',
            field=models.CharField(blank=True, max_length=64),
        ),
    ]
