# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-06-20 10:19
from __future__ import unicode_literals

from django.db import migrations


groups = [
    'Group 1',
    'Group 2',
]

def create_emails_group(apps, schema_apps):
    model = apps.get_model('emails', 'GroupEmail')
    groups_objects = [model(name=item) for item in groups]
    model.objects.bulk_create(groups_objects)


class Migration(migrations.Migration):

    dependencies = [
        ('emails', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_emails_group)
    ]