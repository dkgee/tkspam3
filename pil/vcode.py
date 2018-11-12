# -*- coding: utf-8 -*-

import numpy as np
import requests
import pytesseract
import os
import cv2

import lib.img_tools as imgtool

pytesseract.pytesseract.tesseract_cmd = r'D:\\tesseract-ocr\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "D:\\tesseract-ocr\\tessdata" -psm 10'



#下载验证码图片
def downloads_pic(pic_name):
    # pic_name = kwargs.get('pic_name', None)
    pic_path = 'D:/vcode2/'
    #url = 'https://sso.ckcest.cn/portal/captchaCode'
    url = 'https://www.oschina.net/action/user/captcha'
    res = requests.get(url, stream=True)
    with open(pic_path + pic_name+'.gif', 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()

def downloads_pic_test():
    rand_captcha_url = r'https://sso.ckcest.cn/portal/captchaCode'
    res = requests.get(rand_captcha_url, stream=True)

    cont = res.content
    buf = np.asarray(bytearray(cont), dtype="uint8")
    img = cv2.imdecode(buf, cv2.IMREAD_COLOR)

    img_cache_path = './easy_img/ttt1.jpg'

    bin_clear_img = imgtool.get_clear_bin_image(img)

    # #step01 灰阶二值化处理
    # img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #灰值化
    # img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)#二值化
    #
    # #step02 清理边框
    # h, w = img.shape[:2]
    # for y in range(0, w):
    #     for x in range(0, h):
    #         if y < 4 or y > w -4:
    #             img[x, y] = 255
    #         if x < 4 or x > h - 4:
    #             img[x, y] = 255
    #
    # # step03 清除干扰线
    # h, w = img.shape[:2]
    # for y in range(1, w - 1):
    #     for x in range(1, h - 1):
    #         count = 0
    #         if img[x, y - 1] > 245:
    #             count = count + 1
    #         if img[x, y + 1] > 245:
    #             count = count + 1
    #         if img[x - 1, y] > 245:
    #             count = count + 1
    #         if img[x + 1, y] > 245:
    #             count = count + 1
    #         if count > 2:
    #             img[x, y] = 255
    #
    #
    # # step04 清理干扰点
    # img = interference_point(img, img_cache_path)
    cv2.imwrite(img_cache_path,bin_clear_img)



def create_cut_pic_dir():
    """
    创建各个标记的训练样本目录
    """
    dir_name='0123456789abcdefghijklmnopqrstuvwxyz'
    parent_dir = './dataa/cut_pic/'
    label_to_type_path='./label_to_type.txt'
    # print(len(dir_name))
    label_to_type_file = open(label_to_type_path, 'w')
    for i in range(36):
        child_dir = parent_dir + str(i)
        line = str(i) + "," +  dir_name[i]
        label_to_type_file.write(line)
        label_to_type_file.write('\n')
        if not os.path.exists(child_dir):
            os.mkdir(child_dir)

    label_to_type_file.close()

def interference_point(img, img_file, x = 0, y = 0):
    """点降噪
    9邻域框,以当前点为中心的田字框,黑点个数,,,
    :param x:
    :param y:
    :return:
    """

    #如果三面没有就去掉，如果上下没有或左右没有也去掉
    cur_pixel = img[x,y]# 当前像素点的值
    height,width = img.shape[:2]
    print("%s属性高：%s,宽：%s"%(img_file,height,width))

    for y in range(0, width - 1):
        for x in range(0, height - 1):
            if y == 0:  # 第一行
                if x == 0:  # 左上顶点,4邻域
                    # 中心点旁边3个点
                    sum = int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 2 * 245:
                        img[x, y] = 0
                elif x == height - 1:  # 右上顶点
                    sum = int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1])
                    if sum <= 2 * 245:
                        img[x, y] = 0
                else:  # 最上非顶点,6邻域
                    sum = int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 3 * 245:
                        img[x, y] = 0
            elif y == width - 1:  # 最下面一行
                if x == 0:  # 左下顶点
                    # 中心点旁边3个点
                    sum = int(cur_pixel) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x, y - 1])
                    if sum <= 2 * 245:
                        img[x, y] = 0
                elif x == height - 1:  # 右下顶点
                    sum = int(cur_pixel) \
                          + int(img[x, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y - 1])

                    if sum <= 2 * 245:
                        img[x, y] = 0
                else:  # 最下非顶点,6邻域
                    sum = int(cur_pixel) \
                          + int(img[x - 1, y]) \
                          + int(img[x + 1, y]) \
                          + int(img[x, y - 1]) \
                          + int(img[x - 1, y - 1]) \
                          + int(img[x + 1, y - 1])
                    if sum <= 3 * 245:
                        img[x, y] = 0
            else:  # y不在边界
                if x == 0:  # 左边非顶点
                    sum = int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])

                    if sum <= 3 * 245:
                        img[x, y] = 0
                elif x == height - 1:  # 右边非顶点
                    sum = int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x - 1, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1])

                    if sum <= 3 * 245:
                        img[x, y] = 0
                else:  # 具备9领域条件的
                    sum = int(img[x - 1, y - 1]) \
                          + int(img[x - 1, y]) \
                          + int(img[x - 1, y + 1]) \
                          + int(img[x, y - 1]) \
                          + int(cur_pixel) \
                          + int(img[x, y + 1]) \
                          + int(img[x + 1, y - 1]) \
                          + int(img[x + 1, y]) \
                          + int(img[x + 1, y + 1])
                    if sum <= 4 * 245:
                        img[x, y] = 0

    return img


downloads_pic_test()

# for i in range(1,10):
#     downloads_pic(str(i))

# create_cut_pic_dir()