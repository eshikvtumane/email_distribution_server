# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-22 06:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('logger', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='emailsenderlogger',
            name='result',
            field=models.TextField(default=''),
            preserve_default=False,
        ),
    ]
