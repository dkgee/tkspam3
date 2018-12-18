# -*- coding: utf-8 -*-

from mxnet import nd

x = nd.arange(12)
print(x)
print(x.shape)
print(x.size)

x = x.reshape((3, 4))
print(x)

y = nd.zeros((2, 3, 4))
print(y)

z = nd.ones((3, 4))
print(z)

yy = nd.array([[2,1,4,3],[1,2,3,4],[4,3,2,1]])
print(yy)

xx = nd.random.normal(0, 1, (3, 4))
print(xx)

zz = x + yy
print(zz)

help(nd.ones_like)
