# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 09:07
from __future__ import unicode_literals

from django.db import migrations, models
import document.models


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0015_auto_20170730_0823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='document_files', validators=[document.models.validate_file_extension]),
        ),
    ]
