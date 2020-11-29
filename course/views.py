# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.shortcuts import render
from login import log_in
from lxml import etree
from .forms import UserForm, RegisterForm
from course import models
import requests
headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
host='http://210.42.121.134/'


def get_course(id,  passwd):
    while True:
        res,s = log_in(id, passwd)
        if res.url != 'http://210.42.121.134/servlet/Login':
            return 1,res,s
        else:
            if res.text.find('验证码错误') == -1:
                break
    return 0,0,0


def zhuanhuan(input):
    input=input.replace('\n','').replace(' ','')
    output = ''
    if input == 'Mon':
        output = str(1)
    elif input == 'Tue':
        output = str(2)
    elif input == 'Wed':
        output = str(3)
    elif input == 'Thu':
        output = str(4)
    elif input == 'Fir':
        output = str(5)
    elif input == 'Sat':
        output = str(6)
    elif input == 'Sun':
        output = str(7)
    return output

def get_myinf(username):
    user_inf = models.my_course.objects.filter(username=username)
    course = []
    for c in user_inf:
        t = [c.c_name, c.c_teacher, c.c_weekday, c.c_begin_week, c.c_end_week, c.c_f, c.c_begin_time, c.c_end_time,
             c.c_part, c.c_teach_building]
        course.append(t)
    return course



def class_table(response):
    response.encoding = response.apparent_encoding
    html = etree.HTML(response.text)
    # 这里得到一个表格内tr的集合
    trArr = html.xpath("/html/body/table/tr")
    b = []
    for tr in trArr:
        lessonName = tr.xpath("normalize-space(./td[2]/text())")
        teacherName = tr.xpath("normalize-space(./td[6]/text())")
        time_and_place = tr.xpath("normalize-space(./td[10]/div/text())")

        time_and_place = time_and_place.replace(":", ",").replace(";", ",")
        time_and_place = time_and_place.split(",")
        if (len(time_and_place) != 6):
            for i in range(6 - len(time_and_place)):
                time_and_place.append('')
        Day = time_and_place[0]
        Day = zhuanhuan(Day)
        #print(Day)
        #Week = time_and_place[1]
        Week = time_and_place[1].replace("周","").split("-")
        if (len(Week) == 1):
            Week = ['', '']
        WeekBegin = Week[0]
        WeekEnd = Week[1]
        WeekFrequency = time_and_place[2].replace("每","").replace("周","")
        time = time_and_place[3].replace("节","").split("-")
        if(len(time)==1):
            time = ['','']
        begin = time[0]
        end = time[1]
        region = time_and_place[4].replace("区","").replace("国软","3")

        classroom = time_and_place[5]
        buiding_classroom = time_and_place[4] + time_and_place[5]
        # print(Day)
        t = [lessonName, teacherName, Day, WeekBegin, WeekEnd, WeekFrequency, begin, end, region, classroom]
        for i in range(len(t)):
            if t[i] == "":
                t[i] = "0"
        b.append(t)
        # print(t)
    b = b[1:]
    #print(b)
    return b

# Create your views here.
def login(request):
    pass

    if request.method=='POST':
        login_form = UserForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
        user_exist=models.users.objects.filter(username=username)
        if not user_exist:
            temp,res,s=get_course(username,password)
            if temp==1:
                html = etree.HTML(res.text)
                name = html.xpath('//*[@id="nameLable"]/text()')
                url= html.xpath('//*[@id="hidUrl"]/@value')
                h=s.get(host+url[0])
                h=s.get('http://210.42.121.134'+url[0].replace('action=queryStuLsn','')+'&action=normalLsn&year=2019&term=1&state=')
                course = class_table(h)
                html = etree.HTML(h.text)
                message=name[0]
                resp=s.get('http://210.42.121.134/stu/student_information.jsp')
                html = etree.HTML(resp.text)
                result = html.xpath('/html/body/table/tr[8]/td[2]/img/@src')
                try:
                    img =s.get(result[0])
                    f = open('./static/pic/'+username+'.jpg','ab') #存储图片，多媒体文件需要参数b（二进制文件）
                    f.write(img.content) #多媒体存储content
                    f.close()
                except:
                    print('error')
                #course=html.xpath('/html/body/div[3]/div/text()')
                user_inf=models.users()
                user_inf.username=username
                user_inf.password=password
                user_inf.name=name[0]
                user_inf.save()
                for item in course:
                    print(item)
                    c=models.my_course()
                    c.username=username
                    c.c_name=item[0]
                    c.c_teacher=item[1]
                    c.c_weekday=int(item[2])
                    c.c_begin_week=int(item[3])
                    c.c_end_week=int(item[4])
                    c.c_f=int(item[5])
                    c.c_begin_time=int(item[6])
                    c.c_end_time=int(item[7])
                    c.c_part=int(item[8])
                    c.c_teach_building=item[9]
                    c.save()

                login_form = UserForm()
                r=render(request,'login/index.html',locals())
                r.set_cookie('username',username,max_age=1000)
                return r
            else:
                message='密码错误'

                return render(request, 'login/login.html', locals())
        else:
            user_inf = models.my_course.objects.filter(username=username)
            username=user_exist[0].username
            if user_exist[0].password!= password:
                 message='密码错误'
                 login_form = UserForm()
                 return render(request, 'login/login.html', locals())
            message=user_exist[0].name
            course=get_myinf(username)
            login_form = UserForm()
            r = render(request, 'login/index.html', locals())
            r.set_cookie('username', username, max_age=1000)
            return r


    login_form = UserForm()
    return render(request, 'login/login.html', locals())


def index(request):
    username = request.COOKIES.get('username')
    if username:
        user_exist=models.users.objects.filter(username=username)
        message = user_exist[0].name
        course=get_myinf(username)
    else:
        username='default'
        message='匿名用户'
    return render(request, 'login/index.html',locals())


def register(request):
    pass

def search(request):

    pass


def logout(request):
    r=render(request, 'login/login.html', locals())
    r.delete_cookie('username')
    return r

def talk(request):


    c_id=request.GET['c_id']
    talk=models.talk_inf.objects.filter(c_id=c_id).order_by("-time")
    res=[]
    for item in talk:
        if item.nick==0:
            res.append([item.stu_num,item.inf,item.talk_time])
        else:
            res.append(['匿名',item.inf])
    return render(request,'login/index.html',{'res':res})
    pass