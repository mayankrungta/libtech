# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-07-19 01:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addressbook', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='addressbook',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]