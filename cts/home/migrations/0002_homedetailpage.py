# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-05-24 05:48
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import wagtail.wagtailcore.blocks
import wagtail.wagtailcore.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0033_remove_golive_expiry_help_text'),
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HomeDetailPage',
            fields=[
                ('page_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='wagtailcore.Page')),
                ('content', wagtail.wagtailcore.fields.StreamField((('heading', wagtail.wagtailcore.blocks.CharBlock(classname='text-center')), ('motto', wagtail.wagtailcore.blocks.CharBlock(classname='subtitle')), ('paragraph', wagtail.wagtailcore.blocks.RichTextBlock())), blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=('wagtailcore.page',),
        ),
    ]
