# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-03 11:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('doreshka', '0003_userresult_rj'),
    ]

    operations = [
        migrations.AddField(
            model_name='userresult',
            name='pf',
            field=models.IntegerField(null=True),
        ),
    ]
