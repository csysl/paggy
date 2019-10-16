# -*- coding: utf-8 -*-
'''
    @project:paggy
    @file:image.py
    @ide:PyCharm
    @time:2019-10-16 10:53
    @author:Sun
    @todo:
    @ref:
'''

# from encrytion.encrypt import Encryption
# import init
#
# import copy
# import math
# import time
# import random
# import cv2
import matplotlib.pyplot as plt

def imageshow(img,title):
    plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.show()


class Image(Encryption):

    def __init__(self, image):
        self.__image = copy.deepcopy(image)
        self.__grayimage, self.__gaussgrayimage, self.__padimage = None, None, None  # 原始灰度图,添加了gauss噪声的灰度图,进行局部均值去噪的扩充图

        self.__length, self.__width = len(image), len(image[0])
        self.__size = self.__length * self.__width  # 像素个数

        # TODo 加密
        Encryption.__init__(self, M=init.M, bits=init.bits)
        Encryption.gainParam(self)
        self.__encryimage1, self.__encryimage2 = None, None  #用户和cs1的加密图像
        self.__decryimage1, self.__decryimage2 = None, None  #用户和cs1的解密图像
        self.__encryimage, self.__denoiseimage = None, None  #cs1处理后的图像和用户解密后的图像

        # # todo JL
        # self.__S = init.S  # 每个像素的小矩阵的宽度
        # self.__L = init.L
        # self.__scope = self.__S // 2
        # self.__lscope = self.__L // 2
        # self.__relength = self.__length + (self.__scope + self.__lscope) * 2
        # self.__rewidth = self.__width + (self.__scope + self.__lscope) * 2
        # self.__sigma = init.sigma  # 添加高斯噪音的标准差
        #
        # # todo 去噪
        # self.__H = init.H  #
        # self.__SCAL = init.SCAL
        #
        # # todo 评估
        # self.__PSNR = 0

    # todo 用户加密上传图片
    def userEncryption(self):
        # 获取灰度图
        self.__grayimage = copy.deepcopy(self.__image).tolist()
        imageshow(self.__grayimage,'grayimage')  #显示灰度图
        # 给灰度图添加高斯噪声
        self.__gaussgrayimage=self.__addgaussnoise()
        imageshow(self.__gaussgrayimage,'gaussgrayimage')


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
    def __encryptImage(self,image,K):
        '''
        :param image:  要加密的图像
        :param K: 密钥
        :return:
        '''


