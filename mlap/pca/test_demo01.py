# -*- coding: utf-8 -*-

import time
import logging
from sklearn.datasets import fetch_olivetti_faces
from sklearn.model_selection import train_test_split
import numpy as np
import matplotlib.pyplot as plt

#logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger()
sh = logging.StreamHandler()
fm = logging.Formatter('%(asctime)s-%(filename)s[line%(lineno)d]-%(levelname)s-%(message)s')
sh.setFormatter(fm)
logger.addHandler(sh)  # logger添加标准输出流（std out）
logger.setLevel(logging.DEBUG)  # 设置从那个等级开始提示

def plot_gallery(images, titles, h, w, n_row=2, n_col=5):
    """显示图片阵列"""
    plt.figure(figsize=(2 * n_col, 2.2 * n_row), dpi=144)
    plt.subplots_adjust(bottom=0, left=.01, right=.99, top=.90, hspace=.01)
    for i in range(n_row * n_col):
        plt.subplot(n_row, n_col, i+1)
        plt.imshow(images[i].reshape((h, w)), cmap=plt.cm.gray)
        plt.title(titles[i])
        plt.axis('off')
    plt.show()

#主程序
data_home='datasets/'
logger.info('Start to load dataset')
faces = fetch_olivetti_faces(data_home=data_home)
logger.info('Done with load dataset')

X=faces.data
y=faces.target
targets = np.unique(faces.target)
target_names = np.array(["c%d" % t for t in targets])
n_targets = target_names.shape[0]
n_samples, h, w = faces.images.shape
print(' Sample count:', n_samples)
print(' Target count:', n_targets)
print(' Image size:', w, 'x', h)
print(' Dataset shape:', X.shape)

n_row = 2
n_col = 6

sample_images = None
sample_titles=[]
for i in range(n_targets):
    people_images = X[y == i]
    people_sample_index = np.random.randint(0, people_images.shape[0], 1)
    people_sample_image = people_images[people_sample_index, :]
    if sample_images is not None:
        sample_images = np.concatenate((sample_images, people_sample_image), axis=0)
    else:
        sample_images = people_sample_image
    sample_titles.append(target_names[i])
plot_gallery(sample_images, sample_titles, h, w, n_row, n_col)
x_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=4)


