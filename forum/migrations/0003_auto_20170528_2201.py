# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-28 16:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_auto_20170528_2200'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='ques_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]