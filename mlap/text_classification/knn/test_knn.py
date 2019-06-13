# -*- coding: utf-8 -*-

from numpy import *
import operator
from mlap.text_classification.bayes.Nbayes_lib import *

k = 3
#夹角余弦距离公式
def cosdist(vector1, vector2):
    return dot(vector1, vector2) /(linalg.norm(vector1) * linalg.norm(vector2))

#kNN分类器
#测试集：testdata；训练集：trainSet；类别标签：listClasses；k：k个邻居数
def classify(testdata, trainSet, listClasses, k):
    dataSetSize = trainSet.shape[0] #返回样本集的行数
    distances = array(zeros(dataSetSize))
    for indx in range(dataSetSize): #计算测试集与训练集之间的距离：夹角余弦
        distances[indx] = cosdist(testdata, trainSet[indx])
        #根据生成的夹角余弦按从大到小排序，结果为索引号
        sortedDistIndicies = argsort(-distances)
        classCount = {}
        for i in range(k):  #获取角度最小的前k项作为参考项
            #按排序顺序返回样本集对应的类别标签
            votellabel = listClasses[sortedDistIndicies[i]]
            #为字典classCount 赋值，相同key，其value加1
            classCount[votellabel] = classCount.get(votellabel, 0) + 1
            #对分类字典class Count 按value重新排序
            # sorted(data.iteritems(), key = operator.itemgetter(1), reverse=True)
            #该句是按字典值排序的固定用法
            #classCount.iteritems():字典迭代器函数
            #key：排序参数；operator.itemgetter(1)：多级排序
            sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
            return sortedClassCount[0][0]   #返回序最高的一项

dataSet, listClasses = loadDataSet()
nb = NBayes()
nb.train_set(dataSet, listClasses)
#使用之前贝叶斯分类阶段的数据集，以及生成的tf向量进行分类
print(classify(nb.tf[3], nb.tf, listClasses, k))