# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-01-27 15:57
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logins', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=14),
        ),
    ]