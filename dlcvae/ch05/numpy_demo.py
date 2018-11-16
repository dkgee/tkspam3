# -*- coding: utf-8 -*-

import numpy as np
import numpy.random as random

# array 数组，numpy中最基本的数据结构
## 一维数组
# a = [1,2,3,4]
# b = np.array(a)
# print(b)
# print(type(b))
# print(b.shape)  # b的维度
# print(b.argmax())   # b中最大值的索引
# print(b.max())  #返回b中最大值
# print(b.mean()) #返回b中平均值
##二维数组
# c = [[1,7], [3,4], [5,6]]
# d = np.array(c) #转换为np的数组
# print(d.shape)  # 维度
# print(d.size)   # 数组值数量
# print(d.max(axis=0)) # 旋转一圈，找出每个维度最大值，就是在数组上[1,7]\[3,4]\[5,6]组成的1,3,5和7,4,6两个维度中，每个维度中最大值  [5, 7]
# print(d.max(axis=1)) # 旋转两圈，相当于没旋转，找出维度1，找出每个组数中的最大值， [7,4,6]
# print(d.mean(axis=0))
# print(d.flatten())  #展开数组为1维数组
# print(np.ravel(c))  # 调用静态方法展开1维数组
## 三维浮点型数组
# e = np.ones((3, 3), dtype=np.float) #创建一个3x3的1维浮点矩阵
# print(e)
# f = np.repeat(3, 4) # 创建一个1维值为3的矩阵，重复4次
# print(f)
# g = np.zeros((2, 2, 3), dtype=np.uint8)
# print(g)
# print(g.shape)
# # h = np.astype(np.float)
# # print(h)
# l = np.arange(10)
# print(l)
# m = np.linspace(0, 6, 5)
# print(m)
# p = np.array([[1,2,3,4],[5,6,7,8]])
# np.save('p.npy',p)
# q = np.load('p.npy')
# print(q)

## 多为数组
a = np.arange(24).reshape((2, 3, 4))        # 此为嵌套矩阵，二维矩阵
# print(a)
# print(a.shape)
# b = a[1][1][1]
# print(b)
# c = a[:, 2, :]  # 表示当前维度所有下表
# print(c)
# d = a[:, :, 1]
# print(d)
# e = a[..., 1]   #用以表明没有指明维度值
# print(e)
# print('+++++++++++++++1')
# f = a[:, 1:, 1:-1]
# print(f)
# g = np.split(np.arange(9), 3)
# print(g)
# print('+++++++++++++++2')
# h = np.split(np.arange(9), [2, -3])
# print(h)
# l0 = np.arange(6).reshape((2, 3))
# print(l0)
# l1 = np.arange(6, 12).reshape((2, 3))
# print(l1)
#
# m = np.vstack((l0, l1))
# print(m)
# p = np.hstack((l0, l1))
# print(p)
# q = np.concatenate((l0,l1))
# print(q)
# r = np.concatenate((l0, l1), axis = -1)
# print(r)
# s = np.stack((l0, l1))
# print(s)
# t = s.transpose((2, 0 , 1))
# print(t)
# u = a[0].transpose()
# print(u)
# v = np.rot90(u, 3)
# print(v)
# w = np.fliplr(u)
# print(w)
# x = np.flipud(u)
# print(x)
# y = np.roll(u, 1)
# print(y)
# z = np.roll(u, 1, axis=1)
# print(z)

###数学运算
# a = np.abs(-1)
# print(a)
# b = np.sin(np.pi/2)
# print(b)
# c = np.arctanh(0.462118)
# print(c)
# d = np.exp(3)
# print(d)
# f = np.power(2,3)
# print(f)
# g = np.dot([1,2], [3, 4])
# print(g)
# h = np.sqrt(25)
# print(h)
# l = np.sum([1,2,3,4])
# print(l)
# m = np.mean([4, 5, 6, 7])
# print(m)
# p = np.std([1, 2, 3, 2, 1, 3, 2, 0])
# print(p)

##位广播运算
# a = np.array([[1,2,3],[4,5,6]])
# b = np.array([[1,2,3],[1,2,3]])
# print(a + b)
# print(a - b)
# print(a * b)
# print(a / b)
# print(a ** 2)
# print(a ** b)
# c = np.array([
#     [1,2,3],
#     [4,5,6],
#     [7,8,9],
#     [10, 11, 12]
# ])
# d = np.array([2, 2, 2])
# print(c + d)
# print(c * d)
# print(c - 1)

###linalg
# a = np.array([3, 4])
# np.linalg.norm(a)
# b = np.array([
#     [1,2,3],
#     [4,5,6],
#     [7,8,9]
# ])
# c = np.array([1, 0, 1])
# print(np.dot(b, c))
# print(np.dot(c, b.T))
# print(np.trace(b))
# print(np.linalg.det(b))
# print(np.linalg.matrix_rank(b))
# d = np.array([
#     [2, 1],
#     [1, 2]
# ])
# u,v = np.linalg.eig(d)
# print(u)
# print(v)
# l = np.linalg.cholesky(d)
# print(l)
# np.dot(l, l.T)
# e = np.array([
#     [1, 2],
#     [3, 4]
# ])
# U, s, V = np.linalg.svd(e)
# print(U)
# print(s)
# print(V)
# print('===============')
# S = np.array([
#     [s[0], 0],
#     [0, s[1]]
# ])
# print(S)
# print(np.dot(U, np.dot(S, V)))

# random.seed(42)
# random.random(1, 3)
# random.random()
# random.random((3, 3))
# # random.sample((3, 3))
# # random.random_sample((3,3))
# random.ranf((3,3))
# 5*random.random(10) + 1
# random.uniform(1, 6, 10)
# print(random.randint(1, 6, 10))
