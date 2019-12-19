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
import time
# import numba
#from Crypto.Util import number as prime
from multiprocessing import cpu_count
import multiprocessing as mp

from encrytion.encrypt import Encryption
from encrytion.mod import *
import init
from denoising.image import *
from skimage.measure import compare_ssim


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
        self.__N, self.__M, self.__F = TP.N, TP.M, TP.F

        # 加解密
        self.__R = TP.R
        # self.__R = prime.getRandomRange(0, self.__N)  #todo R这里应该随机取还是和CS1取一样的R吗？不知道，先取成一致
        self.__A, self.__B, self.__C = [], [], []
        self.__a, self.__b, self.__c = -1, -1, -1
        self.__diag = [[0] * 4 for i in range(4)]  # 对角矩阵
        self.__SCAL = init.SCAL

        # self.__pro_num = 4#cpu_count()  # 获取cpu的线程数
        # print(self.__pro_num)

    # TODO 外部执行的加密函数
    # @numba.jit#(nopython=True)
    def encrypt(self):
        # 获取灰度图
        self.__grayimage = copy.deepcopy(self.__image).tolist()
        imageshow(self.__grayimage, 'grayimage')  # 显示灰度图
        # 给灰度图添加高斯噪声
        self.__gaussgrayimage = self.__addgaussnoise()
        imageshow(self.__gaussgrayimage, init.imagepath[4:], True)
        print('加噪图像和源图像的PSNR是：', calPSNR(self.__grayimage, self.__gaussgrayimage))
        # (score,diff)=compare_ssim(np.array(self.__grayimage),np.array(self.__gaussgrayimage),full=True)
        # print("加噪图像和源图像的SSIM是: {}".format(score))
        self.__encryptImage()
        return self.__encryimage[:]

    # TODO 外部执行的解密函数
    def decrypt(self, cipherimg):
        self.__decryptImage(cipherimg)
        imageshow(self.__denoiseimage, 're' + init.imagepath[4:], True)
        print('去噪图像和源图像的PSNR是：', calPSNR(self.__grayimage, self.__denoiseimage))
        # (score, diff) = compare_ssim(np.array(self.__grayimage), np.array(self.__denoiseimage), full=True)
        # print("去噪图像和源图像的SSIM是: {}".format(score))

    #

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

    # 加密密文
    def __encryption(self, plain):
        # stime = time.time()
        self.__gainABC(plain)
        self.__gainabc()
        self.__A.clear(), self.__B.clear(), self.__C.clear()  # 多像素加密时清空，因为产生ABC使用的是append方式
        self.__gainDiag(plain)  # 产生对角矩阵
        res = mul_matmod(self.__invK, self.__diag, 4, self.__N)
        res = mul_matmod(res, self.__K, 4, self.__N)
        # etime = time.time()
        # print('加密的时间是：%fs' % (etime - stime))
        return res

    # 解密
    def __decryption(self, cipher):
        # stime = time.time()
        for i in range(len(cipher)):
            for j in range(len(cipher[0])):
                cipher[i][j] %= self.__N

        res = mul_matmod(self.__K, cipher, 4, self.__N)
        res = mul_matmod(res, self.__invK, 4, self.__N)
        # etime = time.time()
        # print('解密的时间是：%fs' % (etime - stime))
        return res[0][0]

    # todo 加密函数，对输入的图像加密
    # @numba.jit
    def __encryptImage(self):
        self.__encryimage = [[None] * self.__width for i in range(self.__length)]

        """thread = []
        def mythread(i, j, img, pixel):
            img[i][j] = self.__encryption(pixel)
        stime=time.time()
        for i in range(self.__length):
            for j in range(self.__width):
                thread.append(mp.Process(target=mythread, args=(i, j, self.__encryimage, self.__gaussgrayimage[i][j])))

        for i in range(0, self.__size, self.__pro_num):
            if i + self.__pro_num < self.__size:
                [thread[i + j].start() for j in range(self.__pro_num)]
                [thread[i + j].join() for j in range(self.__pro_num)]
            else:
                [thread[j].start() for j in range(i*self.__pro_num,self.__size)]
                [thread[j].join() for j in range(i * self.__pro_num, self.__size)]
        etime=time.time()
        print(etime-stime)"""

        stime = time.time()
        for i in range(self.__length):
            for j in range(self.__width):
                self.__encryimage[i][j] = self.__encryption(self.__gaussgrayimage[i][j])
        etime = time.time()
        print('用户加密时间是：%fs' % (etime - stime))

    # todo 解密函数，对服务器返回的图像解密
    def __decryptImage(self, image):
        stime = time.time()
        self.__denoiseimage = [[None] * self.__width for i in range(self.__length)]
        for i in range(self.__length):
            for j in range(self.__width):
                self.__denoiseimage[i][j] = self.__decryption(image[i][j]) // self.__SCAL
        etime = time.time()
        print('用户解密时间是：%fs' % (etime - stime))

    def __gainABC(self, plain):
        for i in range(self.__M):
            tmp = random.random()
            # tmp=0.5
            if tmp < self.__M / (self.__M + 1):
                self.__A.append(plain)
                self.__B.append(self.__R)
                self.__C.append(self.__R)
            elif tmp >= self.__M / (self.__M + 1) and tmp < 1 - 1 / (2 * (self.__M + 1)):
                self.__A.append(self.__R)
                self.__B.append(plain)
                self.__C.append(self.__R)
            else:
                self.__A.append(self.__R)
                self.__B.append(self.__R)
                self.__C.append(plain)

    def __gainabc(self):
        from modint import chinese_remainder
        self.__a = chinese_remainder(self.__F, self.__A) % self.__N
        self.__b = chinese_remainder(self.__F, self.__B) % self.__N
        self.__c = chinese_remainder(self.__F, self.__C) % self.__N

    def __gainDiag(self, plain):
        self.__diag[0][0] = plain
        self.__diag[1][1], self.__diag[2][2], self.__diag[3][3] = self.__a, self.__b, self.__c

    def test(self):
        pixel = 0
        for i in range(self.__length):
            for j in range(self.__width):
                if self.__image[i][j] == self.__denoiseimage[i][j]:
                    pixel += 1

        print(pixel)
        print('去噪前后重复像素的比例：%0.4f' % (pixel / self.__size))
