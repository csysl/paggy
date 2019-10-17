# -*- coding: utf-8 -*-
'''
    @project:paggy
    @file:CS.py
    @ide:PyCharm
    @time:2019-10-17 16:24
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


class CS:
    def __init__(self, encryptImage, TP: 'Encryption'):
        # 图片
        self.__originEryptImage = encryptImage
        self.__length, self.__width = len(encryptImage), len(encryptImage)
        self.__size = self.__length * self.__width  # 像素个数
        self.__encryimage, self.__padimage, self.__denoiseimage = None, None, None  # 存放对来自用户的图片加密后的图片和最后要返回给用户的图片

        # key for cs1
        self.__K1, self.__invK1, self.__Kcs1, self.__invKcs1 = TP.cs1K
        # key for cs2
        self.__Kcs2, self.__invKcs2 = TP.cs2K
        self.__N = TP.N

        # test
        self.__testK, self.__testinvK = TP.K

    # 对用户发送的图片进行加密，加密后等同于对图像I使用k加密
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
        res = mul_matmod(self.__invK1, plain, 4, self.__N)
        res = mul_matmod(res, self.__K1, 4, self.__N)
        # etime = time.time()
        # print('加密的时间是：%fs' % (etime - stime))
        return res

    # 将加密的图片进行扩充
    def __gainPadImage(self):
        pass

    # TODO 去噪，计算距离，上传距离，计算去噪参数，返回参数，使用参数去噪，全部在这一步执行
    def NLmean(self):
        pass




    """以下用做测试"""

    def testdecryption(self):
        self.__decryptImage(self.__encryimage)

    # 解密
    def __decryption(self, cipher):
        # stime = time.time()
        for i in range(len(cipher)):
            for j in range(len(cipher[0])):
                cipher[i][j] %= self.__N

        res = mul_matmod(self.__testK, cipher, 4, self.__N)
        res = mul_matmod(res, self.__testinvK, 4, self.__N)
        # etime = time.time()
        # print('解密的时间是：%fs' % (etime - stime))
        return res[0][0]

    # todo 解密函数，对服务器返回的图像解密
    def __decryptImage(self, image):
        stime = time.time()
        self.__denoiseimage = [[None] * self.__width for i in range(self.__length)]
        for i in range(self.__length):
            for j in range(self.__width):
                self.__denoiseimage[i][j] = self.__decryption(image[i][j])
        etime = time.time()
        print('用户解密时间是：%fs' % (etime - stime))
        imageshow(self.__denoiseimage,'测试结果')

    """以上用做测试"""