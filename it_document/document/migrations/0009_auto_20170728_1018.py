# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-28 03:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0008_auto_20170727_1350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, null=True, unique=True),
        ),
    ]
