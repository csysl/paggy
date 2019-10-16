# -*- coding: utf-8 -*-
'''
    @project:paggy
    @file:main.py
    @ide:PyCharm
    @time:2019-10-16 10:54
    @author:Sun
    @todo:
    @ref:
'''
import cv2
import init
from encrytion.encrypt import Encryption
from denoising.USER import USER
from denoising.CS1 import CS1

# todo 读取图片
# img = io.imread(init.imagepath)  # length*width*(r,g,b)
img = cv2.imread(init.imagepath, cv2.IMREAD_GRAYSCALE)

# TP为密钥生成器并生成密钥
TP=Encryption(init.M,init.bits)
TP.gainParam()  #生成密钥和参数

# user产生加密图像
user=USER(image=img,TP=TP)
enctyptImage=user.encrypt()

# cs1得到加密图像，产生加密后的距离
cs1=CS1(encryptImage=enctyptImage,TP=TP)


user.decrypt(enctyptImage)
