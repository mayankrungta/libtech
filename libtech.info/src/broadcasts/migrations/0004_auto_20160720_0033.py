# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-19 19:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broadcasts', '0003_broadcast_start_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broadcast',
            name='start_time',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
