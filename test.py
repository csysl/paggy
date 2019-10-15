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
a = [0] * 4
a = [a[:] for i in range(4)]
for i in range(4):
    for j in range(4):
        a[i][j] = i * 4 + j

for i in range(4):
    b=a[:]
    for j in range(4):
        b.remove(a[i])
        for ii in range(4):

            b[ii].remove()