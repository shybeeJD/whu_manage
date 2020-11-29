# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class public_course_inf(models.Model):
    id = models.AutoField(primary_key=True)#课程id
    c_name = models.CharField(max_length=80,null=True)  # 课程名
    c_teacher = models.CharField(max_length=16)  # 课程老师
    c_credit=models.IntegerField()#课程学分
    c_max_stu=models.IntegerField()#最大可选人数
    c_left_stu = models.IntegerField(null=True)  # 最大可选人数
    c_teacher_title=models.CharField(max_length=5,null=True)#教师职称
    c_school=models.CharField(max_length=10,null=True)#开课学院
    c_type=models.IntegerField()#课程类型
    c_weekday=models.IntegerField()#周几上课
    c_begin_week=models.IntegerField()#开始周
    c_end_week=models.IntegerField()#结束周
    c_f=models.IntegerField()#上课频率
    c_begin_time=models.IntegerField()#上课时间
    c_end_time=models.IntegerField()#下课时间
    c_part=models.IntegerField(null=True)#上课区域
    c_teach_building=models.CharField(max_length=20)#上课教学楼
    c_note=models.CharField(max_length=60,null=True)#备注



    def __str__(self):
        return str(self.id)

    class Meta:
        ordering=['id']
        verbose_name='公选课程信息'
        verbose_name_plural='公选课程信息'



class talk_inf(models.Model):
    stu_num=models.IntegerField()
    c_id=models.IntegerField()
    inf=models.CharField(max_length=200)
    nick=models.BooleanField(default=0)
    talk_time=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.id)

    class Meta:

        verbose_name = '聊天记录'
        verbose_name_plural = '聊天记录'

class share_file(models.Model):
    c_id=models.IntegerField(primary_key=True)
    src=models.CharField(max_length=80)

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ['c_id']
        verbose_name = '文件记录'
        verbose_name_plural = '文件记录'

class users(models.Model):
    username=models.CharField(max_length=20,primary_key=True)
    password=models.CharField(max_length=40)
    name=models.CharField(max_length=20)

    def __str__(self):
        return str(self.username)

    class Meta:
        ordering = ['username']
        verbose_name = '用户信息'
        verbose_name_plural = '用户信息'


class my_course(models.Model):
    username=models.CharField(max_length=20)
    c_name = models.CharField(max_length=80)  # 课程名
    c_teacher = models.CharField(max_length=16)  # 课程老师
    c_weekday = models.IntegerField()  # 周几上课
    c_begin_week = models.IntegerField()  # 开始周
    c_end_week = models.IntegerField()  # 结束周
    c_f = models.IntegerField()  # 上课频率
    c_begin_time = models.IntegerField()  # 上课时间
    c_end_time = models.IntegerField()  # 下课时间
    c_part = models.IntegerField(null=True)  # 上课区域
    c_teach_building = models.CharField(max_length=20)  # 上课教学楼
    c_note = models.CharField(max_length=60, null=True)  # 备注
    def __str__(self):
        return str(self.c_name)

    class Meta:
        ordering = ['c_name']
        verbose_name = '课程信息'
        verbose_name_plural = '课程信息'



class pub_class_scores(models.Model):
    id = models.IntegerField(primary_key=True)  # 课程id
    c_mean_scores = models.FloatField(max_length=10)  # 均分
    c_stu_num = models.IntegerField()  # 给分参考人数
    c_06 = models.IntegerField()  # 不及格人数
    c_67 = models.IntegerField()  # 60-70人数
    c_78 = models.IntegerField()  # 70-80人数
    c_89 = models.IntegerField()  # 80-90人数
    c_910 = models.IntegerField()  # 90+人数

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering=['id']
        verbose_name='公选给分信息'
        verbose_name_plural='公选给分信息'