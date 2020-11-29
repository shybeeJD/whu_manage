import os
import datatest
import requests
from VerifyCodeCNN import CNN
import hashlib
import tensorflow as tf
codeurl = 'http://210.42.121.134/servlet/GenImg'
checkUrl = 'http://210.42.121.134/servlet/Login'

MODEL_SAVE_PATH = './data/model.ckpt'



# 代码的健壮性
def gethtml(checkurl, headers, cookies, data,s):
    i = 0
    while i < 10:
        try:
            html = s.post(checkUrl, headers=headers, cookies=cookies, data=data, timeout=0.3)
            return html,s
        except requests.exceptions.RequestException:
            i += 1


def getpic(headers,s):
    i = 0
    while i < 10:
        try:
            html = s.get(codeurl, headers=headers, verify=False, timeout=0.3)
            return html,s
        except requests.exceptions.RequestException:
            i += 1


def log_in(idnum, password):
    s = requests.Session()
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
    valcode,s = getpic(headers,s)
    f = open('valcode.png', 'wb')
    f.write(valcode.content)
    f.close()
    md5 = hashlib.md5(password.encode('utf-8')).hexdigest()
    tf.reset_default_graph()
    cnn = CNN(1000, 0.0005, MODEL_SAVE_PATH)
    code = datatest.main(cnn)
    data = {"id": idnum, "pwd": md5, "xdvfb": str(code)}
    resp,s = gethtml(checkUrl, headers, requests.utils.dict_from_cookiejar(valcode.cookies), data,s)
    # resp = requests.post(checkUrl, headers = headers, cookies = requests.utils.dict_from_cookiejar(valcode.cookies), data=data)

    return resp,s
