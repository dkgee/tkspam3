# -*- coding: utf-8 -*-

import pickle
from sklearn.datasets.base import Bunch
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer


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

def readfile(path): #读取文件
    fp = open(path, "rb")
    content = fp.read().decode('utf-8')
    fp.close()
    return content

####################################################################################################
# 导入分词后的词向量bunch对象
path = "data/test_word_bag/test_set.dat" #词向量空间保存路径
bunch = readbunchobj(path)

# 构建测试集tfidf向量空间
testspace = Bunch(target_name=bunch.target_name, label=bunch.label, filenames=bunch.filenames, tdm=[], vocabulary={})

# 导入训练集的词袋
trainbunch = readbunchobj("data/train_word_bag/tfidfspace.dat")

#读取停用词
stopword_path = "data/train_word_bag/hlt_stop_words.txt"
stpwrdlist = readfile(stopword_path).splitlines()

# 使用TfidfVectorizer初始化向量空间模型
vectorizer = TfidfVectorizer(stop_words=stpwrdlist, sublinear_tf=True, max_df=0.5, vocabulary=trainbunch.vocabulary)

transformer = TfidfTransformer()
# testspace.tdm = vectorizer.fit_transform(bunch.contents)
testspace.tdm = vectorizer.transform(bunch.contents)
testspace.vocabulary = trainbunch.vocabulary

# 创建词袋的持久化
space_path = "data/test_word_bag/testspace.dat"
writebunchobj(space_path, testspace)

print("==============third-03: 构建测试空间模型完成")
####################################################################################################