# -*- coding: utf-8 -*-

import os
import sys
import jieba


def savefile(savepath, content):    #保存至文件
    fp = open(savepath, "w", encoding="utf-8")
    fp.write(content)
    fp.close()

def readfile(path): #读取文件
    fp = open(path, "rb")
    content = fp.read().decode('utf-8')
    fp.close()
    return content

###主程序
corpus_path = "data/corpus/"    #未分词分类语料库路径
seg_path = "data/seg/"   #分词后的分类语料库路径
catelist = os.listdir(corpus_path)  #获取所有子目录
#获取子目录下的所有文件
for mydir in catelist:
    class_path = corpus_path + mydir + "/"
    seg_dir = seg_path + mydir + "/"
    if not os.path.exists(seg_dir):
        os.makedirs(seg_dir)
    file_list = os.listdir(class_path)
    for file_path in file_list:
        fullname = class_path + file_path
        content = readfile(fullname).strip()
        content = content.replace("\r\n", "").strip()
        content_seg = jieba.cut(content)
        savefile(seg_dir + file_path, " ".join(content_seg))

print("中文语料分词结束！！！")