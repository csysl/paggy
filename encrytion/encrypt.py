# -*- coding: utf-8 -*-
'''
    @project:pag2
    @file:encrytion.py
    @ide:PyCharm
    @time:2019-10-15 10:58
    @author:Sun
    @todo:
    @ref:
'''
import operator
from functools import reduce
from Cryptodome.Util import number as prime
from encrytion.mod import *
import time


class Encrytion:

    def __init__(self, M, bits=512):
        self.__M = M
        self.__P, self.__Q, self.__F = [], [], []
        self.__N = None
        self.__K, self.__invK = None, None  # 矩阵以及模逆矩阵
        self.__det = None
        self.__bits = bits

    def gainKey(self):
        # todo 生成密钥
        stime = time.time()
        self.__gainPandQ()
        self.__gainF()
        self.__gainN()
        # self.__gainK()
        self.__gaininvK()  # 在此处执行gainK
        etime = time.time()
        print('生成key的时间是：%fs' % (etime - stime))

    def __gainPandQ(self):
        for i in range(self.__M):
            p, q = prime.getPrime(self.__bits), prime.getPrime(self.__bits)
            self.__P.append(p), self.__Q.append(q)
            continue

    def __gainF(self):
        for i in range(self.__M):
            self.__F.append(self.__P[i] * self.__Q[i])
        # print(self.__F)

    def __gainN(self):
        self.__N = reduce(operator.mul, self.__F)
        # print('%x'%(self.__F[0]*self.__F[1]))
        # print('%x'%self.__N)

    def __gainK(self):
        self.__K = [[0] * 4 for i in range(4)]
        for i in range(4):
            for j in range(4):
                self.__K[i][j] = prime.getRandomRange(0, self.__N)  # a <= n < b

    def __gaininvK(self):
        while True:
            while True:
                self.__gainK()
                self.__det = gainMatrixDeternminant(self.__K)
                if self.__det % self.__N != 0:
                    break
            # det 的模n逆元素
            invdet = mul_inv(self.__det % self.__N, self.__N)
            # 得到伴随矩阵
            adjmatrix = gainAdjMatrix(self.__K)
            # 得到模逆矩阵
            self.__invK = [[0] * 4 for i in range(4)]
            for i in range(4):
                for j in range(4):
                    self.__invK[i][j] = (adjmatrix[i][j] * invdet) % self.__N
            # 检查模逆矩阵的正确性
            if self.__check_KandInvK():
                break

        # print('det:%x' % self.__det)

    def __check_KandInvK(self):
        def checkone(m):
            for i in range(len(m)):
                for j in range(len(m)):
                    if i == j and m[i][j] != 1:
                        return False
                    elif i != j and m[i][j] != 0:
                        return False
            return True

        res = mul_matmod(self.__K, self.__invK, 4, self.__N)
        if checkone(res):
            print('生成的矩阵和模逆矩阵正确')
            return True
        else:
            print('生成的矩阵和模逆矩阵不正确，重新生成矩阵和模逆矩阵')
            return False

    def writeFile(self):  # 将算法得到的信息记录到文本
        pass


if __name__ == '__main__':
    encry = Encrytion(2, 512)
    encry.gainKey()

    pass
