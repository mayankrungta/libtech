# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-13 06:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workdetails', '0003_auto_20160713_0358'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workdetail',
            name='rejection_reason',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
