# -*- coding: utf-8 -*-

import requests
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r'D:\\tesseract-ocr\\tesseract.exe'
tessdata_dir_config = '--tessdata-dir "D:\\tesseract-ocr\\tessdata" -psm 10'



#下载验证码图片
def downloads_pic(pic_name):
    # pic_name = kwargs.get('pic_name', None)
    pic_path = 'D:/vcode/'
    url = 'https://sso.ckcest.cn/portal/captchaCode'
    res = requests.get(url, stream=True)
    with open(pic_path + pic_name+'.jpg', 'wb') as f:
        for chunk in res.iter_content(chunk_size=1024):
            if chunk:  # filter out keep-alive new chunks
                f.write(chunk)
                f.flush()
        f.close()

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




for i in range(1,3000):
    downloads_pic(str(i))

# create_cut_pic_dir()