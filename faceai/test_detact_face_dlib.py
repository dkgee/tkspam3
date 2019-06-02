# -*- coding: utf-8 -*-

import cv2
import dlib

# path = "data/angelababy.png"  #能识别
#path = "data/jp.png" #能识别
# path = "data/jp2.png"   #能识别
# path = "data/jp3.png"   #能识别
# path = "data/jp22.png"   #能识别
# path = "data/jp33.png"   #能识别
# path = "data/ldh.png"   #能识别
# path = "data/zxc.png"   #能识别
# path = "data/ldh.png"   #能识别
path = "data/jht.jpg"  #能识别

# dlib识别率高，采用人脸的68个标定点，在测试样本集中基本都能识别


img = cv2.imread(path)
img_gray = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)

#人脸分类器
detector = dlib.get_frontal_face_detector()
#获取人脸检测器
predictor = dlib.shape_predictor(
    "D:\\Anaconda3\\envs\dev3.6\\Lib\site-packages\\dlib-datadlib-data\\shape_predictor_68_face_landmarks.dat"
)

dets = detector(img_gray, 1)
for face in dets:
    shape = predictor(img_gray,face)
    for pt in shape.parts():
        pt_pos = (pt.x, pt.y)
        cv2.circle(img, pt_pos, 2, (0, 255, 0), 1)
    cv2.imshow("Image", img)

cv2.waitKey(0)
cv2.destroyAllWindows()