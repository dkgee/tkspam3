# -*- coding: utf-8 -*-

import cv2

#### demo1
# color_img = cv2.imread('test_120x40.jpg')
# print(color_img.shape)
# gray_img = cv2.imread('test_120x40.jpg', cv2.IMREAD_GRAYSCALE)
# print(gray_img.shape)
# cv2.imwrite('test_grayscale.jpg', gray_img)
# reload_grayscale = cv2.imread('test_grayscale.jpg')
# print(reload_grayscale.shape)
# cv2.imwrite('test_imwrite.jpg', color_img, (cv2.IMWRITE_JPEG_QUALITY, 80))
# cv2.imwrite('test_imwrite2.jpg', color_img, (cv2.IMWRITE_PNG_COMPRESSION, 5))


###### demo2
img = cv2.imread('test3.jpg')
# img_200x200 = cv2.resize(img, (200, 200))
# img_200x300 = cv2.resize(img, (0, 0), fx=0.5, fy=0.5, interpolation=cv2.INTER_NEAREST)
# img_300x300 = cv2.copyMakeBorder(img, 50, 50, 0, 0, cv2.BORDER_CONSTANT, value=(0 , 0, 0))
# patch_tree = img[170:300, 300:480]      # 高从180到290， 宽从300到480
# cv2.imwrite('cropped_car.jpg', patch_tree)
# cv2.imwrite('resized_200x200.jpg', img_200x200)
# cv2.imwrite('resized_200x300.jpg', img_200x300)
# cv2.imwrite('resized_300x300.jpg', img_300x300)

# img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# turn_green_hsv = img_hsv.copy()
# turn_green_hsv[:, :, 0] = (turn_green_hsv[:, :, 0] + 15)%180
# turn_green_img = cv2.cvtColor(turn_green_hsv, cv2.COLOR_HSV2BGR)
# cv2.imwrite('turn_green.jpg', turn_green_img)

# colorless_hsv = img_hsv.copy()
# colorless_hsv[:, :, 1] =  0.5 * colorless_hsv[:, :, 1]
# colorless_img = cv2.cvtColor(colorless_hsv, cv2.COLOR_HSV2BGR)
# cv2.imwrite('colorless.jpg', colorless_img)

# darker_hsv = img_hsv.copy()
# darker_hsv[:, :, 2] = 0.5 * darker_hsv[:, :, 2]
# darker_img = cv2.cvtColor(darker_hsv, cv2.COLOR_HSV2BGR)
# cv2.imwrite('darker.jpg', darker_img)

# Gamma变换
# 分通道计算每个通道的直方图
hist_b = cv2.calcHist([img], [0], None, [256], [0, 256])
hist_g = cv2.calcHist([img], [1], None, [256], [0, 256])
hist_r = cv2.calcHist([img], [2], None, [256], [0, 256])

import numpy as np
def gamma_trans(img, gamma):
    gamma_table = [np.power(x/255.0, gamma) * 255.0 for x  in range(256)]
    gamma_table = np.round(np.array(gamma_table)).astype(np.uint8)
    return cv2.LUT(img, gamma_table)

img_corrected = gamma_trans(img, 0.5)
cv2.imwrite('gamma_corrected.jpg', img_corrected)
hist_b_corrected = cv2.calcHist([img_corrected], [0], None, [256], [0, 256])
hist_g_corrected = cv2.calcHist([img_corrected], [1], None, [256], [0, 256])
hist_r_corrected = cv2.calcHist([img_corrected], [2], None, [256], [0, 256])

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig = plt.figure()
pix_hists = [
    [hist_b, hist_g, hist_r],
    [hist_b_corrected, hist_g_corrected, hist_r_corrected]
]
pix_vals = range(256)
for sub_plt, pix_hist in zip([121, 122], pix_hists):
    ax = fig.add_subplot(sub_plt, projection='3d')
    for c, z, channel_hist in zip(['b', 'g', 'r'], [20, 10, 0], pix_hist):
        cs = [c] * 256
        ax.bar(pix_vals,channel_hist,zs=z,zdir='y',color=cs,alpha=0.618,edgecolor='none',lw=0)

    ax.set_xlabel('Pixel Values')
    ax.set_xlim([0, 256])
    ax.set_ylabel('Counts')
    ax.set_zlabel('Channels')
plt.show()
# cv2.waitKey()