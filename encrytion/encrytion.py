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
import random
import operator
from functools import reduce
from Cryptodome.Util import number as prime


class Encrytion:

    def __init__(self,M,bits=512):
        self.__M=M
        self.__P=[]
        self.__Q=[]
        self.__F=[]
        self.__N=None
        self.__bits=bits

    def gainPandQ(self):
        for i in range(self.__M):
            p,q=prime.getPrime(self.__bits),prime.getPrime(self.__bits)
            if prime.isPrime(p) and prime.isPrime(q):
                self.__P.append(p),self.__Q.append(q)
                continue
            i-=1

    def gainF(self):
        for i in range(self.__M):
            self.__F.append(self.__P[i]*self.__Q[i])
        # print(self.__F)

    def gainN(self):
        self.__N=reduce(operator.mul,self.__F)
        # print('%x'%(self.__F[0]*self.__F[1]))
        # print('%x'%self.__N)

    def writeFile(self):  #将算法得到的信息记录到文本
        pass





if __name__=='__main__':
    # encry=Encrytion(2,512)
    # encry.gainPandQ()
    # encry.gainF()
    # encry.gainN()

    a=[[1,2],[3,4]]
    # a=1
    b=operator.matmul(a,a)
    print(b)


    pass