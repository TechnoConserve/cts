# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-08-18 22:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='corporatemember',
            old_name='django_usage',
            new_name='cts_usage',
        ),
    ]
