# Generated by Django 2.2.7 on 2019-12-08 03:11

import backend.main.models
from django.db import migrations
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20191206_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='analysis',
            name='timeseries',
            field=djongo.models.fields.ArrayModelField(model_container=backend.main.models.DataPoint),
        ),
    ]
