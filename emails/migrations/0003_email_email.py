# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0002_auto_20180620_2019'),
    ]

    operations = [
        migrations.AddField(
            model_name='email',
            name='email',
            field=models.EmailField(default=None, max_length=254),
            preserve_default=False,
        ),
    ]
