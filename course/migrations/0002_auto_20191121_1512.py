# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-11-21 15:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='public_course_inf',
            name='c_teach_building',
            field=models.CharField(max_length=20),
        ),
    ]
