# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-26 02:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skycast_app', '0006_auto_20171225_0345'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='search',
            name='zip',
        ),
        migrations.AddField(
            model_name='search',
            name='locationFriendlyName',
            field=models.CharField(default='lombard', max_length=200),
            preserve_default=False,
        ),
    ]
