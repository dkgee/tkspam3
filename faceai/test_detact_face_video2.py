# -*- coding: utf-8 -*-

# OpenCV版本视频检测

import cv2
import dlib

#人脸分类器
detector = dlib.get_frontal_face_detector()

#图片识别方法封装
def discern(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    dets = detector(gray, 1)
    for face in dets:
        left = face.left()
        top = face.top()
        right = face.right()
        bottom = face.bottom()
        cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.imshow("Image", img)

#获取摄像头0表示第一个摄像头
cap = cv2.VideoCapture(0)
while (1):  #逐帧显示
    ret, img = cap.read()
    discern(img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()   #释放摄像头
cv2.destroyAllWindows()

#OpenCV和Dlib的视频识别对比，有两个地方是不同的：
# 1.Dlib模型识别的准确率和效果要好于OpenCV；
# 2.Dlib识别的性能要比OpenCV差，使用视频测试的时候Dlib有明显的卡顿，但是OpenCV就好很多，基本看不出来；
