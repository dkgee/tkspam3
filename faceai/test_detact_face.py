# -*- coding: utf-8 -*-

import cv2

# filepath = 'data/angelababy.png'  # 能够识别
# filepath = 'data/jp.png'    # 能识别
# filepath = 'data/jp2.png'    # 未识别出来，可能原因裸露皮肤太多
# filepath = 'data/jp3.png'    # 识别错误，裸露皮肤太多
# filepath = 'data/jp22.png'    # 未识别出来，可能原因是脸被头发遮挡
# filepath = 'data/jp33.png'    # 未识别出来，可能原因是脸被头发遮挡
# filepath = 'data/zxc.png'    # 能识别
# filepath = 'data/ldh.png'    # 能识别
filepath = 'data/jht.jpg'    # 能识别

img = cv2.imread(filepath)
# 灰阶处理
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#opencv 人脸识别分类器
classifier = cv2.CascadeClassifier(
    "D:\Anaconda3\envs\dev3.6\Lib\site-packages\opencv-master\data\haarcascades\haarcascade_frontalface_default.xml"
)

color = (0, 255, 0) #定义绘制颜色

#调用识别人脸
faceRects = classifier.detectMultiScale(
    img_gray, scaleFactor=1.2, minNeighbors=3, minSize=(32, 32))

if len(faceRects): #大于0则检测到人脸
    for faceRect in faceRects: # 单独框出每一张人脸
        x, y, w, h = faceRect
        # 框出人脸
        cv2.rectangle(img, (x, y), (x + h, y + w), color, 2)
        # 左眼
        cv2.circle(img, (x + w//4, y + h//4 + 30), min(w // 8, h // 8), color)
        # 右眼
        cv2.circle(img, (x + 3 * w // 4, y + h // 4 + 30), min(w // 8, h // 8), color)
        #嘴巴
        cv2.rectangle(img, (x + 3 * w // 8, y + 3 * h // 4), (x + 5 * w // 8, y + 7 * h // 8), color)

# x = y = 10      #坐标
# w = 100         #矩形大小（宽、高）
# color = (90, 90, 87) #定义绘制颜色
# cv2.rectangle(img_gray, (x, y), (x + w, y + w), color, 1) #绘制矩形


# 显示图像
cv2.imshow("Image", img)
c = cv2.waitKey(10)
cv2.waitKey(0)
cv2.destroyAllWindows()