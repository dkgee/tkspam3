# -*- coding: utf-8 -*-

import torch
import numpy as np
import torchvision.transforms as transforms
import matplotlib.pyplot as plt

class Rescale(object):
    """Rescale the image in a sample to a given size.
    Args:
        output_size (tuple or int): Desired output size. If tuple, output is
            matched to output_size. If int, smaller of image edges is matched
            to output_size keeping aspect ratio the same.
    """

    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        self.output_size = output_size

    def __call__(self, sample):
        image, landmarks = sample['image'], sample['landmarks']

        h, w = image.shape[:2]
        new_h, new_w = self.output_size

        top = np.random.randint(0, h - new_h)
        left = np.random.randint(0, h - new_w)

        image = image[ top: top + new_h, left: left + new_w]

        landmarks = landmarks - [left, top]

        return { 'image': image, 'landmarks': landmarks }

class RandomCrop(object):
    """Crop randomly the image in a sample.

      Args:
          output_size (tuple or int): Desired output size. If int, square crop
              is made.
      """
    def __init__(self, output_size):
        assert isinstance(output_size, (int, tuple))
        if isinstance(output_size, int):
            self.output_size = (output_size, output_size)
        else:
            assert len(output_size) == 2
            self.output_size = output_size

    def __call__(self, sample):
        image, landmarks = sample['image'], sample['landmarks']

        h, w = image.shape[:2]
        new_h, new_w = self.output_size

        top = np.random.randint(0, h - new_h)
        left = np.random.randint(0, w - new_w)

        image = image[ top: top + new_h, left: left + new_w]
        landmarks = landmarks - [left, top]

        return { 'image': image, 'landmarks': landmarks }

class ToTensor(object):
    """Convert ndarrays in sample to Tensors."""

    def __call__(self, sample):
        image, landmarks = sample['image'], sample['landmarks']

        # swap color axis because
        # numpy image: H x W x C
        # torch image: C x H x W
        image = image.transpose((2, 0, 1))
        return { 'image':torch.from_numpy(image), 'landmarks': torch.from_numpy(landmarks) }


# def show_landmarks(image, landmarks):
#     """Show image with landmarks"""
#     plt.imshow(image)
#     plt.scatter(landmarks[:, 0], landmarks[:, 1], s=10, marker='.', c='r')
#     plt.pause(0.001)    # pause a bit so that plots are updated
#     # plt.pause(0)        # 暂停n秒后自动关闭，当n=0时不关闭窗口
#
# import pytorch.demo02.FaceLandmarksDataset as FaceLandmarksDataset
# face_dataset = FaceLandmarksDataset(csv_file='data/faces/face_landmarks.csv', root_dir='data/faces/')
#
# scale = Rescale(256)
# crop = RandomCrop(128)
# composed = transforms.Compose([Rescale(256), Rescale(224)])
#
# # Apply each of the above transforms on sample.
# fig = plt.figure()
# sample = face_dataset[65]
# for i, tsfrm in enumerate([scale, crop, composed]):
#     transforms_sample = tsfrm(sample)
#
#     ax = plt.subplot(1, 3, i + 1)
#     plt.tight_layout()
#     ax.set_title(type(tsfrm).__name__)
#     show_landmarks(**transforms_sample)
#
# plt.show()