# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-30 07:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0011_auto_20151230_0735'),
    ]

    operations = [
        migrations.AddField(
            model_name='submit',
            name='user_id',
            field=models.IntegerField(null=True),
        ),
    ]
