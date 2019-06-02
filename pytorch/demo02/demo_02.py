# -*- coding: utf-8 -*-

from __future__ import  print_function, division
import os
import torch
import pandas as pd
from skimage import io, transform
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils


#Ignore warnings
import warnings

warnings.filterwarnings("ignore")

# interactive mode
plt.ion()

# 当前目录下data目录
landmarks_frame = pd.read_csv('data/faces/face_landmarks.csv')

n=65
img_name = landmarks_frame.iloc[n, 0]
landmarks = landmarks_frame.iloc[n, 1:].as_matrix()
landmarks = landmarks.astype('float').reshape(-1, 2)

print('Image name:{}'.format(img_name))
print('Landmarks shape:{}'.format(landmarks.shape))
print('First 4 Landmarks:{}'.format(landmarks[:4]))

def show_landmarks(image, landmarks):
    """Show image with landmarks"""
    plt.imshow(image)
    plt.scatter(landmarks[:, 0], landmarks[:, 1], s=10, marker='.', c='r')
    plt.pause(0.001)    # pause a bit so that plots are updated
    # plt.pause(0)        # 暂停n秒后自动关闭，当n=0时不关闭窗口

# plt.figure()
# show_landmarks(io.imread(os.path.join('data/faces', img_name)), landmarks)
# plt.show()

#
# class FaceLandmarksDataset(Dataset):
#     """Face Landmarks dataset."""
#
#     def __init__(self, csv_file, root_dir, transform=None):
#         """
#         :param csv_file: Path to the csv file with annotations.
#         :param root_dir: Directory with all the images.
#         :param transform: Optional transform to be applied on a sample.
#         """
#         self.landmarks_frame = pd.read_csv(csv_file)
#         self.root_dir = root_dir
#         self.transform = transform
#
#     def __len__(self):
#         return len(self.landmarks_frame)
#
#     def __getitem__(self, idx):
#         img_name = os.path.join(self.root_dir, self.landmarks_frame.iloc[idx, 0])
#         image = io.imread(img_name)
#         landmarks = self.landmarks_frame.iloc[idx, 1:].as_matrix()
#         landmarks = landmarks.astype('float').reshape(-1, 2)
#         sample = { 'image': image, 'landmarks': landmarks }
#
#         if self.transform:
#             sample = self.transform(sample)
#
#         return sample

import pytorch.demo02.FaceLandmarksDataset as FaceLandmarksDataset

face_dataset = FaceLandmarksDataset(csv_file='data/faces/face_landmarks.csv', root_dir='data/faces/')

# fig = plt.figure()
# for i in range(len(face_dataset)):
#     sample = face_dataset[i]
#
#     print(i, sample['image'].shape, sample['landmarks'].shape)
#
#     ax = plt.subplot(1, 4, i + 1)
#     plt.tight_layout()
#     ax.set_title('Sample #{}'.format(i))
#     ax.axis('off')
#     show_landmarks(**sample)
#
#     if i == 3:
#         plt.show()
#         # plt.pause(0)
#         break

from pytorch.demo02.Rescale import Rescale, RandomCrop

scale = Rescale(256)
crop = RandomCrop(128)
composed = transforms.Compose([Rescale(256), Rescale(224)])

# Apply each of the above transforms on sample.
fig = plt.figure()
sample = face_dataset[65]
for i, tsfrm in enumerate([scale, crop, composed]):
    transforms_sample = tsfrm(sample)

    ax = plt.subplot(1, 3, i + 1)
    plt.tight_layout()
    ax.set_title(type(tsfrm).__name__)
    show_landmarks(**transforms_sample)

plt.show()