# -*- coding: utf-8 -*-

# import sys
# from libsvm.svmutil import *

# 读取一个目录下的所有图片文件，将图片文件像素解析成多维度16x42向量

from svmutil import *

# y, x = svm_read_problem('../heart_scale.txt')
# m = svm_train(y[:200], x[:200], '-c 4')
# p_label, p_acc, p_val = svm_predict(y[200:], x[200:], m)

# y, x = [1,-1], [[1,0,1], [-1,0,-1]]
# # Sparse data
# y, x = [1,-1], [{1:1, 3:1}, {1:-1,3:-1}]
# prob  = svm_problem(y, x)
# param = svm_parameter('-t 0 -c 4 -b 1')
# m = svm_train(prob, param)

# Precomputed kernel data (-t 4)
# Dense data
y, x = [1,-1], [[1, 2, -2], [2, -2, 2]]
# Sparse data
y, x = [1,-1], [{0:1, 1:2, 2:-2}, {0:2, 1:-2, 2:2}]
# isKernel=True must be set for precomputed kernel
prob  = svm_problem(y, x, isKernel=True)
param = svm_parameter('-t 4 -c 4 -b 1')
m = svm_train(prob, param)
# For the format of precomputed kernel, please read LIBSVM README.