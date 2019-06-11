# -*- coding: utf-8 -*-

from sklearn.datasets.base import Bunch
import os
import pickle

def readfile(path): #读取文件
    fp = open(path, "rb")
    content = fp.read().decode('utf-8')
    fp.close()
    return content

# Bunch类提供一种key,value的对象形式
# target_name:所有分类集名称列表
# label: 每个文件的分类标签列表
# filenames: 文件路径
# contents: 分词后文件词向量形式

bunch = Bunch(target_name=[], label=[], filenames=[], contents=[])

wordbag_path = "data/train_word_bag/"  # 分词语料Bunch对象持久化文件路径
wordbag_file = "train_set.dat"  # 分词语料Bunch对象持久化文件路径
#seg_path = "data/train_corpus_seg/" #分词后分类语料库路径
seg_path = "data/seg/" #分词后分类语料库路径

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
print("构建文本向量结束")