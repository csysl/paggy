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
import cv2
import matplotlib.pyplot as plt
import math
from pylab import mpl
import numpy as np

# 解决matplotlib中文乱码问题
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


# 显示图片
def imageshow(img, title, draw=False):
    plt.imshow(img, cmap='gray')
    plt.title(title)
    if draw:
        cv2.imwrite('resimage/' + title, np.array(img))
        # plt.savefig('resimage/' + title, dpi=1000)
    plt.show()


def calPSNR(sourceimage, targetimage):  # todo 问题：目标图像的范围不在0-255之间
    '''
    :param sourceimage:  源图像 都是灰度图，且是列表
    :param targetimage:  目标图像
    :return:
    '''
    length = len(sourceimage)
    width = len(sourceimage[0])

    # 计算MSE
    MSE = 0
    for i in range(length):
        for j in range(width):
            MSE += pow(sourceimage[i][j] - targetimage[i][j], 2)
    # print(MSE)
    MSE /= float(length * width)

    PSNR = 20 * math.log10(255 / math.sqrt(MSE))
    return PSNR
