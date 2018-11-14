# -*- coding: utf-8 -*-

import os,sys
import pickle, gzip
from matplotlib import pyplot

# if sys.getdefaultencoding() != 'utf-8':
#     reload(sys)
#     sys.setdefaultencoding('utf-8')



# 手写字体识别

print('Loading data from mnist.pkl.gz ...')
path=r'D:\dlcv_data\mnist.pkl.gz'
with gzip.open(path, 'rb+') as f:
    train_set, valid_set, test_set = pickle.load(f, encoding='latin1')

imgs_dir = 'mnist'
# os.system('mkdir -p {}'.format(imgs_dir))
if not os.path.exists(imgs_dir):
    os.makedirs(imgs_dir)

datasets = { 'train': train_set, 'val': valid_set, 'test': test_set }

for dataname, dataset in datasets.items():
    print('Converting {} dataset ...'.format(dataname))
    data_dir = os.sep.join([imgs_dir, dataname])
    # os.system('mkdir -p {}'.format(data_dir))
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
    for i, (img, label) in enumerate(zip(*dataset)):
        filename = '{:0>6d}_{}.jpg'.format(i, label)
        filepath = os.sep.join([data_dir, filename])
        img = img.reshape((28,28))
        pyplot.imsave(filepath, img, cmap='gray')
        if (i+1) % 10000 == 0:
            print('{} images converted!'.format(i + 1))
