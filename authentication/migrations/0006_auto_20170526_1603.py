# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-26 10:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0005_auto_20170526_1557'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=1000, verbose_name='Address'),
        ),
    ]
