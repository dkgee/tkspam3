# -*- coding: utf-8 -*-

from PIL import Image
from fnmatch import fnmatch
from os.path import join
import cv2
import os

#
# pytesseract.pytesseract.tesseract_cmd = r'D:\\tesseract-ocr\\tesseract.exe'
# tessdata_dir_config = '--tessdata-dir "D:\\tesseract-ocr\\tessdata" -psm 10'

def _get_dynamic_binary_image(img_src_dir, img_out_dir, img_name):
    '''
    自适应阀值二值化
    '''

    #'./out_img/' + img_name.split('.')[0] + '.jpg'
    filename =  join(img_out_dir, img_name.split('.')[0] + '-bin.jpg')
    #  filedir + '/' + img_name
    img_name =  join(img_src_dir, img_name)
    print('firname_path:' + filename)
    print('img_name_path:' + img_name)
    im = cv2.imread(img_name)
    im = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY) #灰值化
    #二值化
    th1 = cv2.adaptiveThreshold(im, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 21, 1)
    cv2.imwrite(filename,th1)
    return th1

def clear_border(img_out_dir, img, img_name):
    '''去除边框
    '''

    # filename = './out_img/' + img_name.split('.')[0] + '-clearBorder.jpg'
    filename = join(img_out_dir, img_name.split('.')[0] + '-nb.jpg')
    print('firname_path:' + filename)
    h, w = img.shape[:2]
    for y in range(0, w):
        for x in range(0, h):
            # if y ==0 or y == w -1 or y == w - 2:
            if y < 4 or y > w -4:
                img[x, y] = 255
            # if x == 0 or x == h - 1 or x == h - 2:
            if x < 4 or x > h - 4:
                img[x, y] = 255

    cv2.imwrite(filename,img)
    return img


def interference_line(img_out_dir,img, img_name):
    '''
    干扰线降噪
    '''

    #filename =  './out_img/' + img_name.split('.')[0] + '-interferenceline.jpg'
    filename = join(img_out_dir, img_name.split('.')[0] + '-nl.jpg')
    h, w = img.shape[:2]
    # ！！！opencv矩阵点是反的
    # img[1,2] 1:图片的高度，2：图片的宽度
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
    cv2.imwrite(filename,img)
    return img

def interference_point(img_out_dir, img, img_name, x = 0, y = 0):
    """点降噪
    9邻域框,以当前点为中心的田字框,黑点个数,,,
    :param x:
    :param y:
    :return:
    """

    #如果三面没有就去掉，如果上下没有或左右没有也去掉
    # filename =  './out_img/' + img_name.split('.')[0] + '-interferencePoint.jpg'
    filename = join(img_out_dir, img_name.split('.')[0] + '-np.jpg')
    # todo 判断图片的长宽度下限
    cur_pixel = img[x,y]# 当前像素点的值
    print(cur_pixel)
    height,width = img.shape[:2]
    print("%s属性高：%s,宽：%s"%(filename,height,width))

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
    cv2.imwrite(filename,img)
    return filename

#####################################################################
def cut_imgs_and_save(img, img_name, cut_pic_save_folder):
    """
    按照图片的特点,进行切割,这个要根据具体的验证码来进行工作. # 见本例验证图的结构原理图
    分割图片是传统机器学习来识别验证码的重难点，如果这一步顺利的话，则多位验证码的问题可以转化为1位验证字符的识别问题
    :param img:
    :return:
    """
    child_img_list = []

    #geo登录验证码
    for i in range(4):
       x = 18 + i * 16  # 见原理图
       y = 0
       child_img = img.crop((x, y, x + 16, y + 42))
       child_img_list.append(child_img)

    # 开源中国注册登录验证码
    # for i in range(4):
    #     x = 4 + i * (19 + 10)  # 见原理图
    #     y = 0
    #     child_img = img.crop((x, y, x + 19, y + 40))
    #     child_img_list.append(child_img)

    i = 0
    for child_img in child_img_list:
        cut_img_file_name = img_name.split('.')[0] + '-' + ("z%s.png" % i)
        child_img.save(join(cut_pic_save_folder, cut_img_file_name))
        i += 1

def gif_split_to_img():
    """
      Split gif to image
    """
    gifFileName = r'D:\vcode2\01.gif'
    #使用Image模块的open()方法打开gif动态图像时，默认是第一帧
    im = Image.open(gifFileName)
    pngDir = gifFileName[:-4]
    print(pngDir)
    #创建存放每帧图片的文件夹
    os.mkdir(pngDir)
    try:
        while True:
            #保存当前帧图片
            current = im.tell()
            im.save(pngDir+'/'+str(current)+'.png')
            #获取下一帧图片
            im.seek(current+1)
    except EOFError:
        pass

#####################################################################

def main():
    img_src_dir = './img/img_src'

    img_out_dir = './img/img_out'

    for file in os.listdir(img_src_dir):
        if fnmatch(file, '*.png'):
            img_name = file

            #print('step01: 自适应阈值二值化处理')
            # img_bin_save_dir='./img/img_bin'
            im = _get_dynamic_binary_image(img_src_dir, img_out_dir ,img_name)

            #print('step02: 去除边框')
            # img_no_border_dir = './img/img_no_border'
            im = clear_border(img_out_dir, im, img_name)

            #print('step03: 对图片进行干扰线降噪')
            # img_no_interfer_line = './img/img_no_interfer_line'
            im = interference_line(img_out_dir, im, img_name)

            #print('step04: 对图片进行点降噪')
            #img_no_interfer_point = './img/img_no_interfer_point'
            filename = interference_point(img_out_dir, im, img_name)

            #print('step04: 对图片进行切割')
            img = Image.open(filename)
            cut_imgs_and_save(img, img_name, img_out_dir)

            #print('step05: 对图片进行标记(最费时)')

            #print('step06: 标记完成后，进行SVM训练 ')

            #print('step07: SVM训练完成后，进行测试 ')

            # print('step07: SVM测试通过后可行 ')



if __name__ == '__main__':
    main()