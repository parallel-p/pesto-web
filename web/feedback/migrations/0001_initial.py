# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-04 13:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=2016)),
                ('time', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
