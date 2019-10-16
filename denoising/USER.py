# -*- coding: utf-8 -*-
'''
    @project:paggy
    @file:USER.py
    @ide:PyCharm
    @time:2019-10-16 11:33
    @author:Sun
    @todo:
    @ref:
'''
import copy
import random

from encrytion.encrypt import Encryption
import init
from denoising.image import *


class USER:

    def __init__(self, image, TP: 'Encryption'):
        # 图像
        self.__image = copy.deepcopy(image)
        self.__length, self.__width = len(image), len(image[0])
        self.__size = self.__length * self.__width  # 像素个数

        self.__grayimage, self.__gaussgrayimage = None, None  # 原始灰度图,添加了gauss噪声的灰度图,进行局部均值去噪的扩充图
        self.__encryimage, self.__denoiseimage = None, None  # cs1处理后的图像和用户解密后的图像

        # 密钥
        self.__K, self.__invK = TP.userK
        self.__TP=TP

    def encrypt(self):
        # 获取灰度图
        self.__grayimage = copy.deepcopy(self.__image).tolist()
        imageshow(self.__grayimage, 'grayimage')  # 显示灰度图
        # 给灰度图添加高斯噪声
        self.__gaussgrayimage = self.__addgaussnoise()
        imageshow(self.__gaussgrayimage, 'gaussgrayimage')

    # todo 为灰度图添加高斯噪声
    def __addgaussnoise(self):
        res = [[0] * self.__width for i in range(self.__length)]
        for i in range(self.__length):
            for j in range(self.__width):
                res[i][j] = self.__grayimage[i][j] + int(
                    random.gauss(mu=0, sigma=init.sigma))
                if res[i][j] > 255:
                    res[i][j] = 255
                elif res[i][j] < 0:
                    res[i][j] = 0
        return res

    # todo 加密函数，对输入的图像加密
    def __encryptImage(self):
        self.__encryimage = [[None] * self.__width for i in range(self.__length)]
        for i in range(self.__length):
            for j in range(self.__width):
                self.__encryimage[i][j]=self.__TP.encryption(self.__gaussgrayimage[i][j])

    def __decryptImage(self,image):
        self.__denoiseimage=[[None] * self.__width for i in range(self.__length)]
        for i in range(self.__length):
            for j in range(self.__width):
                self.__encryimage[i][j]=self.__TP.decryption(image[i][j])
