# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 07:14
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_auto_20170524_0700'),
    ]

    operations = [
        migrations.AddField(
            model_name='homepage',
            name='use_detail_template',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
    ]
