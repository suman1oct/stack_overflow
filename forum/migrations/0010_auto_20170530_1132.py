# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-30 06:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0009_auto_20170529_1615'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='updated_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='question',
            name='has_answer',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='question',
            name='updated_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]