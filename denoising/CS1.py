# -*- coding: utf-8 -*-
'''
    @project:paggy
    @file:CS1.py
    @ide:PyCharm
    @time:2019-10-16 11:33
    @author:Sun
    @todo:
    @ref:
'''

import copy
import random
import time
from Cryptodome.Util import number as prime

from encrytion.encrypt import Encryption
from encrytion.mod import *
import init
from denoising.image import *


class CS1:
    def __init__(self, encryptImage, TP: 'Encryption'):
        # 图片
        self.__originEryptImage = encryptImage
        self.__length, self.__width = len(encryptImage), len(encryptImage)
        self.__size = self.__length * self.__width  # 像素个数
        self.__encryimage, self.__denoiseimage = None, None  # 存放对来自用户的图片加密后的图片和最后要返回给用户的图片

        # key
        self.__K, self.__invK, self.__Kcs, self.__invKcs = TP.cs1K
        self.__N = TP.N

    def encryptI(self):
        self.__encryimage = [[None] * self.__width for i in range(self.__length)]
        stime = time.time()
        for i in range(self.__length):
            for j in range(self.__width):
                self.__encryimage[i][j] = self.__encryption(self.__originEryptImage[i][j])
        etime = time.time()
        print('CS1对原图像加密时间是：%fs' % (etime - stime))

        # 加密密文

    def __encryption(self, plain):
        # stime = time.time()
        res = mul_matmod(self.__invK, plain, 4, self.__N)
        res = mul_matmod(res, self.__K, 4, self.__N)
        # etime = time.time()
        # print('加密的时间是：%fs' % (etime - stime))
        return res
