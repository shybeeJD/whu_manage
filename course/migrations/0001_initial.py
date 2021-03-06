# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-11-21 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='my_course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('c_name', models.CharField(max_length=80)),
                ('c_teacher', models.CharField(max_length=16)),
                ('c_weekday', models.IntegerField()),
                ('c_begin_week', models.IntegerField()),
                ('c_end_week', models.IntegerField()),
                ('c_f', models.IntegerField()),
                ('c_begin_time', models.IntegerField()),
                ('c_end_time', models.IntegerField()),
                ('c_part', models.IntegerField(null=True)),
                ('c_teach_building', models.IntegerField(null=True)),
                ('c_note', models.CharField(max_length=60, null=True)),
            ],
            options={
                'verbose_name': '课程信息',
                'verbose_name_plural': '课程信息',
                'ordering': ['c_name'],
            },
        ),
        migrations.CreateModel(
            name='pub_class_scores',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('c_mean_scores', models.FloatField(max_length=10)),
                ('c_stu_num', models.IntegerField()),
                ('c_06', models.IntegerField()),
                ('c_67', models.IntegerField()),
                ('c_78', models.IntegerField()),
                ('c_89', models.IntegerField()),
                ('c_910', models.IntegerField()),
            ],
            options={
                'verbose_name': '公选给分信息',
                'verbose_name_plural': '公选给分信息',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='public_course_inf',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('c_name', models.CharField(max_length=80, null=True)),
                ('c_teacher', models.CharField(max_length=16)),
                ('c_credit', models.IntegerField()),
                ('c_max_stu', models.IntegerField()),
                ('c_left_stu', models.IntegerField(null=True)),
                ('c_teacher_title', models.CharField(max_length=5, null=True)),
                ('c_school', models.CharField(max_length=10, null=True)),
                ('c_type', models.IntegerField()),
                ('c_weekday', models.IntegerField()),
                ('c_begin_week', models.IntegerField()),
                ('c_end_week', models.IntegerField()),
                ('c_f', models.IntegerField()),
                ('c_begin_time', models.IntegerField()),
                ('c_end_time', models.IntegerField()),
                ('c_part', models.IntegerField(null=True)),
                ('c_teach_building', models.CharField(max_length=20)),
                ('c_note', models.CharField(max_length=60, null=True)),
            ],
            options={
                'verbose_name': '公选课程信息',
                'verbose_name_plural': '公选课程信息',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='share_file',
            fields=[
                ('c_id', models.IntegerField(primary_key=True, serialize=False)),
                ('src', models.CharField(max_length=80)),
            ],
            options={
                'verbose_name': '文件记录',
                'verbose_name_plural': '文件记录',
                'ordering': ['c_id'],
            },
        ),
        migrations.CreateModel(
            name='talk_inf',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stu_num', models.IntegerField()),
                ('c_id', models.IntegerField()),
                ('inf', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': '聊天记录',
                'verbose_name_plural': '聊天记录',
            },
        ),
        migrations.CreateModel(
            name='users',
            fields=[
                ('username', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=40)),
                ('name', models.CharField(max_length=20)),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
                'ordering': ['username'],
            },
        ),
    ]
