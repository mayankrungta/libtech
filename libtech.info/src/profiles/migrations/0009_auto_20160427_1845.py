# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-04-27 18:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_auto_20160427_1843'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='last_name',
        ),
        migrations.AlterField(
            model_name='profile',
            name='name',
            field=models.CharField(max_length=1200),
        ),
    ]
