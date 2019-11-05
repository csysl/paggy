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
import numpy as np
from Crypto.Util import number as prime

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
        self.__encryimage, self.__padimage, self.__denoiseimage, self.__decryimage = None, None, None, None  # 存放对来自用户的图片加密后的图片和最后要返回给用户的图片

        # key for cs1
        self.__K1, self.__invK1, self.__Kcs1, self.__invKcs1 = TP.cs1K
        # key for cs2
        self.__Kcs2, self.__invKcs2 = TP.cs2K
        self.__N = TP.N

        # 去噪
        self.__S, self.__L = init.S, init.L
        self.__H, self.__SCAL = init.H, init.SCAL
        self.__scope, self.__lscope = self.__S // 2, self.__L // 2
        self.__relength = self.__length + (self.__scope + self.__lscope) * 2
        self.__rewidth = self.__width + (self.__scope + self.__lscope) * 2

        # CS加解密（对w）
        self.__M, self.__F, self.__R = TP.M, TP.F, TP.R
        # self.__R = prime.getRandomRange(0, self.__N)  #todo R这里应该随机取还是和USER取一样的R吗？不知道，先取成一致
        self.__A, self.__B, self.__C = [], [], []
        self.__a, self.__b, self.__c = -1, -1, -1
        self.__diag = [[0] * 4 for i in range(4)]  # 对角矩阵

        # test
        self.__testK, self.__testinvK = TP.K

    # 对用户发送的图片进行加密，加密后等同于对图像I使用k加密
    def CS1encryptI(self):
        self.__encryimage = [[None] * self.__width for i in range(self.__length)]
        stime = time.time()
        for i in range(self.__length):
            for j in range(self.__width):
                self.__encryimage[i][j] = self.__CS1encryption(self.__originEryptImage[i][j])
        etime = time.time()
        print('CS1对原图像加密时间是：%fs' % (etime - stime))

    # 将去噪后的密文图像进行一次解密，然后传给用户
    def CS1decryptI(self):
        self.__decryimage = [[None] * self.__width for i in range(self.__length)]
        stime = time.time()
        for i in range(self.__length):
            for j in range(self.__width):
                self.__decryimage[i][j] = self.__CS1decryption(self.__denoiseimage[i][j])
        etime = time.time()
        print('CS1对去噪后图像解密时间是：%fs' % (etime - stime))
        return self.__decryimage

    # 加密密文
    def __CS1encryption(self, plain):
        # stime = time.time()
        res = mul_matmod(self.__invK1, plain, 4, self.__N)
        res = mul_matmod(res, self.__K1, 4, self.__N)
        # etime = time.time()
        # print('加密的时间是：%fs' % (etime - stime))
        return res

    # 单像素解密
    def __CS1decryption(self, cipher):
        # stime = time.time()
        for i in range(len(cipher)):
            for j in range(len(cipher[0])):
                cipher[i][j] %= self.__N

        res = mul_matmod(self.__K1, cipher, 4, self.__N)
        res = mul_matmod(res, self.__invK1, 4, self.__N)
        # etime = time.time()
        # print('解密的时间是：%fs' % (etime - stime))
        return res

    # 将加密的图片进行扩充
    def __gainPadImage(self):
        scope = self.__scope + self.__lscope
        shape = ((scope, scope), (scope, scope), (0, 0), (0, 0))
        self.__padimage = np.pad(np.array(self.__encryimage), shape, mode='symmetric')

    # TODO 去噪，计算距离，上传距离，计算去噪参数，返回参数，使用参数去噪，全部在这一步执行
    def Cs1Cs2Denoising(self):
        # todo 图片扩充
        self.__gainPadImage()
        # todo 进行去噪
        stime = time.time()
        self.__NLmean()
        etime = time.time()
        print('图像去噪时间是: %0.2fs' % (etime - stime))

    # 非局部均值去噪
    def __NLmean(self):
        self.__denoiseimage = np.zeros((self.__length, self.__width, 4, 4), dtype=object)
        H2 = pow(self.__H, 2)
        scope = self.__scope + self.__lscope

        for i in range(self.__length):
            for j in range(self.__width):
                indi, indj = i + scope, j + scope
                w1 = self.__padimage[indi - self.__scope:indi + self.__scope + 1,
                     indj - self.__scope:indj + self.__scope + 1]  # 原窗口
                # print(w1)

                ww = np.zeros((self.__L, self.__L), dtype=object)

                for ii in range(indi - self.__lscope, indi + self.__lscope + 1):
                    for jj in range(indj - self.__lscope, indj + self.__lscope + 1):
                        if ii == indi and jj == indj:
                            continue
                        w2 = self.__padimage[ii - self.__scope:ii + self.__scope + 1,
                             jj - self.__scope:jj + self.__scope + 1]

                        encryptDis = self.__CS1gainCalDis(w1, w2)
                        decryptDis = self.__CS1gainDecryptDis(encryptDis)
                        dis = self.__CS2gainPlainDis(decryptDis)
                        ww[ii - (indi - self.__lscope)][jj - (indj - self.__lscope)] = np.exp(-dis / H2)

                # print(ww.max())
                ww[self.__lscope][self.__lscope] = ww.max()
                plainW = self.__CS2gainPlainW(ww)  # 得到去噪参数
                # print('参数：', plainW)
                cipherW = self.__CS2gainCipherW(plainW)  # CS2对去噪参数加密
                # print(cipherW)
                cipherW = self.__CS1gainCipherW(cipherW)  # CS1对去噪参数加密
                # print(cipherW)
                self.__denoiseimage[i][j] = self.__CS1denoising(cipherW, self.__padimage[
                                                                         indi - self.__lscope:indi + self.__lscope + 1,
                                                                         indj - self.__lscope:indj + self.__lscope + 1])
                # print(self.__denoiseimage[i][j])
                #
                # return

        print('done!')

    # CS1得到加密后的dis
    def __CS1gainCalDis(self, block1, block2):
        block = (block1 - block2) % self.__N  #
        # block = np.power(block, 2) % self.__N  #TODO 只有这里可能没有满足同态性
        for i in range(block.shape[0]):
            for j in range(block.shape[1]):
                block[i][j] = np.dot(block[i][j], block[i][j]) % self.__N
        encryptDis = np.sum(block, axis=(0, 1)) % self.__N
        return encryptDis

    # CS1得到使用Kcs1解密的dis
    def __CS1gainDecryptDis(self, encryptDis):
        decryptDis = np.dot(self.__Kcs1, encryptDis) % self.__N
        decryptDis = np.dot(decryptDis, self.__invKcs1) % self.__N
        return decryptDis

    # CS2使用Kcs2解密，得到dis的明文
    def __CS2gainPlainDis(self, decryptDis):
        dis = np.dot(self.__Kcs2, decryptDis) % self.__N
        dis = np.dot(dis, self.__invKcs2) % self.__N
        return dis[0][0]

    # CS2使用dis的明文计算去噪参数w
    def __CS2gainPlainW(self, ww: 'np.ndarray'):
        ww /= ww.sum()
        ww *= self.__SCAL
        plainW = np.floor(ww)
        return plainW

    # CS2使用invKcs2对w进行加密
    def __CS2gainCipherW(self, plainW: 'np.ndarray'):
        # 加密密文
        def encryption(plain):
            # stime = time.time()
            self.__gainABC(plain)
            self.__gainabc()
            self.__A.clear(), self.__B.clear(), self.__C.clear()  # 多像素加密时清空，因为产生ABC使用的是append方式
            self.__gainDiag(plain)  # 产生对角矩阵
            res = mul_matmod(self.__invKcs2, self.__diag, 4, self.__N)
            res = mul_matmod(res, self.__Kcs2, 4, self.__N)
            # etime = time.time()
            # print('加密的时间是：%fs' % (etime - stime))
            return res

        cipherW = np.zeros((self.__L, self.__L, 4, 4), dtype=object)
        for i in range(self.__L):
            for j in range(self.__L):
                cipherW[i][j] = encryption(plainW[i][j])
        return cipherW

    # CS1使用invkcs1对w进行加密
    def __CS1gainCipherW(self, cipherW: 'np.ndarray'):
        cipherW1 = np.zeros((self.__L, self.__L, 4, 4), dtype=object)
        for i in range(self.__L):
            for j in range(self.__L):
                cipherW1[i][j] = np.dot(np.dot(self.__invKcs1, cipherW[i][j]) % self.__N, self.__Kcs1) % self.__N
        return cipherW1

    # CS1对密文进行去噪
    def __CS1denoising(self, cipherW: 'np.ndarray', block: 'np.ndarray'):
        res = np.zeros((4, 4), dtype=object)
        for i in range(self.__L):
            for j in range(self.__L):
                res += np.dot(cipherW[i][j], block[i][j]) % self.__N
                res % self.__N
        return res

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
        imageshow(self.__denoiseimage, '测试结果')

    """以上用做测试"""
