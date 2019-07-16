# -*- coding: utf-8 -*-

import pickle
import os
import jieba
from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

def savefile(savepath, content):    #保存至文件
    fp = open(savepath, "w", encoding="utf-8")
    fp.write(content)
    fp.close()

def readfile(path): #读取文件
    fp = open(path, "rb")
    content = fp.read().decode('utf-8')
    fp.close()
    return content

## 读取bunch对象
def readbunchobj(path):
    file_obj = open(path, "rb")
    bunch = pickle.load(file_obj)
    file_obj.close()
    return bunch

##写入bunch对象
def writebunchobj(path, bunchobj):
    file_obj = open(path, "wb")
    pickle.dump(bunchobj, file_obj)
    file_obj.close()

###主程序
### Train配置
# corpus_path = "data/corpus/"    #未分词分类语料库路径【step01: 准备原始分类文件，将分类文件放在该目录下】
# seg_path = "data/seg/"   #分词后的分类语料库路径【step02: 中间数据，存放分词后的分类文件】
# wordbag_path = "data/train_word_bag/"  # 分词语料Bunch对象持久化文件路径【step03: 存放训练模型数据的目录】
# wordbag_file = "train_set.dat"  # 分词语料Bunch对象持久化文件路径【step04: 训练模型数据文件】
# space_path = "data/train_word_bag/tfidfspace.dat"   # 向量空间模型存放位置

####Test配置
corpus_path = "data/test/"    #未分词分类语料库路径【step01: 准备原始分类文件，将分类文件放在该目录下】
seg_path = "data/seg_test/"   #分词后的分类语料库路径【step02: 中间数据，存放分词后的分类文件】
wordbag_path = "data/test_word_bag/"  # 分词语料Bunch对象持久化文件路径【step03: 存放训练模型数据的目录】
wordbag_file = "test_set.dat"  # 分词语料Bunch对象持久化文件路径【step04: 训练模型数据文件】
space_path = "data/test_word_bag/testspace.dat"   # 向量空间模型存放位置

#读取停用词
stopword_path = "data/train_word_bag/hlt_stop_words.txt"
stpwrdlist = readfile(stopword_path).splitlines()

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
print("==============first-01: 中文语料分词结束!")

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
pickle.dump(bunch, file_obj)    #序列化bunch对象，将其写入到文件中
file_obj.close()
print("==============second-02: 构建文本向量结束!")

##导入分词后的词向量bunch对象
bunch = readbunchobj(wordbag)

##构建tf-idf词向量空间对象
tfidfspace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[], vocabulary={})

##使用TfidVectorizer初始化向量空间模型
vectorizer = TfidfVectorizer(stop_words=stpwrdlist, sublinear_tf=True, max_df=0.5)
transformer = TfidfTransformer()    #该类会统计每个词语的tf-idf权值
#文本转为词频矩阵，单独保存字典文件
tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)
tfidfspace.vocabulary = vectorizer.vocabulary_

##持久化词袋
writebunchobj(space_path, tfidfspace)
print("==============third-03: 构建词袋模型结束!")
