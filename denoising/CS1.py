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
        self.__prencrytimage = encryptImage

        # key
        self.__K, self.__invK, self.__Kcs, self.__invKcs = TP.cs1K
