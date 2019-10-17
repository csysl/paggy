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
from pylab import mpl

# 解决matplotlib中文乱码问题
mpl.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # 指定默认字体
mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

# 显示图片
def imageshow(img,title):
    plt.imshow(img, cmap='gray')
    plt.title(title)
    plt.show()



