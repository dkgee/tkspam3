# -*- coding: utf-8 -*-

import os
from numpy import *
import matplotlib.pyplot as plt
import operator

def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


dataSet, labels = createDataSet()
#绘图
fig = plt.figure()
ax = fig.add_subplot(111)
indx = 0
for point in dataSet:
    if labels[indx] == 'A':
        ax.scatter(point[0], point[1], c='blue', marker='o', linewidths=0, s=300)
        plt.annotate("(" + str(point[0]) + "," + str(point[1]) + ")", xy=(point[0], point[1]))
    else:
        ax.scatter(point[0], point[1], c='red', marker='^', linewidths=0, s=300)
        plt.annotate("(" + str(point[0]) + "," + str(point[1]) + ")", xy=(point[0], point[1]))
    indx += 1

#测试数据
testdata = [0.2, 0.2]
# 测试该类
ax.scatter(testdata[0], testdata[1], c='green', marker='^', linewidths=0, s=300)
plt.annotate("(" + str(testdata[0]) + "," + str(testdata[1]) + ")", xy=(testdata[0], testdata[1]))

plt.show()