


#利用训练模型爆破珞珈体育网
#保存至inf.txt
#在des.txt设置起始学号








import sys, os
from PIL import Image, ImageDraw
import queue
import os,time


import cv2
import pandas as pd

a=[0,1,2,3]
t2val = {}
def cfs(img):
    """传入二值化后的图片进行连通域分割"""
    pixdata = img.load()
    w,h = img.size
    visited = set()
    q = queue.Queue()
    offset = [(-1,-1),(0,-1),(1,-1),(-1,0),(1,0),(-1,1),(0,1),(1,1)]
    x_cuts = []
    y_cuts = []
    for x in range(w):
        for y in range(h):
            x_axis = []
            y_axis = []
            if pixdata[x,y] == 0 and (x,y) not in visited:
                q.put((x,y))
                visited.add((x,y))
            while not q.empty():
                x_p,y_p = q.get()
                for x_offset,y_offset in offset:
                    x_c,y_c = x_p+x_offset,y_p+y_offset
                    if (x_c,y_c) in visited:
                        continue
                    visited.add((x_c,y_c))
                    try:
                        if pixdata[x_c,y_c] == 0:
                            q.put((x_c,y_c))
                            x_axis.append(x_c)
                            y_axis.append(y_c)
                            #y_axis.append(y_c)
                    except:
                        pass
            if x_axis:
                min_x,max_x = min(x_axis),max(x_axis)
                min_y,max_y = min(y_axis),max(y_axis)
                if max_x - min_x >  3:
                    # 宽度小于3的认为是噪点，根据需要修改
                    x_cuts.append((min_x,max_x + 1))
                    y_cuts.append((min_y,max_y + 1))
    return x_cuts,y_cuts





def clearNoise(image, N, Z):
    for i in range(0, Z):
        t2val[(0, 0)] = 1
        t2val[(image.size[0] - 1, image.size[1] - 1)] = 1

        for x in range(1, image.size[0] - 1):
            for y in range(1, image.size[1] - 1):
                nearDots = 0
                L = t2val[(x, y)]
                if L == t2val[(x - 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x - 1, y)]:
                    nearDots += 1
                if L == t2val[(x - 1, y + 1)]:
                    nearDots += 1
                if L == t2val[(x, y - 1)]:
                    nearDots += 1
                if L == t2val[(x, y + 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y - 1)]:
                    nearDots += 1
                if L == t2val[(x + 1, y)]:
                    nearDots += 1
                if L == t2val[(x + 1, y + 1)]:
                    nearDots += 1

                if nearDots < N:
                    t2val[(x, y)] = 1



def saveSmall(img, x_cuts,y_cuts):
    w, h = img.size
    pixdata = img.load()
    for j, item in enumerate(x_cuts):
        if j<4:
            box = (item[0], 0, item[1], 30)
            a[j]=img.crop(box)
            img.crop(box).save('./temp/'+str(j)+'.png')
            #print(box)
            #img.crop(box).save(outDir+file[j]+'/' + str(i)+'-'+str(j) + ".png")

def twoValue(image, G):
    for y in range(0, image.size[1]):
        for x in range(0, image.size[0]):
            g = image.getpixel((x, y))
            if g > G:
                t2val[(x, y)] = 1
            else:
                t2val[(x, y)] = 0


def saveImage(size):
    image = Image.new("1", size)
    draw = ImageDraw.Draw(image)

    for x in range(0, size[0]):
        for y in range(0, size[1]):
            draw.point((x, y), t2val[(x, y)])

    return image

# rename and convert to 16*20 size
def convert(dir, file):

    imagepath = dir+'/'+file
    # 读取图片
    image = cv2.imread(imagepath, 0)
    # 二值化
    ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    img = cv2.resize(thresh, (16, 20), interpolation=cv2.INTER_AREA)
    # 保存图片
    cv2.imwrite('%s/%s' % (dir, file), img)

# 读取图片的数据，并转化为0-1值
def Read_Data(dir, file):

    imagepath = dir+'/'+file
    # 读取图片
    image = cv2.imread(imagepath, 0)
    # 二值化
    ret, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
    # 显示图片
    bin_values = [1 if pixel==255 else 0 for pixel in thresh.ravel()]

    return bin_values





def log_inn(cnn):
    
    image = Image.open('valcode.png').convert("L")
    twoValue(image, 100)
    clearNoise(image, 1, 1)
    image=saveImage(image.size)
    x,y=cfs(image)
    saveSmall(image, x,y)
    prediction = ''
    labels = '0123456789abcdefghijklmnopqrstuvwxyz'
    for i in range(0,4):
        convert('./temp/', str(i)+'.png')
    table = [Read_Data('./temp/', str(file)+'.png') for file in range(0,4)]
    test_data = pd.DataFrame(table, columns=['v%d'%i for i in range(1,321)])

        
    y_pred = cnn.predict(test_data)

        # 预测分类
    for pred in y_pred:
        label = labels[list(pred).index(max(pred))]
        prediction=prediction+label
    if len(prediction)!=4:


        prediction='shit'
    #print(prediction)
    return prediction
    

def main(cnn):

    
    pre=log_inn(cnn)
    return pre

