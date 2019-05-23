# -*- coding: utf-8 -*-
import os
import pandas as pd
from skimage import io, transform
import matplotlib.pyplot as plt
import torch.utils.data.dataset as Dataset

class FaceLandmarksDataset(Dataset):
    """Face Landmarks dataset."""

    def __init__(self, csv_file, root_dir, transform=None):
        """
        :param csv_file: Path to the csv file with annotations.
        :param root_dir: Directory with all the images.
        :param transform: Optional transform to be applied on a sample.
        """
        self.landmarks_frame = pd.read_csv(csv_file)
        self.root_dir = root_dir
        self.transform = transform

    def __len__(self):
        return len(self.landmarks_frame)

    def __getitem__(self, idx):
        img_name = os.path.join(self.root_dir, self.landmarks_frame.iloc[idx, 0])
        image = io.imread(img_name)
        landmarks = self.landmarks_frame.iloc[idx, 1:].as_matrix()
        landmarks = landmarks.astype('float').reshape(-1, 2)
        sample = { 'image': image, 'landmarks': landmarks }

        if self.transform:
            sample = self.transform(sample)

        return sample

# def show_landmarks(image, landmarks):
#     """Show image with landmarks"""
#     plt.imshow(image)
#     plt.scatter(landmarks[:, 0], landmarks[:, 1], s=10, marker='.', c='r')
#     # plt.pause(0.001)    # pause a bit so that plots are updated
#     plt.pause(0)        # 暂停n秒后自动关闭，当n=0时不关闭窗口
#
# face_dataset = FaceLandmarksDataset(csv_file='data/faces/face_landmarks.csv', root_dir='data/faces/')
#
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
#         break
