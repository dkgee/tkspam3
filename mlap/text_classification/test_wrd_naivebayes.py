# -*- coding: utf-8 -*-

import pickle

from sklearn.naive_bayes import MultinomialNB

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

# 测试数据训练到test_set.dat ，然后计算得出testspace.dat  然后使用训练的向量空间模型 tfidfspace.dat  两者运算得出结果

#导入训练集向量空间
trainpath = "data/train_word_bag/tfidfspace.dat"
train_set = readbunchobj(trainpath)

#导入测试集向量空间
testpath = "data/test_word_bag/testspace.dat"
test_set = readbunchobj(testpath)

#应用朴素贝叶斯算法
#alpha: 0.001 alpha越小，迭代次数越多，精度越高
clf = MultinomialNB(alpha=0.001).fit(train_set.tdm, train_set.label)

#预测分类结果
predicted = clf.predict(test_set.tdm)
total = len(predicted);rate=0
for flabel,file_name,expct_cate in zip(test_set.label, test_set.filenames, predicted):
    if flabel != expct_cate:
        rate += 1
        print(file_name, ":实际类别:", flabel, "-->预测类别:", expct_cate)
#精度
print("error rate:", float(rate) * 100/float(total), "%")

## 多项式贝叶斯算法的分类精度非常高

