# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-19 11:02
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Forecast', '0005_auto_20170919_1539'),
    ]

    operations = [
        migrations.AddField(
            model_name='r_userinfo_action',
            name='isPass',
            field=models.BooleanField(default=False),
        ),
    ]