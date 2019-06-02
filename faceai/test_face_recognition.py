# -*- coding: utf-8 -*-

import face_recognition
from PIL import Image, ImageDraw

# 绘制脸部轮廓

image_path = "data/zxc.png"
# 将图片文件加载到numpy数组中
image = face_recognition.load_image_file(image_path)

# 查找图片中所有面部的所有面部特征
face_landmarks_list = face_recognition.face_landmarks(image)

for face_landmarks in face_landmarks_list:
    facial_features = [
        'chin', 'left_eyebrow', 'right_eyebrow', 'nose_bridge', 'nose_tip',
        'left_eye', 'right_eye', 'top_lip', 'bottom_lip'
    ]
    pil_image = Image.fromarray(image)
    d = ImageDraw.Draw(pil_image)
    for facial_feature in facial_features:
        d.line(face_landmarks[facial_feature], fill=(255,255,255), width=3)
    pil_image.show()

