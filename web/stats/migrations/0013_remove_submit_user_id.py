# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2015-12-30 07:51
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0012_submit_user_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submit',
            name='user_id',
        ),
    ]