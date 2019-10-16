# -*- coding: utf-8 -*-
'''
    @project:paggy
    @file:init.py
    @ide:PyCharm
    @time:2019-10-16 10:54
    @author:Sun
    @todo:
    @ref:
'''

import numpy as np

# todo image
imagepath = 'testimage/1.jpg'
# imagepath = 'img/lena.png'

# todo 局部均值滤波
L = 7  # 滤波窗口的大小   21                                7
S = 3  # 像素矩阵的宽度  必须是奇数  5                              3

# R = 0.5  # JL变换中随机矩阵P的元素的范围，其中每个元素的大小在0-R之间
sigma = 100  # 图片添加高斯噪声的**方差**，产生整数的噪声
sigma = np.sqrt(sigma)
step = 8  # 计算eij的线程数

# todo 去噪
H = 20  # 应该是k的10倍 180                                       40
# SCAL = 10000
SCAL = 37889

"""下面是没有使用到的参数"""
# todo encryption
M = 10  # 加密算法的M值  #
bits=20  # 加密算法产生的密钥长度为2*M*bits