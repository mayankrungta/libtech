# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-18 23:11
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('broadcasts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='broadcast',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='broadcast',
            name='start_time',
        ),
    ]
