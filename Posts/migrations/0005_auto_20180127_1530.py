# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-27 15:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0004_auto_20180119_1158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image_1',
            field=models.ImageField(blank=True, upload_to=b'images/'),
        ),
    ]
