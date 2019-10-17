# -*- coding: utf-8 -*-
'''
    @project:paggy
    @file:test.py
    @ide:PyCharm
    @time:2019-10-15 19:26
    @author:Sun
    @todo:
    @ref:
'''

from Cryptodome.Util import number
import time

def matmulti(a, b, row, n, col):
    res = [0] * col
    res = [res[:] for i in range(row)]
    for i in range(row):
        for j in range(col):
            for k in range(n):
                res[i][j] += a[i][k] * b[k][j]
    return res

a=[]
for i in range(10):
    a.append([])
    for j in range(10):
        a[i].append(number.getRandomInteger(512))
print(a)
stime=time.time()
print(matmulti(a,a,10,10,10))
etime=time.time()
print(etime-stime)


import numpy as np
a=np.array(a)
print(a)
stime=time.time()
print(np.dot(a,a))
etime=time.time()
print(etime-stime)