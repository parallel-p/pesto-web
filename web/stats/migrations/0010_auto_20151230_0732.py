# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-30 07:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0009_auto_20151230_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='problem',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
