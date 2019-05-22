# -*- coding: utf-8 -*-

from __future__ import  print_function
import torch


## 声明一个5 x 3且初始值为0的向量
# x = torch.empty(5, 3)
# print(x)

## 构建一个随机向量组，随机数是保留4位小数的浮点数
# x = torch.rand(5, 3)
# print(x)


## 构建一个零向量,且数据类型为long的矩阵
# x = torch.zeros(5, 3, dtype=torch.long)
# print(x)

## 从数据中直接构建一个向量矩阵, 会转换为保留4位浮点精度的数据
# x = torch.tensor([5.5, 3])
# print(x)

## 基于存在的张量创建矩阵，可以指定矩阵的数据类型
# x = x.new_ones(5, 3, dtype=torch.double)    ## 创建所有值为1且为5 x 3的矩阵
# print(x)

## 创建要给像x一样的随机矩阵，且矩阵的数据类型为浮点类型
# x = torch.rand_like(x, dtype=torch.float)
# print(x)
## 获取矩阵的尺寸
# print(x.size())

## 创建一个y矩阵，并加上x矩阵
# y = torch.rand(5, 3)
# print(x + y)    #第一种加法
#
# print(torch.add(x, y))  #第二种加法

##提供一个输出向量作为参数
# result = torch.empty(5, 3)
# torch.add(x, y, out=result)
# print(result)

## x或y矩阵自带方法进行向量加法操作
# y.add_(x)
# print(y)

# print(x[:, 1])  #todo 没看懂

## 如果需要重新调整向量的大小
x = torch.randn(4, 4)
# y = x.view(16)
# z = x.view(-1, 8)
# print(x)
# print(y)
# print(z)
# print(x.size(), y.size(), z.size())

## 如果矩阵只有一个元素，使用.item()方法获取值
# x = torch.randn(1)
# print(x)
# print(x.item())

# a = torch.ones(5)   #这是tensor（张量）
# print(a)
#
# b = a.numpy()       #这是numpy矩阵
# print(b)
#
# a.add_(1)           #可以使用该方法，该方法使每个元素都加一，但基于该向量计算的所有都会加一
# print(a)
# print(b)

# import numpy as np
#
# a = np.ones(5)          # 获取一个5维值为1的矩阵
# b = torch.from_numpy(a) # 将矩阵转换为tensor（张量）
# np.add(a, 1, out=a)     #将矩阵a加一并输出到a
# print(a)                #a==b都是基于内存计算
# print(b)


if torch.cuda.is_available():
    device = torch.device("cuda")
    y = torch.ones_like(x, device=device)
    x = x.to(device)
    z = x + y
    print(z)
    print(z.to("cpu", torch.double))
else:
    print("cuda is not available")