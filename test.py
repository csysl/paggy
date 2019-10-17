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
import numpy as np

# kernel = np.ones((4, 4),dtype=object)
# b=kernel/np.power(16,2)
#
# a=[]
# for i in range(4):
#     a.append([])
#     for j in range(4):
#         a[i].append(number.getRandomInteger(512))
# print(a)
# print(kernel)
# print()
# c=np.dot(np.array(a),b)
# d=np.ceil(c)
# print(np.dot(np.array(a),b))


a=np.array([[1,2],[3,4]])
print(np.sum(a,axis=1))
#
a=[]
for i in range(2):
    a.append([])
    for j in range(2):
        a[i].append([])
        for l in range(2):
            a[i][j].append([])
            for k in range(2):
                a[i][j][l].append((i+1)*(j+1)*(l+1)+k+1)
a=np.array(a)
print(a.shape[0])
print(a)
print(np.sum(a))
print(np.sum(a,axis=(0,1)))

# a=np.array(a)
# b=np.ones((2,2),dtype=object)
# print(np.multiply(b,a))
# print(a.shape)
# b=np.pad(a,((2,2),(2,2),(0,0),(0,0)),mode='symmetric')
# print(b.shape)



# def matmulti(a, b, row, n, col):
#     res = [0] * col
#     res = [res[:] for i in range(row)]
#     for i in range(row):
#         for j in range(col):
#             for k in range(n):
#                 res[i][j] += a[i][k] * b[k][j]
#     return res
#
# a=[]
# for i in range(10):
#     a.append([])
#     for j in range(10):
#         a[i].append(number.getRandomInteger(512))
# print(a)
# stime=time.time()
# print(matmulti(a,a,10,10,10))
# etime=time.time()
# print(etime-stime)
#
#
# import numpy as np
# a=np.array(a)
# print(a)
# stime=time.time()
# print(np.dot(a,a))
# etime=time.time()
# print(etime-stime)