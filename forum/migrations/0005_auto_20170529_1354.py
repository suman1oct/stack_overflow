# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-05-29 08:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0004_auto_20170529_1324'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answer',
            name='ans_description',
            field=models.CharField(max_length=5000, verbose_name='Answer'),
        ),
        migrations.AlterField(
            model_name='question',
            name='ques_description',
            field=models.CharField(max_length=5000, verbose_name='Question'),
        ),
        migrations.AlterField(
            model_name='question',
            name='ques_title',
            field=models.CharField(max_length=500, verbose_name='Question Title'),
        ),
    ]
