# -*- coding: utf-8 -*-

import pickle
import os
import jieba
from sklearn.datasets.base import Bunch

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
corpus_path = "data/corpus/"    #未分词分类语料库路径【step01: 准备原始分类文件，将分类文件放在该目录下】
seg_path = "data/seg/"   #分词后的分类语料库路径【step02: 中间数据，存放分词后的分类文件】
wordbag_path = "data/train_word_bag/"  # 分词语料Bunch对象持久化文件路径【step03: 存放训练模型数据的目录】
wordbag_file = "train_set.dat"  # 分词语料Bunch对象持久化文件路径【step04: 训练模型数据文件】

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
print("first-01: 中文语料分词结束!")

bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])
catelist = os.listdir(seg_path)
bunch.target_name.extend(catelist)  #将类别信息保存到bunch对象中
for mydir in catelist:
    class_path = seg_path + mydir + "/"
    file_list = os.listdir(class_path)
    for file_path in file_list:
        fullname = class_path + file_path
        bunch.label.append(mydir)   # 保存当前文件的分类标签
        bunch.filenames.append(fullname)    #保存当前文件的文件路径
        bunch.contents.append(readfile(fullname).strip())   # 保存文件词向量

if not os.path.exists(wordbag_path):
        os.makedirs(wordbag_path)
wordbag = wordbag_path + wordbag_file
#bunch 对象持久化
file_obj = open(wordbag, "wb")
pickle.dump(bunch, file_obj)
file_obj.close()
print("second-02: 构建文本向量结束!")
