# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-24 22:30
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('skycast_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='search',
            name='lat',
            field=models.DecimalField(decimal_places=50, max_digits=53),
        ),
        migrations.AlterField(
            model_name='search',
            name='long',
            field=models.DecimalField(decimal_places=50, max_digits=53),
        ),
    ]
