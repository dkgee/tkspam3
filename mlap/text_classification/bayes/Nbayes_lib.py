# -*- coding: utf-8 -*-

import numpy as np

def loadDataSet():
    #训练集文本
    postingList = [['my','dog','has','flea','problems','help','please'],
        ['maybe','not','take','him','to','dog','park','stupid'],
        ['my','dalmation','is','so','cute','I','love','him','my'],
        ['stop','posting','stupid','worthless','garbage'],
        ['mr','licks','ate','my','steak','how','to','stop','him'],
        ['quit','buying','worthless','dog','food','stupid']]
    classVec = [0,1,0,1,0,1]    #1 is abusive,0 not 每个文本对应的分类
    return postingList,classVec

# 贝叶斯算法类
class NBayes(object):
    def __init__(self):
        self.vocabulary=[]  # 词典
        self.idf = 0    # 词典的idf权值向量
        self.tf = 0     # 训练集的权值矩阵
        self.tdm = 0    # P(x|yi)
        self.Pcates = {}    #P(yi)是个类别字典
        self.labels = []    # 对应每个文本的分类，是个外部导入的列表
        self.doclength = 0  # 训练集文本数
        self.vocablen = 0   # 词典词长
        self.testset = 0    #测试集

    #导入和训练数据集，生成算法必须的参数和数据结构
    def train_set(self, train_set, classVec):
        self.cate_prob(classVec)    #计算每个分类在数据集中的概率：P(yi)
        self.doclength = len(train_set)
        tempset = set()
        [tempset.add(word) for doc in train_set for word in doc]    # 生成词典
        self.vocabulary = list(tempset)
        self.vocablen = len(self.vocabulary)
        self.calc_wordfreq(train_set)   #计算词频数据集
        # self.build_tmd()  #按分类累计向量空间的每维值：P(x|yi)
        self.bulid_tmd()     #按分类累计向量空间的每维值：P(x|yi)

    # 计算每个分类在数据集中的概率
    def cate_prob(self, classVec):
        self.labels = classVec
        labeltemps = set(self.labels)   #获取全部分类
        for labeltemp in labeltemps:
            # 统计列表中重复的分类： self.labels.count(labeltemp)
            self.Pcates[labeltemp] = float(self.labels.count(labeltemp))/float(len(self.labels))

    # 生成普通词频向量
    def calc_wordfreq(self,trainset):
        self.idf = np.zeros([1, self.vocablen]) #1,词典数
        self.tf = np.zeros([self.doclength, self.vocablen]) # 训练集文件数*词典数
        for index in range(self.doclength): #遍历所有的文本
            for word in trainset[index]:    #遍历文本中所有的词
                self.tf[index, self.vocabulary.index(word)] += 1    #找到文本的词在字典中的位置+1
            for singleword in set(trainset[index]):
                self.idf[0, self.vocabulary.index(singleword)] += 1

    # 按分类累计向量空间的每维值
    def bulid_tmd(self):
        self.tdm = np.zeros([len(self.Pcates), self.vocablen])  #类别行 词典列
        sumlist = np.zeros([len(self.Pcates), 1])   # 统计每个分类的总值
        for indx in range(self.doclength):
            self.tdm[self.labels[indx]] += self.tf[indx]    # 将同一类别的词向量空间值加总
            sumlist[self.labels[indx]] = np.sum(self.tdm[self.labels[indx]])
        self.tdm = self.tdm/sumlist #生成P(x|yi)

    # 将测试集映射到当前词典
    def map2vocab(self, testdata):
        self.testset = np.zeros([1, self.vocablen])
        for word in testdata:
            self.testset[0, self.vocabulary.index(word)] += 1

    def predict(self, testset):
        if np.shape(testset)[1] != self.vocablen:  # 如果测试集长度与词典不相等，退出程序
            print("输入错误")
            exit(0)
        predvalue = 0  # 初始化类别概率
        predclass = ""    #初始化类别名称
        for tdm_vect,keyclass in zip(self.tdm, self.Pcates):
            # P（xlyi）P（yi）
            temp = np.sum(testset * tdm_vect * self.Pcates[keyclass]) # 变量tdm，计算最大分类
            if temp > predvalue:
                predvalue = temp
                predclass = keyclass
        return predclass

    # 生成f-idf
    def calc_tfidf(self, trainset):
        self.idf=np.zeros([1,self.vocablen])
        self.tf = np.zeros([self.doclength,self.vocablen])
        for indx in range(self.doclength):
            for word in trainset[indx]:
                self.tf[indx,self.vocabulary.index(word)] += 1
            # 消除不同句长导致的偏差
            self.tf[indx] = self.tf[indx] / float(len(trainset[indx]))
        for singleword in set(trainset[indx]):
            self.idf[0,self.vocabulary.index(singleword)] += 1
            self.idf=np.log(float(self.doclength) / self.idf)
            self.tf=np.multiply(self.tf,self.idf)  # 矩阵与向量的点乘 tfxidf


##
dataSet,listClasses = loadDataSet() #导入外部数据集
#dataset：句子的词向量，
#listClass是句子所属的类别[0，1，0，1，0，1]
nb = NBayes() #实例化
nb.train_set(dataSet, listClasses)   #训练数据集
nb.map2vocab(dataSet[0])    #随机选择一个测试句
print(nb.predict(nb.testset))   #   输出分类结果