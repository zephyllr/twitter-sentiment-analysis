# Generated by Django 2.2.7 on 2019-12-06 15:42

import backend.main.models
from django.db import migrations, models
import djongo.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription',
            name='checked_since',
            field=models.IntegerField(default=0),
            preserve_default=False,
        )
    ]