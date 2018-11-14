# -*- coding: utf-8 -*-

import torch
import torch.optim as optim
import matplotlib.pyplot as plt

def get_fake_data(batch_size=32):
    """ y = x*2 + 3"""
    x = torch.randn(batch_size, 1) * 20
    y = x * 2 + 3 + torch.randn(batch_size, 1)
    return x, y

x,y = get_fake_data()

class LinerRegress(torch.nn.Module):
    def __init__(self):
        super(LinerRegress, self).__init__()
        self.fc1 = torch.nn.Linear(1,1)

    def forward(self,x):
        return self.fc1(x)

net = LinerRegress()
loss_func = torch.nn.MSELoss()
optimzer = optim.SGD(net.parameters(), lr = 0.01)

for i in range(40000):
    optimzer.zero_grad()

    out = net(x)
    loss = loss_func(out, y)
    loss.backward()

    optimzer.step()

w, b = [param.item() for param in net.parameters()]
print('%s,%s'%(w, b))

#显示原始点与拟合直线
plt.scatter(x.squeeze().numpy(), y.squeeze().numpy())
plt.plot(x.squeeze().numpy(), y.squeeze().numpy())
plt.show()

