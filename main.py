# -*- coding: utf-8 -*-
'''
    @project:paggy
    @file:main.py
    @ide:PyCharm
    @time:2019-10-16 10:54
    @author:Sun
    @todo:
    @ref:
'''
import cv2
import init
from encrytion.encrypt import Encryption
from denoising.USER import USER
from denoising.CS import CS

# todo 读取图片
# img = io.imread(init.imagepath)  # length*width*(r,g,b)
img = cv2.imread(init.imagepath, cv2.IMREAD_GRAYSCALE)

# TP为密钥生成器并生成密钥
TP = Encryption(init.M, init.bits)
TP.gainParam()  # 生成密钥和参数
# TP.writeFile()  #将密钥写入到txt，目的是为了c++程序读取

# user产生加密图像
user = USER(image=img, TP=TP)
encryptImage = user.encrypt()

# cs得到加密图像，产生加密后的距离
cs = CS(encryptImage=encryptImage, TP=TP)
cs.CS1encryptI()  # 对来自用户的图片进行加密，等同于对图像I使用k加密
# cs.testdecryption() #测试函数
cs.Cs1Cs2Denoising()  # cs1和cs2去噪的全过程
decryptImageRe = cs.CS1decryptI()  # 得到cs1一次解密后的去噪图片

# 用户得到去噪后图片密文，然后进行解密
user.decrypt(decryptImageRe)

from SSIM_PIL import compare_ssim
from PIL import Image

image1 = Image.open('img/' + init.imagepath[4:])
image2 = Image.open('resimage/' + init.imagepath[4:])
value = compare_ssim(image1, image2)
print("去噪图像和源图像的SSIM是", value)

# import tensorflow as tf
#
# im1 = tf.decode_png('img/' + init.imagepath[4:])
# im2 = tf.decode_png('resimage/' + init.imagepath[4:])
# # Compute SSIM over tf.uint8 Tensors.
# ssim1 = tf.image.ssim(im1, im2, max_val=255, filter_size=11,
#                       filter_sigma=1.5, k1=0.01, k2=0.03)
# print("去噪图像和源图像的SSIM是", ssim1)


#user.test()
