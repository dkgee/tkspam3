# -*- coding: utf-8 -*-

import cv2


def get_clear_bin_image(imgBuf):
    img = cv2.imdecode(imgBuf, cv2.IMREAD_COLOR)
    #step01 灰阶二值化处理
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #灰值化
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)#二值化
    #step02 清理边框
    h, w = img.shape[:2]
    for y in range(0, w):
        for x in range(0, h):
            if y < 4 or y > w -4:
                img[x, y] = 255
            if x < 4 or x > h - 4:
                img[x, y] = 255
    # step03 清除干扰线
    h, w = img.shape[:2]
    for y in range(1, w - 1):
        for x in range(1, h - 1):
            count = 0
            if img[x, y - 1] > 245:
                count = count + 1
            if img[x, y + 1] > 245:
                count = count + 1
            if img[x - 1, y] > 245:
                count = count + 1
            if img[x + 1, y] > 245:
                count = count + 1
            if count > 2:
                img[x, y] = 255
    # step04 清理干扰点
    img = interference_point(img)
    return img

def get_crop_imgs(img):
    child_img_list = []

    #geo登录验证码
    for i in range(4):
        x = 18 + i * 16  # 见原理图
        y = 0
        child_img = img.crop((x, y, x + 16, y + 42))
        child_img_list.append(child_img)
    return child_img_list

def get_label_by_path(lable_to_type_path):
    label_to_type = []
    #获取标签映射
    with open(lable_to_type_path) as f:
        for line in f:
            tt = line.split(',')[1].replace("\n", "")
            label_to_type.append(tt)

    return label_to_type


def interference_point(img, x = 0, y = 0):
    """点降噪
    9邻域框,以当前点为中心的田字框,黑点个数,,,
    :param x:
    :param y:
    :return:
    """

    #如果三面没有就去掉，如果上下没有或左右没有也去掉
    cur_pixel = img[x,y]# 当前像素点的值
    height,width = img.shape[:2]

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