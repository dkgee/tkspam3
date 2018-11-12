# -*- coding: utf-8 -*-

"""
在训练结束后，一个完整的hack流程：

1. 从网站动态请求相应的验证文件
#. 进行图像预处理
#. 将图像进行分割成最小基本单位
#. 计算出本图像的特征
#. 使用SVM训练好的模型进行对新的验证图片来做结果预测

"""

import time
import requests
import numpy as np
import cv2
import random

from PIL import Image
from pil.lib.img_tools import get_clear_bin_image, get_crop_imgs, get_label_by_path
from pil.lib.svm_lib.svmutil import svm_predict, svm_load_model
from pil.lib.svm_features import get_feature_in_four_box, convert_feature_to_vector


def crack_captcha(rand_captcha_url, cookies):
    """
    破解验证码,完整的演示流程
    :return:
    """

    # 向指定的url请求验证码图片
    # rand_captcha_url = 'https://sso.ckcest.cn/portal/captchaCode'
    res = requests.get(rand_captcha_url, stream=True, cookies=cookies)

    cont = res.content
    imgBuf = np.asarray(bytearray(cont), dtype="uint8")

    # 需要修改
    bin_clear_img = get_clear_bin_image(imgBuf)  # 处理获得去噪的二值图

    img_cache_path = '../pil/lib/cut_pic/temp.jpg'
    cv2.imwrite(img_cache_path,bin_clear_img)

    img = Image.open(img_cache_path)
    child_img_list = get_crop_imgs(img)  # 切割图片为单个字符，保存在内存中,例如：4位验证码就可以分割成4个child

    # 加载SVM模型进行预测
    model_path = '../pil/lib/train_data/svm_model_file'
    model = svm_load_model(model_path)

    #加载标签映射
    lable_to_type_path='../pil/lib/train_data/label_to_type.txt'
    label_to_type = get_label_by_path(lable_to_type_path)

    img_ocr_name = ''
    # img_save_folder = '../pil/lib/crack_img_res'
    # uuid_tag = str(int(time.time())) + str(int(random.random()*100))
    index = 0
    for child_img in child_img_list:
        img_feature_list = get_feature_in_four_box(child_img)  # 使用特征算法，将图像进行特征化降维
        index +=1
        yt = [0]  # 测试数据标签
        xt = convert_feature_to_vector(img_feature_list)  # 将所有的特征转化为标准化的SVM单行的特征向量
        p_label, p_acc, p_val = svm_predict(yt, xt, model)
        for item in p_label:
            img_ocr_label = label_to_type[int(item)]
            img_ocr_name +=img_ocr_label
        # child_img.save(img_save_folder + '/' + uuid_tag + '_' + str(index) + "_" + img_ocr_label + '.png')
    # img.save(img_save_folder + '/' + uuid_tag + img_ocr_name  + '.png')
    return img_ocr_name

def crack_100():
    """
    直接从在线网上下载100张图片，然后识别出来
    :return:
    """
    for i in range(1):
        crack_captcha()


if __name__ == '__main__':
    crack_100()
    # crack_captcha()
    pass

