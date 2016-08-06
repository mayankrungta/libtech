# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-23 16:51
from __future__ import unicode_literals

import broadcasts.models
import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('broadcasts', '0005_auto_20160720_0414'),
    ]

    operations = [
        migrations.AlterField(
            model_name='broadcast',
            name='media',
            field=models.FileField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/Users/mayank/Desktop/libtech.info/CDN/protected'), upload_to=broadcasts.models.download_media_location),
        ),
    ]