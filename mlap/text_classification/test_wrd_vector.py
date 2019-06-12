# -*- coding: utf-8 -*-

from sklearn.datasets.base import Bunch
import pickle
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer

def readfile(path): #读取文件
    fp = open(path, "rb")
    content = fp.read().decode('utf-8')
    fp.close()
    return content

##1,定义基础函数
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

##2.导入分词后的词向量bunch对象
path = "data/train_word_bag/train_set.dat"
bunch = readbunchobj(path)

##3,构建tf-idf词向量空间对象
tfidfspace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[], vocabulary={})

#读取停用词
stopword_path = "data/train_word_bag/hlt_stop_words.txt"
stpwrdlist = readfile(stopword_path).splitlines()

##4,使用TfidVectorizer初始化向量空间模型
vectorizer = TfidfVectorizer(stop_words=stpwrdlist, sublinear_tf=True, max_df=0.5)
transformer = TfidfTransformer()    #该类会统计每个词语的tf-idf权值
#文本转为词频矩阵，单独保存字典文件
tfidfspace.tdm = vectorizer.fit_transform(bunch.contents)
tfidfspace.vocabulary = vectorizer.vocabulary
##5, 持久化词袋
space_path = "data/train_word_bag/tfidfspace.dat"
writebunchobj(space_path, tfidfspace)

