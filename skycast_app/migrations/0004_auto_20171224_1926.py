# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-25 01:26
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('skycast_app', '0003_auto_20171224_1632'),
    ]

    operations = [
        migrations.RenameField(
            model_name='search',
            old_name='serch_date',
            new_name='search_date',
        ),
    ]
